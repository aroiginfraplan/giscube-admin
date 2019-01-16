import datetime
import json
import os
import pytz
import requests

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone

from django_celery_monitor.models import TaskState

from .models import GeoJsonLayer


def geojsonlayer_check_cache(layer):
    """
    Check if the layer has url and has been ever generated.
    Check layer cache_time.
    Check if there is an async_geojsonlayer_refresh pending or in process.
    """
    if layer.url and layer.generated_on:
        cache_time = layer.cache_time or 0
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        layer_time = layer.generated_on.utcnow().replace(tzinfo=pytz.utc) + datetime.timedelta(seconds=cache_time)

        if now < layer_time:
            return

        qs = TaskState.objects.filter(
            name='layerserver.tasks.async_geojsonlayer_refresh',
            state__in=['PENDING', 'RECEIVED', 'STARTED'],
            args='(%s,)' % layer.pk
        )
        if qs.count() > 0:
            return

        from .tasks import async_geojsonlayer_refresh
        async_geojsonlayer_refresh.delay(layer.pk)


def geojsonlayer_refresh(pk):
    layer = GeoJsonLayer.objects.get(pk=pk)
    geojsonlayer_refresh_layer(layer)


def geojsonlayer_refresh_layer(layer):
    if layer.url:
        try:
            r = requests.get(layer.url)
        except Exception as e:
            print('Error getting file %s' % e)
        else:
            content = ContentFile(r.text)
            if content:
                remote_file = os.path.join(
                    settings.MEDIA_ROOT, layer.service_path, 'remote.json')
                if os.path.exists(remote_file):
                    os.remove(remote_file)
                layer.data_file.save('remote.json', content, save=True)
                layer.last_fetch_on = timezone.localtime()

    if layer.data_file:
        path = os.path.join(settings.MEDIA_ROOT, layer.data_file.path)
        data = json.load(open(path))
        data['metadata'] = layer.metadata
        outfile_path = os.path.join(
            settings.MEDIA_ROOT, layer.service_path, 'data.json')
        with open(outfile_path, 'wb') as fixed_file:
            fixed_file.write(json.dumps(data))
        layer.generated_on = timezone.localtime()
        layer.save()