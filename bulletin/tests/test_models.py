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
            b = BulletinFactory(url=None)
            b.save()

    def test_null_time_of_quake_is_allowed(self):
        b = BulletinFactory(time_of_quake=None)
        b.save()
        self.assertEqual(Bulletin.objects.count(), 1)

    def test_duplicate_bulletins(self):
        same_url = 'https://www.same-url.com/'
        b1 = BulletinFactory.create(url=same_url)
        with self.assertRaises(IntegrityError):
            b2 = BulletinFactory(url=same_url)


class BulletinScrapedAtAndUpdatedAtTest(TestCase):

    def setUp(self):
        self.bulletin = BulletinFactory.create()

    def test_first_time_save(self):
        self.assertIsNotNone(self.bulletin.scraped_at)
        self.assertIsNotNone(self.bulletin.updated_at)
        self.assertEqual(
            self.bulletin.scraped_at,
            self.bulletin.updated_at
        )

    def test_subsequent_updates(self):
        # Get details from original bulletin
        bulletin_id = self.bulletin.id
        orig_scraped_at = self.bulletin.scraped_at
        orig_updated_at = self.bulletin.updated_at

        # Update bulletin
        self.bulletin.location = 'New location'
        self.bulletin.save()
        updated_bulletin = Bulletin.objects.get(pk=bulletin_id)

        self.assertEqual(
            orig_scraped_at,
            updated_bulletin.scraped_at
        )
        self.assertGreater(
            updated_bulletin.updated_at,
            orig_updated_at
        )
