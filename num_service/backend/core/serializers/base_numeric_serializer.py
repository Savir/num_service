from datetime import datetime, timezone

from rest_framework import serializers


class BaseNumericSerializer(serializers.ModelSerializer):
    datetime = serializers.SerializerMethodField()  # Adds current datetime

    @staticmethod
    def get_datetime(*_, **__) -> datetime:
        """Returns the current timestamp in ISO format."""
        return datetime.now(tz=timezone.utc)

    class Meta:
        abstract = True
        exclude = ["id"]  # Excludes 'id', includes everything else
