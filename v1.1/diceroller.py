"""
This program is intended to determine results of a d100 for Call of Cthulhu
and other BRP RPGs.
"""

__author__ = "Nathan Winslow"
__copyright__ = "MIT"

import random

random.seed()


def get_fumble(skill_val):
    return 100 if skill_val >= 50 else 95


class Die(object):

    def __init__(self, skill_val):
        self.fumble = get_fumble(skill_val)
        self.skill_val = skill_val
        self.hard_suc = skill_val // 2
        self.extreme_suc = skill_val // 5
        self.last_result = 0

    def __call__(self, bonus_die: int, penalty_die: int):

        modifier = abs(bonus_die - penalty_die)

        if modifier != 0:

            ones_digit = random.randint(0, 9)
            tens_digit = [random.randint(0, 9) * 10]

            i = 0
            while i < modifier:
                tens = random.randint(0, 9) * 10
                tens_digit.append(tens)
                i += 1

            tens_digit.sort()
            tens_digit = list(set(tens_digit))
            high = 0

            if bonus_die > penalty_die:
                high = tens_digit[0]

            elif penalty_die > bonus_die:
                high = tens_digit[-1]

            result = high + ones_digit
            if result == 0 and penalty > bonus:
                result = 100

            # so the user gets the lowest possible value.
            elif result == 0 and bonus_die > penalty_die:
                result += tens_digit[1]

        else:
            result = random.randint(1, 100)

        self.last_result = result
        return result
