"""
credit: https://www.tomshardware.com/how-to/lcd-display-raspberry-pi-pico
"""

__author__ = "Nathan Winslow"
__copyright__ = "MIT"

from micropython import const
from machine import I2C, Pin
from time import sleep
from I2C_LCD import I2cLcd
from kpc import KeypadController, Color
from game_factory import GameFactory, supported_games


# change these for your particular screen
_NUM_OF_ROWS = const(4)
_NUM_OF_COLS = const(20)


i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
i2c_addr = i2c.scan()[1]  # in this build address[0] is the keypad IO
lcd = I2cLcd(i2c, i2c_addr, _NUM_OF_ROWS, _NUM_OF_COLS)

# Keypad
keypad = KeypadController()


def welcome_splash():
    msg = " " * (_NUM_OF_COLS - 16)
    msg += "DICE KRACKEN!\n   Version 0.2"
    lcd.putstr(msg)
    sleep(5)
    reset_lcd()


def reset_lcd():
    lcd.clear()
    lcd.blink_cursor_off()


main_menu_options = [
    "Select game",
    "Download PC",
    "Download game",
    # add other options here!
    "Exit",  # Exit should always be last
]


def print_options(options: list[str]):
    i = 0
    for option in options:
        lcd.putstr(f"{i}: {option} \n")
        i += 1


def main_menu():
    sub_menus = [game_menu, download_character_menu, download_game_menu, power_off]

    keypress = -1
    while keypress != len(sub_menus) - 1:
        reset_lcd()
        print_options(main_menu_options)
        keypress = keypad.get_button_press()
        sub_menus[keypress]()


def game_menu():
    reset_lcd()
    i = 0
    for game in supported_games:
        lcd.putstr(f"{i}: {game} \n")
        i += 1
    keypress = keypad.get_button_press()

    while keypress >= len(supported_games):
        lcd.putstr("Press a valid key.\n")
        keypress = keypad.get_button_press()

    selected = supported_games[keypress]
    game = GameFactory.create_game(keypad, lcd, selected)
    game.loop()


def download_character_menu():
    pass


def download_game_menu():
    pass


def power_off():
    reset_lcd()
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
    # welcome_splash()
    main_menu()


try:
    main()

finally:
    power_off()
