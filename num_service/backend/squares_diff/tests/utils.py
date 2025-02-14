import math


def manual_square_diff_calc(number):
    """
    A straightforward but slower alternative to our Model's .value @property  for calculating the
    difference between the square of the sum of all numbers  and the sum of their squares.

    This function is used to verify the correctness of the more advanced method implemented
    in our model.
    """
    sum_of_squares = sum(math.pow(n, 2) for n in range(1, number + 1))
    square_of_sum = math.pow(sum(range(1, number + 1)), 2)
    return square_of_sum - sum_of_squares
