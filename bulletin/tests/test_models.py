from django.db.utils import IntegrityError
from django.test import TestCase

from bulletin.models import Bulletin


class BulletinModelTest(TestCase):

    def test_completing_required_fields(self):
        b = Bulletin(
            url='https://earthquake.phivolcs.gov.ph/',
            latitude=6.9,
            longitude=125.2,
            depth=35,
            magnitude=1.9
        )
        b.save()
        self.assertEqual(Bulletin.objects.count(), 1)

    def test_violating_not_null_fields(self):
        with self.assertRaises(IntegrityError):
            b = Bulletin()
            b.save()
