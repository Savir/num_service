from rest_framework import serializers

from core.serializers import BaseNumericSerializer
from pythagorean_triplet.models import PythagoreanTriplet


class PythagoreanTripletSerializer(BaseNumericSerializer):
    triplet = serializers.DictField()   # This comes from a @property

    class Meta(BaseNumericSerializer.Meta):
        model = PythagoreanTriplet
