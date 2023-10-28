"""
Module for testing future character sheet classes.
"""
__author__ = "Nathan Winslow"
__copyright__ = "MIT"

from character_sheet import CharacterSheet
        
# Test values        
example_character = 'pulp_cthulhu_sheet.json'
my_character = CharacterSheet(example_character)
test_key = 'CON'

print(f"{my_character.name}({my_character.pronoun}), {my_character.age}")
print(f"{test_key} score: {my_character.get_value_at(test_key)}")
print('\n----------- Skill List -----------')
for skill in my_character.skills:
    print(skill)
