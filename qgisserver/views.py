import logging
import os

import requests

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.utils.cache import patch_response_headers

import oauth2_provider
import rest_framework.authentication

from rest_framework.views import APIView

from giscube.tilecache.caches import GiscubeServiceCache
from giscube.tilecache.image import tile_cache_image
from giscube.tilecache.proj import GoogleProjection
from giscube.utils import get_service_wms_bbox
from giscube.views_mixins import WMSProxyBufferViewMixin
from giscube.views_utils import web_map_view

from .models import Service


logger = logging.getLogger(__name__)


class View(APIView):
    authentication_classes = (
        rest_framework.authentication.SessionAuthentication,
        oauth2_provider.contrib.rest_framework.OAuth2Authentication
    )
    permission_classes = ()


class ServiceMixin:
    model = Service

    def get_queryset(self, *args, **kwargs):
        qs = self.model.objects.filter(active=True)
        filter_anonymous = Q(anonymous_view=True)

        if self.request.user.is_anonymous:
            qs = qs.filter(filter_anonymous)
        else:
            self.user_groups = self.request.user.groups.values_list('name', flat=True)
            filter_authenticated_user_view = Q(authenticated_user_view=True)
            filter_group = (
                Q(group_permissions__group__name__in=self.user_groups) & Q(group_permissions__can_view=True))
            filter_user = Q(user_permissions__user=self.request.user) & Q(
                user_permissions__can_view=True)
            qs = qs.filter(
                filter_anonymous | filter_authenticated_user_view | filter_user | filter_group).distinct()

        return qs

    def _get_object(self, service_name):
        qs = self.get_queryset()
        service = qs.filter(name=service_name).first()
        if not service:
            raise PermissionDenied()
        return service


class QGISServerWMSView(WMSProxyBufferViewMixin, ServiceMixin):
    def get_wms_buffer_enabled(self):
        return self.service.wms_buffer_enabled

    def get_wms_buffer_size(self):
        return self.service.wms_buffer_size or ''

    def get_wms_tile_sizes(self):
        return (self.service.wms_tile_sizes or '').splitlines()

    def get(self, request, service_name):
        self.service = self._get_object(request, service_name)
        return super().get(request)

    def do_post(self, request, service_name):
        self.service = self._get_object(request, service_name)
        url = self.build_url(request)
        return requests.post(url, data=request.body)

    def build_url(self, request):
        meta = request.META.get('QUERY_STRING', '')
        url = "%s&%s" % (self.service.service_internal_url, meta)
        return url


class QGISServerTileCacheView(View, ServiceMixin):

    def get(self, request, service_name):
        service = self._get_object(request, service_name)
        data = {}
        if self.service.tilecache_enabled:
            data.update(
                {
                    'bbox': service.tilecache_bbox,
                    'min_zoom': service.tilecache_minzoom_level,
                    'max_zoom': service.tilecache_maxzoom_level
                }
            )
        return JsonResponse(data)


class QGISServerTileCacheTilesView(View, ServiceMixin):

    def build_url(self, service):
        url = service.service_internal_url
        if service.tilecache_transparent:
            url = '%s&transparent=True' % url
        return url

    def get(self, request, service_name, z, x, y, image_format='png'):
        service = self._get_object(request, service_name)

        if not service.tilecache_enabled:
            raise Http404()

        if z < service.tilecache_minzoom_level or z > service.tilecache_maxzoom_level:
            return HttpResponseBadRequest()

        bbox = self.tile2bbox(z, x, y)
        layers = os.path.splitext(os.path.basename(service.project_file.name))[0]
        tile_options = {
            'url': self.build_url(service),
            'layers': layers,
            'xyz': [z, x, y],
            'bbox': bbox,
            'srs': 'EPSG:3857'
        }

        buffer = [0, 0]
        if service.wms_buffer_enabled:
            buffer = list(map(int, service.wms_buffer_size.split(',')))
        cache = GiscubeServiceCache(service)
        image = tile_cache_image(tile_options, buffer, cache)
        response = HttpResponse(image, content_type='image/%s' % image_format)
        patch_response_headers(response, cache_timeout=60 * 60 * 24 * 7)
        response.status_code = 200
        return response

    def tile2bbox(self, z, x, y):
        proj = GoogleProjection(256, [z])
        bbox = proj.tile_bbox((z, x, y))
        return proj.project(bbox[:2]) + proj.project(bbox[2:])


class QGISServerMapViewerView(View, ServiceMixin):

    def get(self, request, service_name):
        service = self._get_object(request, service_name)

        layers = []
        layers.append(
            {
                'name': '%s (WMS)' % (service.title or service.name),
                'type': 'wms',
                'layers': service.default_layer,
                'url': reverse('qgisserver', args=(service.name, '',)),
                'transparent': service.tilecache_enabled and service.tilecache_transparent
            }
        )
        if service.tilecache_enabled:
            layers.append(
                {
                    'name': '%s (Tile Cache)' % (service.title or service.name),
                    'type': 'tile',
                    'url': '%s{z}/{x}/{y}.png' % reverse('qgisserver-tilecache', args=(service.name,))
                }
            )
        extra_context = {
            'title': service.title or service.name,
            'layers': layers
        }
        bbox = get_service_wms_bbox(service.service_internal_url)
        if bbox:
            extra_context['bbox'] = list(bbox)

        return web_map_view(request, extra_context)
