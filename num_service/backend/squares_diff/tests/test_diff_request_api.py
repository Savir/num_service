from rest_framework import status
from rest_framework.test import APITestCase

from squares_diff.models.diff_request import DiffRequest
from squares_diff.tests import utils as test_utils


class DifferenceAPITest(APITestCase):

    def test_valid_number(self):
        """Test API returns correct response for a valid number"""
        number = 10
        response = self.client.get(f"/difference?number={number}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number"], number)
        self.assertEqual(response.data["value"], test_utils.manual_square_diff_calc(number))

    def test_invalid_number(self):
        """Test API rejects invalid numbers"""
        number = 500
        response = self.client.get(f"/difference?number={number}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_occurrences_increment(self):
        """Test occurrences field increments correctly"""
        num_requests = 5
        number = 28
        for i in range(num_requests):
            self.client.get(f"/difference?number={number}")
        obj = DiffRequest.objects.get(number=number)
        self.assertEqual(obj.occurrences, num_requests)

    def test_db_value(self):
        """Test that the obj.value gets stored properly"""
        number = 5
        self.client.get(f"/difference?number={number}")
        obj = DiffRequest.objects.get(number=number)
        self.assertEqual(obj.value, test_utils.manual_square_diff_calc(number))