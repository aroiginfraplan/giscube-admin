# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.urls import reverse

from giscube.models import DBConnection
from layerserver.models import DataBaseLayer
from tests.common import BaseTest

from layerserver.model_legacy import create_dblayer_model


class DataBaseLayerBulkAPITestCase(BaseTest):
    def setUp(self):
        super(self.__class__, self).setUp()
        conn = DBConnection()
        conn.alias = 'test_connection'
        conn.engine = settings.DATABASES['default']['ENGINE']
        conn.name = settings.DATABASES['default']['NAME']
        conn.user = settings.DATABASES['default']['USER']
        conn.password = settings.DATABASES['default']['PASSWORD']
        conn.host = settings.DATABASES['default']['HOST']
        conn.port = settings.DATABASES['default']['PORT']
        conn.save()

        layer = DataBaseLayer()
        layer.db_connection = conn
        layer.slug = 'tests_location'
        layer.name = 'tests_location'
        layer.table = 'tests_location'
        layer.pk_field = 'code'
        layer.geometry_field = 'geometry'
        layer.anonymous_view = True
        layer.anonymous_add = True
        layer.anonymous_update = True
        layer.anonymous_delete = True
        layer.save()
        self.layer = layer

        self.locations = []
        Location = create_dblayer_model(layer)
        self.Location = Location
        for i in range(0, 12):
            location = Location()
            location.code = 'C%s' % str(i).zfill(3)
            location.address = 'C/ Jaume %s, Girona' % i
            location.geometry = 'POINT(0 %s)' % i
            location.save()
            self.locations.append(location)

    def test_bulk_ok(self):
        data = {
            'ADD': [
                {
                    'code': 'A101',
                    'address': 'C/ Jaume 100, Girona',
                    'geometry': 'POINT (0 10)'
                },
                {
                    'code': 'A102',
                    'address': 'C/ Jaume 100, Girona',
                    'geometry': 'POINT (11 10)'
                },
            ],
            'UPDATE': [
                {
                    'code': self.locations[2].code,
                    'geometry': 'POINT (0 10)'
                },
                {
                    'code': self.locations[5].code,
                    'address': 'C/ Cor de Maria 5, Girona',
                    'geometry': 'POINT (11 10)'
                },
                {
                    'code': self.locations[1].code,
                    'address': 'C/ Cor de Maria 1, Girona'
                }
            ],
            'DELETE': [self.locations[9].code, self.locations[10].code]
        }

        url = reverse('content-bulk', kwargs={'layer_slug': self.layer.slug})
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        obj = self.Location.objects.get(code=self.locations[2].code)
        self.assertEqual(obj.geometry.wkt, data['UPDATE'][0]['geometry'])

        obj = self.Location.objects.get(code=self.locations[5].code)
        self.assertEqual(obj.address, data['UPDATE'][1]['address'])
        self.assertEqual(obj.geometry.wkt, data['UPDATE'][1]['geometry'])

        obj = self.Location.objects.get(code=self.locations[1].code)
        self.assertEqual(obj.address, data['UPDATE'][2]['address'])

        self.assertEqual(
            0, self.Location.objects.filter(code__in=data['DELETE']).count())

    def test_bulk_not_found(self):
        data = {
            'ADD': [],
            'UPDATE': [
                {
                    'code': 'XXXX',
                    'geometry': 'POINT (0 10)'
                },
                {
                    'code': self.locations[5].code,
                    'address': 'C/ Cor de Maria 5, Girona',
                    'geometry': 'POINT (11 10)'
                },
                {
                    'code': self.locations[1].code,
                    'address': 'C/ Cor de Maria 1, Girona'
                }
            ],
            'DELETE': []
        }
        url = reverse('content-bulk', kwargs={'layer_slug': self.layer.slug})
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_bulk_geometry_null(self):
        data = {
            'ADD': [],
            'UPDATE': [
                {
                    'code': self.locations[5].code,
                    'address': 'C/ Cor de Maria 5, Girona',
                    'geometry': None
                }
            ],
            'DELETE': []
        }
        url = reverse('content-bulk', kwargs={'layer_slug': self.layer.slug})
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertTrue('geometry' in result['UPDATE'][0])