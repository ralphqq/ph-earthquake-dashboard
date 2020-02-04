from django.db.utils import IntegrityError
from django.test import TestCase

from bulletin.factories import BulletinFactory
from bulletin.models import Bulletin


class BulletinModelTest(TestCase):

    def test_completing_required_fields(self):
        b = BulletinFactory()
        b.save()
        self.assertEqual(Bulletin.objects.count(), 1)

    def test_violating_not_null_fields(self):
        with self.assertRaises(IntegrityError):
            b = BulletinFactory(
                time_of_quake=None,
                url=None
            )
            b.save()

    def test_duplicate_bulletins(self):
        same_url = 'https://www.same-url.com/'
        b1 = BulletinFactory.create(url=same_url)
        with self.assertRaises(IntegrityError):
            b2 = BulletinFactory(url=same_url)

