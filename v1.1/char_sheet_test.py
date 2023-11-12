"""
Module for testing future character sheet classes.
"""
__author__ = "Nathan Winslow"
__copyright__ = "MIT"

from character_sheet import PulpCharacter
        
# Test values        
example_character = 'pulp_cthulhu_sheet.json'
my_character = PulpCharacter(example_character)
test_key = 'Latin'


def print_skills_test(skill_list):
    print('\n----------- Skill List -----------')
    for skill in skill_list:
        print(skill)


print(f"{my_character.name}({my_character.pronoun}), {my_character.age}")
print(f"{test_key}: {my_character.get_value_at(test_key)}")

