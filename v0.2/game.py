"""
This module defines the game logic 
"""

from time import sleep
from character_sheet import CthulhuCharacter, PulpCharacter
from kpc import KeypadController, Color
from I2C_LCD import I2cLcd

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
    def __init__(self, keypad: KeypadController, lcd: I2cLcd, fpath: str):
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

        while keypress != self.keypad.CONFIRM:
            for i in range(self.lcd.num_lines):
                if i == cursor_index:
                    msg = '>:' 
                else:
                    msg = '  '
                    
                msg += list_of_stuff[current + i] + '\n'
                self.lcd.putstr(msg)

            keypress = self.keypad.get_button_press()
            
            if keypress == self.keypad.UP_MENU:
                cursor_index -= 1
                
            elif keypress == self.keypad.DOWN_MENU:
                cursor_index += 1
            
            
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
            
        return list_of_stuff[current].lstrip()  
    
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
        while keypress != self.keypad.CONFIRM and keypress != self.keypad.DENY:

            keypress = self.keypad.get_button_press()

            if keypress == self.keypad.CONFIRM:
                return True
            
            elif keypress == self.keypad.DENY:
                return False
            
            else:
                self.lcd.putstr("Press a valid key")
                sleep(1.5)
                self.lcd.clear()


class CthulhuGame(Game):
    def __init__(self, keypad: KeypadController, lcd: I2cLcd, fpath: str):
        super().__init__(keypad, lcd, fpath)
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
        }
        
    def loop(self):
        while self.running:
            i = 0
            options = []
            self.reset_lcd()
            for k,v in self.game_menu.items():
                options.append(k)
                self.lcd.putstr(f"{i}: {k}\n")
                i += 1
            keypress = self.keypad.get_button_press()
            while keypress >= len(self.game_menu):
                self.lcd.putstr("Press a valid key.\n")
                keypress = self.keypad.get_button_press()
            self.reset_lcd()
            self.game_menu[options[keypress]]()
            
        

    def determine_result(self, roll: int,  skill_val: int,  fumble: int, difficulty: str) -> bool:

        msg = ""
        failed = False
        if roll <= skill_val:
            msg = f"\n{difficulty} success!"

            if difficulty == "Normal":
                self.keypad.light_buttons(16, Color.green)

            elif difficulty == "Hard":
                self.keypad.light_buttons(16, Color.lt_blue)

            else:  # Extreme
                self.keypad.light_buttons(16, Color.yellow)

        elif roll == 1:
            msg = "\nCritical success!"
            self.keypad.light_buttons(16, Color.white)

        elif roll > skill_val and roll < fumble:
            msg = "\nFailure."
            self.keypad.light_buttons(16, Color.purple)
            failed = True

        else:  # roll >= fumble
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
        self.reset_lcd()
        diff = self.select_from_list_menu(self.difficulty_levels)
        self.reset_lcd()
        val = self.investigator.get_value_at(skill)
        if isinstance(val, int):
            self.lcd.putstr("Any modifiers?  C=Confirm D=Deny")
            if self.get_yes_no():
                self.lcd.clear()
                self.lcd.putstr("Num of bonus\ndice:")
                bonus = self.get_number()
                self.lcd.clear()
                self.lcd.putstr("Num of penalty\ndice:")
                penalty = self.get_number()
            else:
                bonus = 0
                penalty = 0

            self.lcd.clear()

            roll = self.investigator.roll_skill(bonus, penalty)
            skill_val_at = self.investigator.get_skill_at_difficulty(val, diff)
            fumble = self.investigator.get_fumble(val)
            failed = self.determine_result(roll, skill_val_at, fumble, diff)
            if failed and roll < fumble:
                self.lcd.putstr("Push the roll?  C=Confirm D=Deny")
                push = self.get_yes_no()

                if push != self.keypad.DENY:
                    self.reset_lcd()
                    roll = self.investigator.roll_skill(bonus, penalty)
                    failed_push = self.determine_result(roll, skill_val_at, fumble, diff)
                    if failed_push:
                        self.lcd.putstr("Failing pushed   rolls is bad!")
                        sleep(2)
                        self.reset_lcd()
        else:
            raise TypeError("Selected Skill does not have a value associated with it.")
        
    def change_hit_points(self):
        self.lcd.putstr("Taking Damage?\n C=Confirm D=Deny")
        if self.get_yes_no():
            amt = - self.get_number()
        else:
            amt = self.get_number()

        self.investigator.change_hit_points(amt)    

    def change_sanity(self):
        self.lcd.putstr("Losing Sanity\n C=Confirm D=Deny")
        if self.get_yes_no():
            amt = - self.get_number()
        else:
            amt = self.get_number()

        self.investigator.change_sanity(amt)

class PulpCthulhuGame(CthulhuGame):
    def __init__(self, keypad: KeypadController, lcd: I2cLcd, fpath: str):
        super().__init__(keypad, lcd, fpath)


