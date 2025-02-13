import typing

from django.db import models

if typing.TYPE_CHECKING:
    from datetime import datetime
    from django.db.models.manager import Manager


class DiffRequest(models.Model):
    number: int = models.PositiveIntegerField(null=False, blank=True, db_index=True)  # Let's assume zero is allowed
    occurrences: int = models.PositiveIntegerField(default=0)
    last_datetime: 'datetime' = models.DateTimeField(auto_now=True, db_index=True)

    objects: "Manager[DiffRequest]"  # Type hint only (.objects is added via the Metadata._prepare core method)

    @property
    def value(self) -> int:
        # We don't need to run costly calculations to get the sum of squares nor the square of the sum
        # There are well known (erm... well known to chatGPT) algorithms for that. This way can can avoid
        # having to introduce complex speedup tools such as memoization, caching... we can just do a few
        # blazing fast multiplications/divisions.
        # Heck, we wouldn't even need to keep the "value" in the tables
        sum_of_squares = (self.number * (self.number + 1) * (2 * self.number + 1)) // 6
        square_of_sum = ((self.number * (self.number + 1)) // 2) ** 2
        return square_of_sum - sum_of_squares
