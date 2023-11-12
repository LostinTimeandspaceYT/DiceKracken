"""

"""

__author__ = "Nathan Winslow"
__copyright__ = "MIT"

from random import seed, randint

seed()


class Dice:

    @classmethod
    def roll(cls, num_dice: int, num_sides: int) -> int:
        result = 0
        for _ in range(num_dice):
            result += randint(1, num_sides)
        return result

    @classmethod
    def roll_multiple(cls, dice: list[tuple]) -> int:
        """
        Rolls multiple different kinds of dice.

        e.g.
        1d10 + 1d4

        :param: dice is a list of 2 element tuples (num_dice, num_sides)
        """
        result = 0
        for die in dice:
            result += cls.roll(*die)
        return result
    
class CthulhuDice(Dice):

    @classmethod
    def roll_skill(cls, bonus: int, penalty: int) -> int:  # May want to change the name
        modifier: int = abs(bonus - penalty)
        if modifier == 0:
            return randint(1, 100)  
        else:
            ones_digit = randint(0, 9)
            tens_place = [randint(0, 9) * 10,]
            for _ in range(modifier):
                tens_place.append(randint(0, 9) * 10)

            tens_place.sort()
            tens_place = list(set(tens_place))
            tens_digit = tens_place[0] if bonus > penalty else tens_place[-1]
            
            if (tens_digit + ones_digit) == 0:
                return tens_place[1] if bonus > penalty else 100
            return (tens_digit + ones_digit)
