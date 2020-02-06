from math import ceil

from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.pagination import StandardResultsSetPagination
from bulletin.factories import BulletinFactory


class BulletinAPITestCase(APITestCase):
    """Base class for bulletin API endpoints tests."""

    @classmethod
    def setUpTestData(cls):
        cls.num_of_bulletins = 250
        cls.bulletins = BulletinFactory.create_batch(cls.num_of_bulletins)
        cls.endpoint_url = reverse('bulletin-list')

    def assert_http_status_code(self, response, code=200):
        """Helper method to check for status code."""
        codes = {
            200: status.HTTP_200_OK,
            404: status.HTTP_404_NOT_FOUND,
            405: status.HTTP_405_METHOD_NOT_ALLOWED
        }
        self.assertEqual(response.status_code, codes[code])


class BulletinListTest(BulletinAPITestCase):
    """Tests GET request on `bulletin-list` endpoint.

    This API call should return a JSON payload that includes 
    a paginated list of Bulletin objects.
    """

    def test_does_not_allow_post_request(self):
        response = self.client.post(self.endpoint_url)
        self.assert_http_status_code(response, 405)

    def test_does_not_allow_put_request(self):
        response = self.client.put(self.endpoint_url)
        self.assert_http_status_code(response, 405)

    def test_does_not_allow_delete_request(self):
        response = self.client.delete(self.endpoint_url)
        self.assert_http_status_code(response, 405)

    def test_valid_get_request(self):
        response = self.client.get(self.endpoint_url)
        payload = response.json()
        self.assert_http_status_code(response)
        self.assertIsInstance(payload, dict)
        self.assertIsInstance(payload['results'], list)
        self.assertEqual(payload['count'], self.num_of_bulletins)
        self.assertIn('previous', payload)
        self.assertIn('next', payload)


class BulletinListPaginationTest(BulletinAPITestCase):
    """Tests pagination behavior of bulletin API endpoints."""

    @classmethod
    def setUpTestData(cls):
        super(BulletinListPaginationTest, cls).setUpTestData()

        # Expected pagination stats
        cls.page_size = StandardResultsSetPagination().page_size
        cls.page_range = ceil(cls.num_of_bulletins / cls.page_size)
        cls.last_page_size = cls.num_of_bulletins % cls.page_size

    def setUp(self):
        self.response = self.client.get(self.endpoint_url)
        self.payload = self.response.json()

    def test_first_page(self):
        results = self.payload['results']
        self.assertEqual(len(results), self.page_size)
        self.assertIsNone(self.payload['previous'])
        self.assertIsNotNone(self.payload['next'])

    def test_subsequent_pages(self):
        next_page_url = self.payload['next']
        current_page_num = 2

        while next_page_url:
            response = self.client.get(next_page_url)
            payload = response.json()
            results = payload['results']
            next_page_url = payload['next']

            self.assert_http_status_code(response)
            if current_page_num < self.page_range:  # middle pages
                self.assertEqual(len(results), self.page_size)
                self.assertIsNotNone(payload['previous'])
                self.assertIsNotNone(payload['next'])
                current_page_num += 1
            elif current_page_num == self.page_range:   # last page
                self.assertEqual(len(results), self.last_page_size)
                self.assertIsNotNone(payload['previous'])
                self.assertIsNone(payload['next'])

        self.assertEqual(current_page_num, self.page_range)
