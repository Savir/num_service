import typing

from core.models import BaseNumericModel

if typing.TYPE_CHECKING:
    from django.db.models.manager import Manager


class SquaresDiff(BaseNumericModel):
    """
    Model to calculate difference between sum of squares and the square of sum.
    When this comment was written, it was here solely to be able to provide a .value property that
    would to the requested calculations which could then be serialized in a REST response
    Example:
        The sum of the squares of the first ten natural numbers is:
            1^2 + 2^2 + ... + 10^2 = 385
        The square of the sum of the first ten natural numbers is:
            (1 + 2 + ... + 10)^2 = 552 = 3025
        Hence the difference between the sum of the squares of the first ten natural numbers and the square
        of the sum is 3025 − 385 = 2640.
    """

    objects: "Manager[SquaresDiff]"  # Type hint only (.objects is added via the Metadata._prepare method)

    @property
    def value(self) -> int:
        # We don't need to run costly calculations to get the sum of squares nor the square of the sum
        # There are well known (erm... well known to chatGPT) algorithms for that. This way can can avoid
        # having to introduce complex speedup tools such as memoization, caching... we can just do a few
        # blazing fast multiplications/divisions.
        # Here's some more detail:
        #   sum of squares: https://www.geeksforgeeks.org/sum-of-squares/#sum-of-squares-for-n-natural-numbers
        #   sum of N natural numbers (not squared): https://en.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_%E2%8B%AF
        sum_of_squares = (self.number * (self.number + 1) * (2 * self.number + 1)) // 6
        square_of_sum = ((self.number * (self.number + 1)) // 2) ** 2
        return square_of_sum - sum_of_squares
