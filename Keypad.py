from machine import Pin
from time import sleep_ms

# constants
keys = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]
rows = [0, 1, 2, 3]
cols = [4, 5, 6, 7]
KEY_UP = 0
KEY_DOWN = 1


class Keypad:

    def __init__(self):
        self.row_pins = [Pin(pin_name, Pin.OUT) for pin_name in rows]
        self.col_pins = [Pin(pin_name, Pin.IN, pull=Pin.PULL_DOWN) for pin_name in cols]
        self.last_key_press = ''
        for row in range(0, 4):
            for col in range(0, 4):
                self.row_pins[row].low()

    def get_keypress(self):
        self.last_key_press = ''
        while self.last_key_press == '':
            for row in range(4):
                for col in range(4):
                    self.row_pins[row].high()
                    key = self.col_pins[col].value()
                    self.row_pins[row].low()
                    sleep_ms(10)
                    if key == KEY_DOWN:
                        self.last_key_press = keys[row][col]
                        print("Key Pressed: " + keys[row][col])
                        return self.last_key_press
