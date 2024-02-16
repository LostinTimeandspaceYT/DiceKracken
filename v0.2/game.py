"""
This module defines the game logic 
"""

from time import sleep
from character_sheet import CthulhuCharacter, PulpCharacter
from kpc import KeypadController, Color
from I2C_LCD import I2cLcd
import json

supported_games = [
    "Call of Cthulhu",
    "Pulp Cthulhu",
]

def get_game(selected_game: str):

    if selected_game == supported_games[0]:
        return CthulhuGame
    
    elif selected_game == supported_games[1]:
        return PulpCthulhuGame
    
    else:
        raise ValueError
    

def get_character_sheet() -> str:
    return "pulp_cthulhu_sheet.json"

class GameFactory():

    @classmethod
    def create_game(cls, keypad: KeypadController, lcd: I2cLcd, selected_game: str):
        file_path = get_character_sheet()
        game = get_game(selected_game)
        return game(keypad, lcd, file_path)
    

class Game():
    """
    Interface to game logic
    
    TODO: Create menu scrolling in class to help with long menus
    
    """
    def __init__(self, keypad: KeypadController, lcd: I2cLcd):
        self.keypad = keypad
        self.lcd = lcd
        self.game_menu = {}
        self.running = True
    
    def loop(self):
        raise NotImplementedError

    def reset_lcd(self):
        self.lcd.clear()
        self.lcd.blink_cursor_off()

    def populate_game_menu(self):
        """
        Interface to create a menu for your game
        
        {'game option': function to handle option}
    
        example:
            {"make skill roll': self.investigator.make_skill_roll}
        """
        raise NotImplementedError
    
    def quit(self):
        self.running = False
        
    def select_option(self, options: list[str]) -> int:
        """
        Helper method for print a short list of items to the user to select from.
        """
        self.reset_lcd()
        i = 0
        keypress = -1
        for option in options:
            self.lcd.putstr(f"{i}: {option} \n")
            i += 1
        keypress = self.keypad.get_button_press()
        while keypress >= i:
            self.reset_lcd()
            self.lcd.putstr("Press a valid key. \n")
            sleep(1.5)
            self.reset_lcd()
            for j in range(options):
                self.lcd.putstr(f"{j}: {options[j]} \n")
            keypress = self.keypad.get_button_press()
        return keypress
            
    
    def select_from_list_menu(self, list_of_stuff: list[str]) -> str:
        """
        Helper method for printing lists of things
        users may want to select from

        the intention is to use this method to get a key 
        which is then passed into another method to get a value.
        :return: str 
        """  
        keypress = 0
        self.lcd.hide_cursor()
        current = 0
        cursor_index = 0
        max_len = len(list_of_stuff)
        num_lines = self.lcd.num_lines
        
        while keypress != self.keypad.ACCEPT:
            for i in range(min(self.lcd.num_lines, max_len)):
                if i == cursor_index:
                    msg = '>:' 
                else:
                    msg = '  '
                    
                msg += list_of_stuff[current + i] + '\n'
                self.lcd.putstr(msg)

            keypress = self.keypad.get_button_press()
            
            # Figure out how far down does the user want to scroll
            if keypress == self.keypad.UP_MENU:
                cursor_index -= 1
                
            elif keypress == self.keypad.DOWN_MENU:
                cursor_index += 1

            elif keypress == self.keypad.PAGE_UP:
                cursor_index -= num_lines

            elif keypress == self.keypad.PAGE_DOWN:
                cursor_index += num_lines
            
            # If they reach the bounds of the screen
            if cursor_index >= num_lines:
                cursor_index = 0 # we may want to set to num_lines - 1
                current += (num_lines - 1)
                self.lcd.clear()
                
            elif cursor_index < 0:
                cursor_index = num_lines - 1 # and this to 0 depending on desired behavior
                current -= (num_lines - 1)
                self.lcd.clear()
                
            if (current + (num_lines - 1)) >= max_len or current < 0:
                current = 0
                
            sleep(.1) 
            
        return list_of_stuff[cursor_index + current].lstrip()  
    
    def get_number(self):
        """
        gets a number from the user via keypad entry.
        blocking function.
        :return: int from user input
        """
        test_str = ""
        keypress = None
        self.lcd.blink_cursor_on()
        first = True
        prev_press = -1
        while keypress != self.keypad.ACCEPT:
            keypress = self.keypad.get_button_press()

            if 0 <= keypress <= 9:
                usr_in = str(keypress)
                self.lcd.putchar(usr_in)
                test_str += usr_in   
                if first:
                    self.keypad.light_button(keypress, Color.pink)
                    first = False
                else:
                    self.keypad.light_button(keypress, Color.blue)
                prev_press = keypress

            if keypress == self.keypad.BACKSPACE:
                if first:
                    self.keypad.light_button(int(test_str), Color.black)
                else:
                    self.keypad.light_button(int(usr_in), Color.black)  # We are bounded to 16 Python!!!
                    first = True
                    
                test_str = test_str[:-1] 
                if self.lcd.cursor_x > 7:  #TODO: we may need to change this 
                    self.lcd.cursor_x -= 1
                    self.lcd.move_to(self.lcd.cursor_x, self.lcd.cursor_y)
                    self.lcd.putchar(' ')
                    self.lcd.cursor_x -= 1
                    self.lcd.move_to(self.lcd.cursor_x, self.lcd.cursor_y)

        self.lcd.blink_cursor_off()
        self.keypad.reset_number_buttons()
        return int(test_str) if test_str != "" else 0

    def get_yes_no(self):
        """
        gets a yes or no answer from the user via keypad entry.
        blocking function.
        """
        keypress = 0
        self.lcd.hide_cursor()
        while keypress != self.keypad.ACCEPT and keypress != self.keypad.BACKSPACE:

            keypress = self.keypad.get_button_press()

            if keypress == self.keypad.ACCEPT:
                return True
            
            elif keypress == self.keypad.BACKSPACE:
                return False
            
            else:
                self.lcd.putstr("Press a valid key")
                sleep(1.5)
                self.lcd.clear()


class CthulhuGame(Game):
    """
    TODO: 
    Create a means for a user to select a weapon. 

    """
    def __init__(self, keypad: KeypadController, lcd: I2cLcd, fpath: str):
        super().__init__(keypad, lcd)
        self.investigator = CthulhuCharacter(fpath)
        self.difficulty_levels = [
            "Normal",
            "Hard",
            "Extreme"
        ]
        self.populate_game_menu()

    def populate_game_menu(self):
        self.game_menu = { 
            "Make a skill roll" : self.make_skill_roll,
            "Change Hit Points": self.change_hit_points,
            "Change Sanity" : self.change_sanity,
            "Quit"			: self.quit,
            "Select Weapon" : self.select_weapon,
            "Roll Damage" : self.roll_damage
        }
        
    def loop(self):
        options = []
        for k,v in self.game_menu.items():
            options.append(k)

        self.reset_lcd()
        while self.running:
            selected = self.select_from_list_menu(options)
            self.reset_lcd()
            self.game_menu[selected]()

    def determine_result(self, roll: int,  skill_val: int, fumble: int, difficulty: str) -> bool:
        msg = ""
        failed = False
        if roll == 1:
            msg = "\nCritical success!"
            self.keypad.light_buttons(16, Color.white)

        elif roll <= skill_val:
            msg = f"{difficulty} success!"

            if difficulty == "Normal":
                self.keypad.light_buttons(16, Color.green)

            elif difficulty == "Hard":
                self.keypad.light_buttons(16, Color.lt_blue)

            else:  # Extreme
                self.keypad.light_buttons(16, Color.yellow)


        elif roll > skill_val and roll < fumble:
            msg = "\nFailure."
            self.keypad.light_buttons(16, Color.purple)
            failed = True

        elif roll >= fumble:
            msg = "\nFumble..."
            self.keypad.light_buttons(16, Color.red)
            failed = True

        self.lcd.putstr("Result: " + str(roll) + '\n' + msg)
        sleep(3.5)
        self.keypad.default_layout()
        self.reset_lcd()
        return failed
    
    def make_skill_roll(self):
        skill = self.select_from_list_menu(self.investigator.skills)
        diff_level = self.select_option(self.difficulty_levels)
        
        val = self.investigator.get_value_at(skill)
        if isinstance(val, int):
            self.reset_lcd()
            self.lcd.putstr("Any modifiers?\n")
            if self.get_yes_no():
                self.lcd.clear()
                self.lcd.putstr("Num of bonus \ndice:")
                bonus = self.get_number()
                self.lcd.clear()
                self.lcd.putstr("Num of penalty \ndice:")
                penalty = self.get_number()
            else:
                bonus = 0
                penalty = 0

            self.lcd.clear()

            roll = self.investigator.roll_skill(bonus, penalty)
            skill_val_at = self.investigator.get_skill_at_difficulty(val, self.difficulty_levels[diff_level])
            fumble = self.investigator.get_fumble(val)
            failed = self.determine_result(roll, skill_val_at, fumble, self.difficulty_levels[diff_level])
            if failed and roll < fumble:
                self.lcd.putstr("Push the roll? \n")
                push = self.get_yes_no()
                
                if push:
                    self.reset_lcd()
                    roll = self.investigator.roll_skill(bonus, penalty)
                    failed_push = self.determine_result(roll, skill_val_at, fumble, self.difficulty_levels[diff_level])
                    if failed_push:
                        self.lcd.putstr("Failing pushed\nrolls is bad!")
                        sleep(2)
                        self.reset_lcd()
        else:
            raise TypeError("Selected Skill does not have a value associated with it.")
        
    def change_hit_points(self):
        self.lcd.putstr("Taking Damage?\n")
        damaged = self.get_yes_no()
        amt = self.get_number()
        if damaged:
            amt = -amt

        self.investigator.change_hit_points(amt)    

    def change_sanity(self):
        self.lcd.putstr("Losing Sanity?\n")
        answer = self.get_yes_no()
        self.reset_lcd()
        self.lcd.putstr("How much damage? \n")
        amt = self.get_number()
        if answer: 
            amt = -amt
    
        self.investigator.change_sanity(amt)

    def roll_damage(self):  #TODO: Create means to grab damage die from weapon
        self.lcd.putstr("Rolling Damage\n")
        damage = self.investigator.roll_damage((1,6))
        sleep(1.5)
        self.lcd.reset_lcd()
        self.lcd.putsr(f"You deal {damage} damage")

    def select_weapon(self):
        self.lcd.putstr("Not yet implemented.\n")
        sleep(2.5)


class PulpCthulhuGame(CthulhuGame):
    def __init__(self, keypad: KeypadController, lcd: I2cLcd, fpath: str):
        super().__init__(keypad, lcd, fpath)
        self.investigator = PulpCharacter(fpath) #FIXME: Don't make me twice!
        self.game_menu["Change Luck"] = self.change_luck_points
        self.game_menu["View Pulp Talents"] = self.view_pulp_talents
        self.game_menu["Save Changes"] = self.save_changes
    
    def change_luck_points(self):
        self.lcd.putstr("Spending Luck?\n")
        answer = self.get_yes_no()
        self.reset_lcd
        self.lcd.putstr("How much luck?\n")
        amt = self.get_number()
        if answer:
            amt = -amt 

        self.investigator.change_luck(amt)

    def view_pulp_talents(self):
        self.reset_lcd()
        desc = self.select_from_list_menu(self.investigator.talents)
        self.reset_lcd()
        self.lcd.putstr(self.investigator.get_value_at(desc))
        usr_rdy = self.get_yes_no()
        self.reset_lcd()

    def save_changes(self):
        filename = self.investigator.name.strip(" ") + "_pulp_cthulhu.json"
        with open(filename, "w") as file:
            json.dump(file)
