# Version 1.1
New and improved version of the CoC Dice Roller 

## Updates
- New keypad! This version uses the Pimoroni Keypad linked Here: https://shop.pimoroni.com/products/pico-rgb-keypad-base?variant=32369517166675
  
  - Added support for controlling the keypad with the kpc.py module
- Support for reading characters sheets via JSON (example sheet provided !)
- Menu support for skill roll selection (still a work in progress)
  
## Future Improvements/ Wishlist
- Finish skill roll selection menu
- Ability to update values from the app
- Web API support for users to download their own character sheets

## Bill of Materials
1x USB-Micro Cable + Wall adapter
1x Pico-W
1x Pimoroni Pico RGB Keypad Base: https://shop.pimoroni.com/products/pico-rgb-keypad-base?variant=32369517166675
1x LCD Display
1x I2C Adapter such as the PCF8574
4x M -> F jumper wires

## Assembly
_Note: Some Soldering is required_

1. Solder the male ends of the jumper wires to **VSYS**(Pin 39), **-**(GND Pin 38), **SDA**(GP 4), **SCL**(GP 5) onto the Keypad base
2. Mount the Pico-W in the proper orientation as pictured on the Keypad
3. Connect the female ends of the jumper wires to the following:
   **Vcc** to **VSYS**,
   **GND** to **-**,
   **SDA** to **SDA**,
   **SCL** to **SCL**


## Fan Material Policy  
“This application uses trademarks and/or copyrights owned by Chaosium Inc/Moon Design Publications LLC, which are used under Chaosium Inc’s Fan Material Policy.
We are expressly prohibited from charging you to use or access this content. This application is not published, endorsed, or specifically approved by Chaosium Inc.
For more information about Chaosium Inc’s products, please visit www.chaosium.com.”

Link: https://www.chaosium.com/fan-material-policy/
