from rest_framework import serializers

from core.serializers import BaseNumericSerializer
from squares_diff.models import SquaresDiff


class SquaresDiffSerializer(BaseNumericSerializer, serializers.ModelSerializer):
    value = serializers.IntegerField()   # This comes from a @property

    class Meta(BaseNumericSerializer.Meta):
        model = SquaresDiff
