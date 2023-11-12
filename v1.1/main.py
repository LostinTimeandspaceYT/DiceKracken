"""
credit: https://www.tomshardware.com/how-to/lcd-display-raspberry-pi-pico
"""

__author__ = "Nathan Winslow"
__copyright__ = "MIT"

from micropython import const
from machine import I2C, Pin
from time import sleep
from character_sheet import PulpCharacter
from I2C_LCD import I2cLcd
from dice import Dice
from kpc import KeypadController, Color


# Menu buttons #
_CONFIRM = const(12)
_DENY = const(13)
_ACCEPT = const(10)
_BACKSPACE = const(11)
_UP_MENU = const(14)
_DOWN_MENU = const(15)

# change these for your particular screen
_NUM_OF_ROWS = const(4) 
_NUM_OF_COLS = const(20)


i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
i2c_addr = i2c.scan()[1]  # in this build address[0] is the keypad io
lcd = I2cLcd(i2c, i2c_addr, _NUM_OF_ROWS, _NUM_OF_COLS)

# Keypad
keypad = KeypadController()


def start_up():
    """ start up logic """
    msg = " " * (_NUM_OF_COLS - 16)
    msg += "DICE KRAKEN\n    Version 1.1"
    lcd.putstr(msg)
    sleep(5)
    lcd.clear()

def reset_lcd():
    lcd.clear()
    lcd.blink_cursor_off()

def get_answer():
    """
    gets a yes or no answer from the user via keypad entry.
    blocking function.
    """

    ret = 0
    keypress = 0
    lcd.hide_cursor()
    while keypress != _CONFIRM and keypress != _DENY:

        keypress = keypad.get_button_press()

        if keypress == _CONFIRM or keypress == _DENY:
            ret = keypress
        else:
            lcd.putstr("Press a valid key")
            sleep(2)
            lcd.clear()

    return ret

def select_skill_menu(list_of_stuff):  
    keypress = 0
    lcd.hide_cursor()
    current = 0
    cursor_index = 0
    max_len = len(list_of_stuff)
    
    while keypress != _CONFIRM:
        for i in range(_NUM_OF_ROWS):
            if i == cursor_index:
                msg = '>:' 
            else:
                msg = '  '
                
            msg += list_of_stuff[current + i] + '\n'
            lcd.putstr(msg)

        keypress = keypad.get_button_press()
        
        if keypress == _UP_MENU:
            cursor_index -= 1
            
        elif keypress == _DOWN_MENU:
            cursor_index += 1
        
        
        if cursor_index >= _NUM_OF_ROWS:
            cursor_index = 0 # we may want to set to _NUM_OF_ROWS - 1
            current += (_NUM_OF_ROWS - 1)
            lcd.clear()
            
        elif cursor_index < 0:
            cursor_index = _NUM_OF_ROWS - 1 # and this to 0 depending on desired behavior
            current -= (_NUM_OF_ROWS - 1)
            lcd.clear()
            
        if (current + (_NUM_OF_ROWS - 1)) >= max_len or current < 0:
            current = 0
            
        sleep(.1)      

def get_input():
    """
    gets a number from the user via keypad entry.
    blocking function.
    :return: int from user input
    """
    test_str = ""
    keypress = None
    lcd.blink_cursor_on()
    first = True
    prev_press = -1
    while keypress != _ACCEPT:
        keypress = keypad.get_button_press()

        if 0 <= keypress <= 9:
            usr_in = str(keypress)
            lcd.putchar(usr_in)
            test_str += usr_in   
            if first:
                keypad.light_button(keypress, Color.pink)
                first = False
            else:
                keypad.light_button(keypress, Color.blue)
            prev_press = keypress

        if keypress == _BACKSPACE:
            if first:
                keypad.light_button(int(test_str), Color.black)
            else:
                keypad.light_button(int(usr_in), Color.black)  # We are bounded to 16 Python!!!
                first = True
                
            test_str = test_str[:-1]
            if lcd.cursor_x > 7:
                lcd.cursor_x -= 1
                lcd.move_to(lcd.cursor_x, lcd.cursor_y)
                lcd.putchar(' ')
                lcd.cursor_x -= 1
                lcd.move_to(lcd.cursor_x, lcd.cursor_y)


    lcd.blink_cursor_off()
    keypad.reset_number_buttons()
    return int(test_str) if test_str != "" else 0

def determine_result(die, res) -> bool:
    """
    determines result of the roll and displays it
    to the user.
    
    Reason for returning true upon failure is to
    facilitate futher game logic. Much more interested
    in skill failure than success.
    
    :return: True if roll failed.
    """
    msg = ""
    failed = False
    if die.hard_suc < res <= die.skill_val:
        msg = "\nSuccess!"
        keypad.light_buttons(16, Color.green)

    elif die.extreme_suc < res <= die.hard_suc:
        msg = "\nHard success!"
        keypad.light_buttons(16, Color.lt_blue)

    elif 1 < res <= die.extreme_suc:
        msg = "\nExtreme Success!"
        keypad.light_buttons(16, Color.yellow)

    elif res == 1:
        msg = "\nCritical success!"
        keypad.light_buttons(16, Color.white)

    elif die.skill_val < res < die.fumble:
        msg = "\nFailure."
        keypad.light_buttons(16, Color.purple)
        failed = True

    elif res >= die.fumble:
        msg = "\nFumble..."
        keypad.light_buttons(16, Color.red)
        failed = True

    lcd.putstr("Result: " + str(res) + '\n' + msg)
    sleep(3.5)
    keypad.default_layout()
    reset_lcd()
    return failed

def main():
    my_file = 'pulp_cthulhu_sheet.json'
    my_character = PulpCharacter(my_file)
    select_skill_menu(my_character.skills)
    reset_lcd()
    start_up()


try:
    main()

finally:
    lcd.putstr("Until next time.")
    sleep(2)
    lcd.backlight_off()
    reset_lcd()
    keypad.light_buttons(16, Color.black)
    
