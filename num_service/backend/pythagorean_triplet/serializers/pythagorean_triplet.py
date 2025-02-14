from rest_framework import serializers

from core.serializers import BaseNumericSerializer
from pythagorean_triplet.models import PythagoreanTriplet


class PythagoreanTripletSerializer(BaseNumericSerializer, serializers.ModelSerializer):
    triplet = serializers.DictField()   # This comes from a @property in the model

    class Meta(BaseNumericSerializer.Meta):
        model = PythagoreanTriplet
