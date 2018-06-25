import os
import json

from django.conf import settings


def generateGeoJsonLayer(instance):
    if not instance.data_file:
        return

    path = os.path.join(settings.MEDIA_ROOT, instance.data_file.path)
    data = json.load(open(path))
    data['metadata'] = instance.metadata
    outfile_path = os.path.join(
        settings.MEDIA_ROOT, instance.service_path, 'data.json')
    with open(outfile_path, "wb") as fixed_file:
        fixed_file.write(json.dumps(data))