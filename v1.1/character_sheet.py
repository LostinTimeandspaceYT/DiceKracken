"""
Module for manipulating and parsing through complex json files in
Micropython.
"""
__author__ = "Nathan Winslow"
__copyright__ = "MIT"

import json
from collections import OrderedDict


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
        return 'Null'
    

class CharacterSheet:
    """
    Base class for all character sheets in the future.
    """
    
    def __init__(self, fpath: str):
        self.character_sheet = JsonParser.load_json_file(fpath)     
        
    def __call__(self):
        return self.character_sheet
    
    def get_value_at(self, key: str):
        value = JsonParser.get_value_at_key(self.character_sheet, key)
        return value
    
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
        
