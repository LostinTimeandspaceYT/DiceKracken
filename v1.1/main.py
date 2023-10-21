"""
credit: https://www.tomshardware.com/how-to/lcd-display-raspberry-pi-pico
"""

__author__ = "Nathan Winslow"
__copyright__ = "MIT"

from micropython import const
from machine import I2C, Pin
from time import sleep
from collections import OrderedDict
import json
from I2C_LCD import I2cLcd
from diceroller import Die
from kpc import KeypadController, Color


# Globals
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
i2c_addr = i2c.scan()[1]  # in this build address[0] is the keypad io

lcd = I2cLcd(i2c, i2c_addr, 2, 16)
keypad = KeypadController()

character_str = ""
with open('pulp_cthulhu_sheet.json','r') as sheet:
    for entry in sheet:
        character_str += entry
json_sheet = json.loads(character_str)


# Menu buttons
_CONFIRM = const(12)
_DENY = const(13)
_ACCEPT = const(10)
_BACKSPACE = const(11)
_UP_MENU = const(14)
_DOWN_MENU = const(15)


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
        

def start_up():
    """ start up logic """
    lcd.putstr("CoC Dice Roller   Version 1.1")
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
    ret = 0
    keypress = 0
    lcd.hide_cursor()
    current = 1
    max_len = len(list_of_stuff)
    
    while keypress != _CONFIRM:
        str_1 = ">:" + list_of_stuff[current - 1] + '\n'
        str_2 = "  " + list_of_stuff[current] + '\n'
        lcd.putstr(str_1)
        lcd.putstr(str_2)
        # print(">:", list_of_stuff[current - 1])
        # print("  ",list_of_stuff[current])
        
        keypress = keypad.get_button_press()
        
        if keypress == _UP_MENU:
            current -= 1
        elif keypress == _DOWN_MENU:
            current += 1

        if current >= max_len or current < 1:
            current = 1
        lcd.clear()
        sleep(.25)
        

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
            char = str(keypress)
            lcd.putchar(char)
            test_str += char   
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
                keypad.light_button(int(char), Color.black)
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


def loop():

    running = True
    while running:
        lcd.putstr("Enter your skill value:")
        skill_val = get_input()
        lcd.clear()
        lcd.putstr("Any modifiers?  C=Confirm D=Deny")
        mods = get_answer()

        if mods != _DENY:
            lcd.clear()
            lcd.putstr("Num of bonus      dice:")
            bonus_die = get_input()
            lcd.clear()
            lcd.putstr("Num of penalty    dice:")
            penalty_die = get_input()
        else:
            bonus_die = 0
            penalty_die = 0

        lcd.clear()
        dice = Die(skill_val)
        roll = dice(bonus_die, penalty_die)
        
        failed = determine_result(dice, roll)
        if failed and roll < dice.fumble:
            lcd.putstr("Push the roll?  C=Confirm D=Deny")
            push = get_answer()

            if push != _DENY:
                reset_lcd()
                result = dice(0,0)
                failed_push = determine_result(dice, result)
                if failed_push:
                    lcd.putstr("Failing pushed   rolls is bad!")
                    sleep(2)
                    reset_lcd()
                    
        lcd.putstr("Roll again?     C=Confirm D=Deny")
        again = get_answer()

        if again == _DENY:
            running = False

        reset_lcd()


def main():
    skills = []
    character_sheet = sort_character_sheet(json_sheet)
    for skill in (pretty_print_dict(character_sheet['Skills'])):
        # print(skill)
        skills.append(skill)
    select_skill_menu(skills)
    start_up()
    loop()


try:
    main()

finally:
    lcd.putstr("Until next time.")
    sleep(2)
    lcd.backlight_off()
    reset_lcd()
    keypad.light_buttons(16, Color.black)
    
