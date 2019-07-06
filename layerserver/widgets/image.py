import inspect
import json
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.validators import URLValidator
from django.utils.translation import gettext as _

from giscube.utils import url_slash_join
from layerserver.storage import get_image_with_thumbnail_storage_class

from .base import BaseJSONWidget


class ImageWidget(BaseJSONWidget):
    TEMPLATE = inspect.cleandoc("""
    {
        "upload_root": "%s",
        "base_url": "%s",
        "thumbnail_root": "%s",
        "thumbnail_base_url": "%s"
    }
    """ % (
        os.path.join(settings.MEDIA_ROOT, 'images'),
        url_slash_join(settings.GISCUBE_URL, settings.MEDIA_URL.replace(settings.APP_URL, ''), 'images'),
        os.path.join(settings.MEDIA_ROOT, 'thumbnails'),
        url_slash_join(settings.GISCUBE_URL, settings.MEDIA_URL.replace(settings.APP_URL, ''), 'thumbnails'),
    ))
    ERROR_UPLOAD_ROOT_REQUIRED = _('\'upload_root\' attribute is required')
    ERROR_UPLOAD_ROOT_NOT_EXISTS = _('\'upload_root\' folder doesn\'t exist')
    ERROR_UPLOAD_ROOT_NOT_WRITABLE = ('\'upload_root\' folder is not writable')
    ERROR_BASE_URL = ('\'base_url\' is not valid')
    ERROR_THUMBNAIL_ROOT_NOT_EXISTS = _('\'thumbnail_root\' folder doesn\'t exist')
    ERROR_THUMBNAIL_ROOT_NOT_WRITABLE = ('\'thumbnail_root\' folder is not writable')
    ERROR_THUMBNAIL_BASE_URL = ('\'thumbnail_base_url\' is not valid')
    base_type = 'image'

    @staticmethod  # noqa: C901
    def is_valid(value):
        try:
            data = json.loads(value)
        except Exception:
            return ImageWidget.ERROR_INVALID_JSON

        if 'upload_root' not in data:
            return ImageWidget.ERROR_UPLOAD_ROOT_REQUIRED

        base_url = data.get('base_url', None)
        thumbnail_root = data.get('thumbnail_root', None)
        thumbnail_base_url = data.get('thumbnail_base_url', None)
        StorageClass = get_image_with_thumbnail_storage_class()
        storage = StorageClass(
            location=data['upload_root'],
            base_url=base_url,
            thumbnail_location=thumbnail_root,
            thumbnail_base_url=thumbnail_base_url
        )
        try:
            storage.listdir('.')
        except OSError:
            return ImageWidget.ERROR_UPLOAD_ROOT_NOT_EXISTS

        if issubclass(StorageClass, FileSystemStorage):
            path = storage.path('.')
            if not os.access(path, os.W_OK):
                return ImageWidget.ERROR_UPLOAD_ROOT_NOT_WRITABLE

        if base_url is not None:
            val = URLValidator()
            try:
                val(base_url)
            except ValidationError:
                return ImageWidget.ERROR_BASE_URL

        if thumbnail_root is not None:
            thumbnail_storage = storage.get_thumbnail_storage()
            try:
                thumbnail_storage.listdir('.')
            except OSError:
                return ImageWidget.ERROR_THUMBNAIL_ROOT_NOT_EXISTS

            if issubclass(thumbnail_storage.__class__, FileSystemStorage):
                path = thumbnail_storage.path('.')
                if not os.access(path, os.W_OK):
                    return ImageWidget.ERROR_THUMBNAIL_ROOT_NOT_WRITABLE

        if thumbnail_base_url is not None:
            val = URLValidator()
            try:
                val(thumbnail_base_url)
            except ValidationError:
                return ImageWidget.ERROR_THUMBNAIL_BASE_URL

    @staticmethod
    def serialize_widget_options(obj):
        try:
            options = json.loads(obj.widget_options)
        except Exception:
            return {'error': 'ERROR PARSING WIDGET OPTIONS'}

        widget_options = {}
        if 'upload_size' in options:
            widget_options['upload_size'] = options['upload_size']
        data = {'widget_options': widget_options}
        return data
