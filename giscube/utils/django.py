import os
import tempfile

from django.conf import settings
from django.core import mail
from django.core.mail import get_connection
from django.utils import log
from django.utils.module_loading import import_string
from django.utils.version import get_version as django_get_version


class AdminEmailHandler(log.AdminEmailHandler):
    def send_mail(self, subject, message, *args, **kwargs):
        kwargs['fail_silently'] = False
        mail.mail_admins(subject, message, *args, connection=self.connection(), **kwargs)

    def connection(self):
        return get_connection(backend=self.email_backend, fail_silently=False)


def get_cls(key, default=None):
    value = getattr(settings, key, None)
    if type(value) is type:
        return value
    elif type(value) is tuple or type(value) is list:
        return tuple(import_string(p) for p in value if type(p) is str)
    elif type(value) is str:
        return import_string(value)
    else:
        return default


def get_version(version=None):
    if version is None:
        from giscube import VERSION as version

    return django_get_version(version)


def unique_service_directory(instance, filename=None):
    if not instance.service_path:
        path = os.path.join(settings.MEDIA_ROOT, instance._meta.app_label)
        path = os.path.abspath(path)
        if not os.path.exists(path):
            os.makedirs(path)
        pathname = tempfile.mkdtemp(prefix='%s_' % instance.name, dir=path)
        pathname = os.path.relpath(pathname, settings.MEDIA_ROOT)
        instance.service_path = pathname
    if filename:
        return os.path.join(instance.service_path, filename)
    else:
        return instance.service_path