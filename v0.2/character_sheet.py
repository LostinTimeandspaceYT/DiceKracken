"""
Module for Character sheet manipulation 
"""
__author__ = "Nathan Winslow"
__copyright__ = "MIT"

from json_parser import JSONParser
from dice import CthulhuDice

class PlayerCharacter:
    def __init__(self, fpath: str):
        self.character_sheet = JSONParser.load_json_file(fpath)

    def __call__(self):
        return self.character_sheet
    
    def get_value_at(self, key: str):
        return JSONParser.get_value_at_key(self.character_sheet, key)
        
    @property
    def age(self):
        return self.character_sheet['Age']
    
    @property
    def name(self):
        return self.character_sheet['Name']
    

class CthulhuCharacter(PlayerCharacter):

    def __init__(self, fpath: str):
        super().__init__(fpath)  
        self.prev_skill_modifier: int = 0  # used when pushing rolls.
        self.current_weapon: dict = {}
        self.db: tuple = self.damage_bonus()
        self.skills_to_improve: list[str] = []  # Used during Development phase
    
    def damage_bonus(self) -> tuple:
        """ Returns a tuple (num_dice, num_side) such that -2 and -1 are const"""
        val = self.character_sheet['Characteristics']['STR'] + self.character_sheet['Characteristics']['SIZ']
        if val <= 64:
            return (-2, 1) 
        elif 65 <= val <= 84:
            return (-1, 1)
        elif 85 <= val <= 124:
            return (0, 0)
        elif 125 <= val <= 164:
            return (1, 4) 
        else:
            return (1, 6)

    def roll_damage(self, dmg_die: tuple) -> int:
        if self.db[0] == 0:
            return CthulhuDice.roll(*dmg_die)
        else:  # to prevent empty range
            return CthulhuDice.roll_multiple([dmg_die, self.db])

    def cast_spell(self, spell_name: str):
        print(f"Casting {spell_name}!")
        # TODO: Flesh out spell logic

    def roll_skill(self, bonus_die: int, penalty_die: int):
        return CthulhuDice.roll_skill(bonus_die, penalty_die)

    def get_skill_at_difficulty(self, skill_val: int, level: str) -> int:
        if level == "Hard":
            return skill_val // 2
        elif level == "Extreme":
            return skill_val // 5
        else:
            return skill_val

    def get_fumble(self, skill_val):
        return 100 if skill_val >= 50 else 96
    
    def change_hit_points(self, amount: int):
        """
        For regaining hit points, pass in a
        positive integer.
        For taking damage, pass in a negative
        integer.
        """
        self.character_sheet['Characteristics']['Hit Points']['Current'] += amount

    def change_magic_points(self, amount: int):
        """ same behavior as change_hit_points """
        self.character_sheet['Characteristics']['Magic Points']['Current'] += amount
    
    def change_sanity(self, amount: int):
        """ same behavior as change_hit_points """
        self.character_sheet['Characteristics']['Sanity']['Current'] += amount
    
    def get_weapon_names(self):
        w_names = []
        for i in range(1, len(self.weapons) + 1):
            w_names.append(self.weapons[f"Weapon {i}"]["Name"])
        return w_names

    def set_current_weapon(self, selection: int):
        self.current_weapon = self.weapons[f"Weapon {selection}"]

    @property
    def pronoun(self):
        return self.character_sheet['Pronoun']
    
    @property
    def skills(self):
        return JSONParser.get_keys(self.character_sheet['Skills'])

    @property 
    def weapons(self):
        return self.character_sheet["Combat"]["Weapons"]

    @property
    def current_sanity(self):
        return self.character_sheet['Characteristics']['Sanity']['Current']
    
    @property
    def current_hp(self):
        return self.character_sheet['Characteristics']['Hit Points']['Current']
    
    @property
    def current_mp(self):
        return self.character_sheet['Characteristics']['Magic Points']['Current']
    
    @property
    def current_luck(self):
        return self.character_sheet["Characteristics"]["Luck"]
    
        
class PulpCharacter(CthulhuCharacter):

    def __init__(self, fpath: str):
        super().__init__(fpath)
    
    # Modifiers
    def change_luck(self, amount: int):
        """ similar to other change methods """
        self.character_sheet["Characteristics"]["Luck"] += amount
    
    @property
    def archetype(self):
        return self.character_sheet["Archetype"]   
    
    @property
    def talents(self):
        return JSONParser.get_keys(self.character_sheet['Pulp Talents'])
    

