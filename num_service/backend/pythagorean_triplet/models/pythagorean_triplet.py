import typing
from math import gcd, isqrt

from django.core.cache import cache

from core.models import BaseNumericModel

if typing.TYPE_CHECKING:
    from django.db.models.manager import Manager


class PythagoreanTriplet(BaseNumericModel):
    objects: "Manager[PythagoreanTriplet]"  # Type hint only (.objects is added in the Metadata._prepare method)

    @classmethod
    def generate_cache_key(cls, number) -> str:
        # It may seem a bit dumb extrapolating this into a method, but it will be
        # used in the test suite so... there!
        return f"{cls.__name__}_{number}"

    @property
    def triplet(self) -> dict[str, int] | None:
        """Finds a Pythagorean triplet (a, b, c) such that a * b * c = number,
        using an optimized approach thanks to ChatGPT.
        See: https://en.wikipedia.org/wiki/Pythagorean_triple#Geometry_of_Euclid's_formula
        """
        cache_key = self.generate_cache_key(self.number)
        if cache.has_key(cache_key):
            # Need to check whether we have the key because it could be None (which
            # means: Just checking "if cache.get(cache_key):" and assuming that if we
            # get a 'None' that means that we haven't cached the value won't be a good
            # a enough check.
            return cache.get(cache_key)

        # If we're here, we need to calculate the triplet because is not cached
        limit = isqrt(self.number)
        for m in range(2, limit):
            for n_ in range(1, m):
                if gcd(m, n_) != 1 or (m - n_) % 2 == 0:
                    continue

                a = m**2 - n_**2
                b = 2 * m * n_
                c = m**2 + n_**2

                if c > 1_000:
                    # Customer said they didn't want c(s) > 1000 so...
                    continue

                product = a * b * c
                if product == self.number:
                    triplet = {"a": a, "b": b, "c": c}
                    # Cache and return to stop looking
                    cache.set(cache_key, triplet, timeout=3600)
                    return triplet

        cache.set(cache_key, None, timeout=3600)  # Cache for one hour
        return None
