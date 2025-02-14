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
        # It may seem a bit silly extrapolating something this simple into a method, but that way we can
        # use it safely in the test suite
        return f"{cls.__name__}_{number}"

    @property
    def triplet(self) -> dict[str, int] | None:
        """Finds a Pythagorean triplet (a, b, c) such that a * b * c = self.number,
        using an optimized approach... thanks to ChatGPT. It knows a lot!
        You can double-check what ChatGPT suggested in the following link:
           https://en.wikipedia.org/wiki/Pythagorean_triple#Geometry_of_Euclid's_formula
        That thing knows quite a bit!
        """
        cache_key = self.generate_cache_key(self.number)
        if cache.has_key(cache_key):
            # Need to check whether we have the key because it could be None. Which
            # means: Just checking "if cache.get(cache_key):" and assuming that if we
            # get a 'None' that means that we haven't cached the value won't be a good
            # enough check (it could be None because we tried to calculate but didn't
            # find a suitable triplet).
            return cache.get(cache_key)

        # If we're here, we need to calculate the triplet because is not cached
        limit = isqrt(self.number)
        for m in range(2, limit):
            for n in range(1, m):
                if gcd(m, n) != 1 or (m - n) % 2 == 0:
                    continue

                a = m**2 - n**2
                b = 2 * m * n
                c = m**2 + n**2

                if c > 1_000:
                    # Customer said they didn't want c(s) > 1000 so...
                    continue

                product = a * b * c
                if product == self.number:
                    triplet = {"a": a, "b": b, "c": c}
                    # Cache and return to stop looking
                    cache.set(cache_key, triplet, timeout=3600)
                    return triplet

        cache.set(cache_key, None, timeout=3600)  # Cache for one hour. The fact the cache_key exists (even
        # though its value is None) means we tried to find the triplet and it doesn't exist.
        return None
