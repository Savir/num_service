import math


def manual_square_diff_calc(number):
    sum_of_squares = sum(math.pow(n, 2) for n in range(1, number + 1))
    square_of_sum = math.pow(sum(range(1, number + 1)), 2)
    return  square_of_sum - sum_of_squares
