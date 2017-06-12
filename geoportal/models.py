from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    keywords = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s' % self.title or self.name


RESOURCE_TYPE_CHOICES = [ 
    ('TMS', 'TMS'),
    ('WMS', 'WMS'),
]


class Resource(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='resources')
    type = models.CharField(max_length=12, choices=RESOURCE_TYPE_CHOICES)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=100, null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    layers = models.CharField(max_length=255, null=True, blank=True)
    projection = models.IntegerField(help_text='EPSG code')

    def __unicode__(self):
        return '%s' % self.title or self.name