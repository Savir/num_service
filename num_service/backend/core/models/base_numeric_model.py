import typing

from django.db import models

if typing.TYPE_CHECKING:
    from datetime import datetime


class BaseNumericModel(models.Model):
    """Abstract base model for shared models across the apps provided by the 'num_service'... erm... service"""

    number: int = models.PositiveIntegerField(
        null=False,
        blank=True,
        db_index=True,
        unique=True,
        db_comment="A unique positive integer representing the primary numeric "
        'value our endpoints will calculate "things" for. This is the core of our numeric services.',
    )
    occurrences: int = models.PositiveIntegerField(
        null=False,
        default=0,
        db_comment="Tracks how many times this number has been used or requested.",
    )

    # TODO: Note that the auto_now=True in the 'last_datetime' below will always store the time when this row
    #       was last updated (saved). It will NOT (!) keep a reference to the previous "current_datetime". If
    #       that's not the desired behavior, we should remove the auto_now=True and add some logic in the View
    #       handlers to fetch the .datetime attribute from the serialized data and set it as this .last_datetime
    #       field rather than discharge that responsibility into Django.
    #       Otherwise said: With this setup, response.datetime != next_response.last_datetime (just by a few
    #       nanoseconds, but they WILL be different)
    last_datetime: "datetime" = models.DateTimeField(
        auto_now=True,
        null=False,
        db_comment="Auto-updated timestamp indicating the last time this entry was modified. It will"
        " de-facto correspond with the time of the last request, since every time we get a request,"
        " the 'occurrences' field gets updated",
    )

    class Meta:
        abstract = True
