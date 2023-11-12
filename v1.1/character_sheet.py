"""
Module for manipulating and parsing through complex json files in
Micropython.
"""
__author__ = "Nathan Winslow"
__copyright__ = "MIT"

from json_parser import JSONParser
from random import seed, randint

    
class CthulhuCharacter:
    def __init__(self, fpath: str):
        self.character_sheet = JSONParser.load_json_file(fpath)   
        self.prev_modifier = 0
        self.db = self.damage_bonus()
        
    def __call__(self):
        return self.character_sheet
    
    def get_value_at(self, key: str):
        value = JSONParser.get_value_at_key(self.character_sheet, key)
        return value
    
    def damage_bonus(self):
        val = self.character_sheet['Characteristics']['STR'] + self.character_sheet['Characteristics']['SIZ']
        if val <= 64:
            return (1, -2)
        elif 65 <= val <= 84:
            return (1, -1)
        elif 85 <= val <= 124:
            return (0, 0)
        elif 125 <= val <= 164:
            return (4, 1) # num_of_sides, num_of_dice
        else:
            return (6, 1)

    def roll_damage(self, num_of_sides: int, num_of_dice: int) -> int:
        return ((num_of_dice * randint(1, num_of_sides)) + (self.db[1] * randint(1, self.db[0])))

    def make_skill_roll(self, bonus_die: int, penalty_die: int) -> int:
        modifier: int = abs(bonus_die - penalty_die)
        self.prev_modifier = modifier
        if modifier == 0:
            return randint(1, 100)  
        else:
            ones_digit = randint(0, 9)
            tens_place = [randint(0, 9) * 10,]
            for _ in range(modifier):
                tens_place.append(randint(0, 9) * 10)

            tens_place.sort()
            tens_place = list(set(tens_place))
            tens_digit = tens_place[0] if bonus_die > penalty_die else tens_place[-1]
            
            if (tens_digit + ones_digit) == 0:
                return tens_place[1] if bonus_die > penalty_die else 100
            return (tens_digit + ones_digit)
            
    def determine_skill_result(self, skill_val: int, roll: int):
        """
        determines the level of success of a skill roll
        and if the player can push that roll
        
        :returns: str, bool "rate of success", True if can push, False otherwise
        """
        fumble = self.get_fumble(skill_val)
        result = f"{roll} out of {skill_val}: "
        can_push = True
        if roll == 1:
            result += "Critical success!"
        
        elif roll <= (skill_val // 5):
            result += "Extreme Success!"
        
        elif roll <= (skill_val // 2):
            result += "Hard success!"
        
        elif roll <= skill_val:
            result +=  "Success!"
        
        elif skill_val < roll < fumble:
            result = "Failed."
        
        else: # roll >= fumble
            result = "Fumble..."
            can_push = False

        return result, can_push

    def get_fumble(self, skill_val):
        return 100 if skill_val >= 50 else 96
    
    def take_damage(self, amount: int):
        self.character_sheet['Characteristics']['Hit Points']['Current'] -= amount

    def lose_sanity(self, amount: int):
        self.character_sheet['Characteristics']['Sanity']['Current'] -= amount
    
    @property
    def age(self):
        return self.character_sheet['Age']
    
    @property
    def name(self):
        return self.character_sheet['Name']
    
    @property
    def pronoun(self):
        return self.character_sheet['Pronoun']
    
    @property
    def skills(self):
        return JSONParser.get_keys(self.character_sheet['Skills'])

    @property
    def current_sanity(self):
        return self.character_sheet['Characteristics']['Sanity']['Current']
    
    @property
    def current_hp(self):
        return self.character_sheet['Characteristics']['Hit Points']['Current']
    
    @property
    def current_luck(self):
        return self.character_sheet["Characteristics"]["Luck"]
        


class PulpCharacter(CthulhuCharacter):
    
    def __init__(self, fpath: str):
        super().__init__(fpath)
    
    def spend_luck(self, amount: int):
        self.character_sheet["Characteristics"]["Luck"] -= amount
       
    @property
    def talents(self):
        return JSONParser.get_keys(self.character_sheet['Pulp Talents'])
