import json
from collections import OrderedDict


character_str = ""
with open('pulp_cthulhu_sheet.json','r') as sheet:
    for entry in sheet:
        character_str += entry
json_sheet = json.loads(character_str)

def get_all_keys(d):
    for k, v in d.items():
        yield k
        if isinstance(v, dict):
            yield from get_all_keys(v)
    
def sort_character_sheet(sheet):
    sorted_sheet = OrderedDict(sorted(sheet.items()))
    for k, v in sorted_sheet.items():
        if isinstance(v, dict):
            sorted_dict = sort_character_sheet(v)
            sorted_sheet.update({k : sorted_dict})
    return sorted_sheet
            
def pretty_print_dict(d, indent=0, ret_str=''):
    for k, v in d.items():
        ret_str = '  ' * indent + str(k)
        yield ret_str
        if isinstance(v, dict):
           yield from pretty_print_dict(v, indent + 1)
        else:
            # print('  ' * (indent + 1) + str(v))
            pass

def select_skill_menu(list_of_stuff):
    usr_input = 'w'
    current = 1
    max_len = len(list_of_stuff)
    while usr_input != 'q':
        print(">:", list_of_stuff[current - 1])
        print("  ",list_of_stuff[current])
        
        usr_input = input()
        if usr_input == 'w':
            current -= 1
        elif usr_input == 's':
            current += 1

        if current >= max_len or current < 1:
            current = 1

skills = []
character_sheet = sort_character_sheet(json_sheet)
for skill in (pretty_print_dict(character_sheet['Skills'])):
    # print(skill)
    skills.append(skill)
    
    
select_skill_menu(skills)
 