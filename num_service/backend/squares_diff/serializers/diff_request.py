from datetime import datetime, timezone

from rest_framework import serializers

from squares_diff.models import DiffRequest


class DiffRequestSerializer(serializers.ModelSerializer):
    datetime = serializers.SerializerMethodField()  # Adds current datetime
    value = serializers.IntegerField()   # This comes from a @property

    @staticmethod
    def get_datetime(*_, **__) -> datetime:
        """Returns the current timestamp in ISO format."""
        return datetime.now(tz=timezone.utc)

    class Meta:
        model = DiffRequest
        exclude = ["id"]  # Excludes 'id', includes everything else
