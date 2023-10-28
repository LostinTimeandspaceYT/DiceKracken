import json
from collections import OrderedDict

# Examples
example_pulp_character = 'pulp_cthulhu_sheet.json'


class CharacterSheetParser:  #TODO: find a way to get values recursively
    """
    Helper Class for Character Sheets.
    As of v1.2.1 MicroPython's json library
    does not have a ``sort_keys`` kwarg, so
    we must parse and sort the keys ourselves.
    """
    
    def load_character_sheet(fpath: str):
        character_str = ""
        with open(fpath,'r') as sheet:
            for entry in sheet:
                character_str += entry
        tmp_sheet = json.loads(character_str)
        return CharacterSheetParser.sort_character_sheet(tmp_sheet)


    def sort_character_sheet(sheet: dict):
        sorted_sheet = OrderedDict(sorted(sheet.items()))
        for k, v in sorted_sheet.items():
            if isinstance(v, dict):
                sorted_dict = CharacterSheetParser.sort_character_sheet(v)
                sorted_sheet.update({k : sorted_dict})
        return sorted_sheet


    def pretty_print_dict(d: dict, indent=0, ret_str=''):
        """
        Helper for printing skills, attributes, gear, etc.
        to screens
        
        the default behavior is indent subentries by 2 spaces
        per depth level.
        
        ex.
            skill_1
              sub_skill_1
                sub_sub_skill_1
                
            skill_2
        """
        for k, v in d.items():
            ret_str = '  ' * indent + str(k)
            yield ret_str
            if isinstance(v, dict):
               yield from CharacterSheetParser.pretty_print_dict(v, indent + 1)
    
    def get_keys(d: dict) -> list[str]:
        keys = []
        for key in CharacterSheetParser.pretty_print_dict(d):
            keys.append(key)
        return keys
    
    def get_vals(d: dict) -> list:
        vals = []
        for k, value in d.items():
            vals.append(value)
        return vals
    
    def get_value_at_key(d, key: str):
        if key in d:
            return d[key]
        for v in d.values():
            if isinstance(v, dict):
                return CharacterSheetParser.get_value_at_key(v, key)
    

class CharacterSheet:
    
    def __init__(self, fpath: str):
        self.character_sheet = CharacterSheetParser.load_character_sheet(fpath)
        self.skills_list = CharacterSheetParser.get_keys(self.character_sheet['Skills'])
        s
        
    def __call__(self):
        return self.character_sheet
    
    @property
    def skills(self):
        return self.skills_list
        
