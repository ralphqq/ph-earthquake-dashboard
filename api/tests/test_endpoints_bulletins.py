from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.pagination import StandardResultsSetPagination
from bulletin.factories import BulletinFactory


class BulletinListTest(APITestCase):
    """Tests GET request on `bulletin-list` endpoint.

    This API call should return a JSON payload that includes 
    a paginated list of Bulletin objects.
    """

    @classmethod
    def setUpTestData(cls):
        cls.num_of_bulletins = 350
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
