from datetime import datetime, timezone

from rest_framework import serializers


class BaseNumericSerializer(serializers.Serializer):
    """Abstract serializer for numeric models, ensuring DRY principles.

    This base class is originally intended for models inheriting from 'BaseNumericModel' and should
    be useful to return common fields, such as: [number, occurrences, last_datetime, and (current) datetime].
    Subclasses (of BaseNumericModel, ideally) can extend it to add model-specific fields while inheriting
    shared behavior.
    """

    datetime = serializers.SerializerMethodField()  # Adds current datetime

    @staticmethod
    def get_datetime(*_, **__) -> datetime:
        return datetime.now(tz=timezone.utc)

    class Meta:
        abstract = True
        exclude = ["id"]  # Excludes 'id', includes everything else
        # model = BaseNumericModel  # 'model' is unused in the basic serializer.Serializer. Kept for clarity
