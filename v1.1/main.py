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
from game import supported_games, GameFactory




# change these for your particular screen
_NUM_OF_ROWS = const(4) 
_NUM_OF_COLS = const(20)


i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
i2c_addr = i2c.scan()[1]  # in this build address[0] is the keypad io
lcd = I2cLcd(i2c, i2c_addr, _NUM_OF_ROWS, _NUM_OF_COLS)

# Keypad
keypad = KeypadController()


def welcome_splash():
    msg = " " * (_NUM_OF_COLS - 16)
    msg += "DICE KRAKEN\n    Version 1.1"
    lcd.putstr(msg)
    sleep(5)
    reset_lcd()

def reset_lcd():
    lcd.clear()
    lcd.blink_cursor_off()

main_menu_options = [ 
    "Select a game",
    "Download character",
    "Download new game",
    # add other options here!
    "Exit (Power Off)"  # Exit should always be last
]

def print_options(options: list[str]):
    i = 0
    for option in options:
        lcd.putstr(f"{i}: {option} \n")
        i += 1


def main_menu():
    sub_menus = [
        game_menu,
        download_character_menu,
        download_game_menu
    ]

    print_options(main_menu_options)
    keypress = keypad.get_button_press()

    while keypress != main_menu_options.index("Exit (Power Off)\n"):
        reset_lcd()
        sub_menus[keypress]
        reset_lcd()
        print_options(main_menu_options)
        keypress = keypad.get_button_press()



def game_menu():
    for game in supported_games:
        lcd.putstr(game)

def download_character_menu():
    pass

def download_game_menu():
    pass

def power_off():
    lcd.putstr("Until next time.\n")
    sleep(2)
    lcd.backlight_off()
    reset_lcd()
    keypad.light_buttons(16, Color.black)

"""
Start up Procedure

1. Initialize Keypad and LCD
2. Display welcome splash
3. Display Home menu
    - Download new games
    - Download a character
    - Select a game
    - Exit (Quit/Power off)
4. Display sub-menu for selected option
    - downloading new games is low priority ATM
    - downloading a character is medium priority ATM
    - Selecting a game is top priority ATM
    - Exiting is top priority ATM
5. When the user selects Exit, safely power off the device
"""


def main():
    welcome_splash()
    main_menu()


try:
    main()

finally:
    power_off()
    
