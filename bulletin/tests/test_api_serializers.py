from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from bulletin.api.serializers import BulletinSerializer
from bulletin.models import Bulletin


class TestBulletinSerializer(TestCase):

    def setUp(self):
        self.bulletin_details = {
            'time_of_quake': timezone.now(),
            'url': 'https://phivolcs.gov.ph',
            'latitude': Decimal(6.7),
            'longitude': Decimal(125.1),
            'depth': Decimal(10),
            'magnitude': Decimal(4.5),
            'location': 'Somewhere in time'
        }
        self.bulletin = Bulletin.objects.create(**self.bulletin_details)
        self.bulletin_serializer = BulletinSerializer(instance=self.bulletin)

    def test_serializer_has_expected_fields_only(self):
        serialized_data = self.bulletin_serializer.data
        self.assertCountEqual(
            serialized_data.keys(),
            self.bulletin_details.keys()
        )
        self.assertNotIn('id', serialized_data.keys())
