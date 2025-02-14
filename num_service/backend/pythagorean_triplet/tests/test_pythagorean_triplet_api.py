from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from pythagorean_triplet.models import PythagoreanTriplet


class PythagoreanTripletAPITest(APITestCase):
    def test_foundable_triplets(self):
        """Test that the triplets are correctly found/calculated using a few known pythagorean triplets"""
        # TODO: Parametrize nicely using pytest
        test_cases = [
            {"a": 3, "b": 4, "c": 5},
            {"a": 209, "b": 120, "c": 241},
            {"a": 231, "b": 160, "c": 281},
            {"a": 597, "b": 796, "c": 995},
        ]
        # We know those are valid pythagorean triples.
        # Our "number" (the parameter sent to the API) is the product of them. We can use that fact to generate
        # said "number".
        for test_case in test_cases:
            number = test_case["a"] * test_case["b"] * test_case["c"]
            response = self.client.get(f"/pythagorean?number={number}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["triplet"]["a"], test_case["a"])
            self.assertEqual(response.data["triplet"]["b"], test_case["b"])
            self.assertEqual(response.data["triplet"]["c"], test_case["c"])

    def test_unfoundable_triplets(self):
        """Test that for numbers that we know don't have valid triplets, we will get None as triplet value"""
        number = 100
        response = self.client.get(f"/pythagorean?number={number}")
        self.assertEqual(response.data["triplet"], None)

    def test_no_number(self):
        """Make sure if we don't provide a number we will get a malformed request error"""
        response = self.client.get(f"/pythagorean")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_numbers(self):
        """Test API rejects invalid numbers"""
        number = -10
        response = self.client.get(f"/difference?number={number}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_caching_yes_triplet(self):
        """Ensure the cache works when a triplet can be calculated"""
        number = 4200
        cache_key = PythagoreanTriplet.generate_cache_key(number)
        assert not cache.has_key(cache_key)
        self.client.get(f"/pythagorean?number={number}")
        assert cache.has_key(cache_key)
        cached_triplet = cache.get(cache_key)
        assert cached_triplet["a"] == 7 and cached_triplet["b"] == 24 and cached_triplet["c"] == 25

    def test_caching_no_triplet(self):
        """Ensure the cache works when a triplet can NOT be calculated"""
        number = 10
        cache_key = PythagoreanTriplet.generate_cache_key(number)
        assert not cache.has_key(cache_key)
        self.client.get(f"/pythagorean?number={number}")
        assert cache.has_key(cache_key)
        cached_triplet = cache.get(cache_key)
        assert cached_triplet is None
