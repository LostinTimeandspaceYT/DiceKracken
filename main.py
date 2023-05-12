"""
credit: https://www.tomshardware.com/how-to/lcd-display-raspberry-pi-pico
"""

__author__ = "Nathan Winslow"
__copyright__ = "MIT"

from machine import I2C, Pin
from time import sleep
from I2C_LCD import I2cLcd
from DiceRoller import Die
from Keypad import Keypad

# Globals
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400_000)
i2c_addr = i2c.scan()[0]
lcd = I2cLcd(i2c, i2c_addr, 2, 16)
keypad = Keypad()
red_led = Pin(18, Pin.OUT)
grn_led = Pin(17, Pin.OUT)
blu_led = Pin(16, Pin.OUT)
brd_led = Pin(25, Pin.OUT)
confirm = 'C'
deny = 'D'


def setup():
    """
    start up logic
    """
    red_led.off()
    grn_led.off()
    blu_led.off()
    brd_led.on()
    lcd.putstr("Welcome to the CoC Dice Roller!")
    sleep(3)
    lcd.clear()


def reset():
    """
    reset the user led's and clears the lcd.
    """
    red_led.off()
    grn_led.off()
    blu_led.off()
    lcd.clear()
    lcd.blink_cursor_off()


def get_answer():
    """
    gets a yes or no answer from the user via keypad entry.
    blocking function.
    :return: 'C' for confirm , 'D' for Deny
    """

    ret = ""
    keypress = ''
    while keypress != 'C' and keypress != 'D':
        lcd.hide_cursor()
        keypress = keypad.get_keypress()

        if keypress == 'C' or keypress == 'D':  # Delete last keypress
            ret = keypress
        else:
            lcd.putstr("Press a valid key")
            sleep(2)
            lcd.clear()

        print(ret)
        print(f"keypress = {keypress}")

    return ret


def get_input():
    """
    gets a number from the user via keypad entry.
    blocking function.
    :return: int from user input
    """
    test_str = ""
    keypress = ''
    while keypress != 'A' and keypress != '*':
        lcd.blink_cursor_on()
        keypress = keypad.get_keypress()

        if '0' <= keypress <= '9':
            lcd.putchar(keypress)
            test_str += keypress

        if keypress == 'B':  # Delete last keypress

            test_str = test_str[:-1]
            if lcd.cursor_x > 7:
                lcd.cursor_x -= 1
                lcd.move_to(lcd.cursor_x, lcd.cursor_y)
                lcd.putchar(' ')
                lcd.cursor_x -= 1
                lcd.move_to(lcd.cursor_x, lcd.cursor_y)

        print(test_str)
        print(f"keypress = {keypress}")

    return int(test_str)


def blink(led, blinks=3):
    val = 0
    while blinks > 0:
        val = val ^ 1
        led.value(val)
        blinks -= 1
        sleep(.5)


def loop():

    running = True
    while running:
        lcd.putstr("Enter your skill value:")
        skill_val = get_input()
        lcd.clear()
        lcd.putstr("Number of bonus   dice:")
        bonus_die = get_input()
        lcd.clear()
        lcd.putstr("Number of penalty dice:")
        penalty_die = get_input()
        lcd.clear()
        dice = Die(skill_val)
        roll = dice(bonus=bonus_die, penalty=penalty_die)
        msg = ""
        failed = False

        # Result logic
        if dice.hard_suc < roll <= skill_val: # the user succeeded their roll
            grn_led.on()
            msg = "\nSuccess!"

        elif dice.extreme_suc < roll <= dice.hard_suc:
            blink(grn_led, blinks=2)
            msg = "\nHard success"

        elif 1 < roll <= dice.extreme_suc:
            blu_led.on()
            msg = "\nExtreme Success!"

        elif roll == 1: # the user got a critical success
            blink(blu_led)
            msg = "\nCritical success!"

        elif skill_val < roll < dice.fumble:  # the user failed the roll
            red_led.on()
            msg = "\nYou failed."
            failed = True

        elif roll >= dice.fumble:
            blink(red_led)
            msg = "\nYou fumbled."

        lcd.putstr("Result: " + str(roll) + '\n' + msg)  # show the user their result
        sleep(2.5)

        reset()

        if failed:
            lcd.putstr("Push the roll?  C=Confirm D=Deny")
            push = get_answer()

            if push != deny:
                reset()
                re = dice()
                msg1 = ""
                if re >= dice.fumble:
                    blink(red_led)
                    lcd.putstr("Shouldn't have done that!")

                elif skill_val < re < dice.fumble:  # the user failed the roll
                    red_led.on()
                    msg1 = "\nYou failed."

                elif 1 < re <= skill_val:
                    grn_led.on()
                    msg1 = "\nLucky roll"

                elif dice.extreme_suc < re <= dice.hard_suc:
                    blink(grn_led, blinks=2)
                    msg1 = "\nHard success"

                elif 1 < roll <= dice.extreme_suc:
                    blu_led.on()
                    msg1 = "\nExtreme Success!"

                elif roll == 1:
                    blink(blu_led)
                    msg1 = "\nCritical success!"

                lcd.putstr("Result: " + str(re) + '\n' + msg1)
                sleep(3.5)
                reset()

        lcd.clear()
        lcd.hide_cursor()
        lcd.putstr("Roll again?\nC=Confirm D=Deny")
        again = get_answer()
        if again == deny:
            running = False

        reset()


def main():
    setup()
    loop()


try:
    main()

except KeyboardInterrupt:
    lcd.clear()
    lcd.putstr("Shutting down...")
    sleep(3)
    brd_led.off()
    reset()

finally:
    lcd.putstr("Until next time.")
    sleep(3)
    brd_led.off()
    reset()
