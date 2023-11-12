"""
Module for manipulating and parsing through complex json files in
Micropython.
"""
__author__ = "Nathan Winslow"
__copyright__ = "MIT"

import json
from collections import OrderedDict
from random import seed, randint

class JsonParser:
    """
    For when we must parse and sort
    complex json files ourselves.
    """
    @classmethod
    def load_json_file(cls, fpath: str):
        json_str = ""
        with open(fpath,'r') as file:
            for entry in file:
                json_str += entry
        tmp_file = json.loads(json_str)
        return cls.sort_json_file(tmp_file)

    @classmethod
    def sort_json_file(cls, d: dict):
        sorted_file = OrderedDict(sorted(d.items()))
        for k, v in sorted_file.items():
            if isinstance(v, dict):
                sorted_dict = cls.sort_json_file(v)
                sorted_file.update({k : sorted_dict})
        return sorted_file

    @classmethod
    def pretty_print_keys(cls, d: dict, indent=0, ret_str=''):
        """
        Helper for nested dictionary keys to screens.
        
        The default behavior is indent subentries by 2 spaces
        per depth level.
        
        ex.
            Language
              English
              French
                
            Weapons
              Firearms
                Pistol
                  .45 Automatic
                Shotgun
        """
        for k, v in d.items():
            ret_str = '  ' * indent + str(k)
            yield ret_str
            if isinstance(v, dict):
                yield from cls.pretty_print_keys(v, indent + 1)
               
    @classmethod
    def get_all_vals(cls, d: dict):
        for v in d.values():
            if isinstance(v, dict):
                yield from cls.get_all_vals(v)
            else:
                yield v
    
    @classmethod
    def get_keys(cls, d: dict) -> list[str]:
        keys = []
        for key in cls.pretty_print_keys(d):
            keys.append(key)
        return keys
    
    @classmethod
    def get_vals(cls, d: dict) -> list:
        vals = []
        for value in cls.get_all_vals(d):
            vals.append(value)
        return vals
    
    @classmethod
    def get_value_at_key(cls, d: dict, key: str):
        if key in d:
            return d[key]
        
        for v in d.values():
            if isinstance(v, dict):
                value = cls.get_value_at_key(v, key)
                if value is not None:  # the value could be 0, which we do want to return
                    return value
    
class CthulhuCharacter:
    def __init__(self, fpath: str):
        self.character_sheet = JsonParser.load_json_file(fpath)   
        self.prev_modifier = 0
        self.db = self.damage_bonus()
        
    def __call__(self):
        return self.character_sheet
    
    def get_value_at(self, key: str):
        value = JsonParser.get_value_at_key(self.character_sheet, key)
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
        return JsonParser.get_keys(self.character_sheet['Skills'])

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
        return JsonParser.get_keys(self.character_sheet['Pulp Talents'])
