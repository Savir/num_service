import typing

from django.db import models

if typing.TYPE_CHECKING:
    from datetime import datetime


class BaseNumericModel(models.Model):
    """Abstract base model for shared models across the apps provided by the 'num_service'... erm... service"""
    number: int = models.PositiveIntegerField(null=False, blank=True, db_index=True, unique=True)
    occurrences: int = models.PositiveIntegerField(default=0)
    last_datetime: "datetime" = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
