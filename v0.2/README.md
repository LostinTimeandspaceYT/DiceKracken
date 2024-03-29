# Version 0.2
CoC dice roller rebranded to the Dice Kracken

## Updates
- New keypad! This version uses the Pimoroni Keypad linked Here: https://shop.pimoroni.com/products/pico-rgb-keypad-base?variant=32369517166675
  
- Added support for controlling the keypad with the kpc.py module
- Support for reading characters sheets via JSON (example sheet provided !)
- Menu support for skill roll selection

### Update Nov/12/23

- fixed a bug when attempting to find values inside a nested dictionary. Very useful when trying to find skill values

- added support rolling skills at a particular difficulty level.

- added support for manipulating hp, mp, luck, and sanity

- Adding support for regular and pulp Cthulhu characters 

- added support for any sided dice rolling. This should make adding  other games easier

- updated file structure to reflect new changes

### Update Dec/16/2023

- Rebranded device as the Dice Kracken. Sounds cool, right?!

- Began work on the Game interface and GameFactory classes to support other RPGs in the future.

- Began work on a main menu system

- Restructured main.py to utilize new code structure.

- Added PlayerCharacter base class to more generalize behavioral code

These changes aim to decouple the Character classes from the Game logic classes. The Character classes now
only concern themselves with keeping track of stats, improvements, and 'rolling the dice'. The Game classes
perform logic and interface with the peripherials. 

The GameFactory class aims to allow the device to support multiple games and characters on the same device.

### Update Dec 28/23  
_Began work on Web API to interface with Dice Kracken._
Pico-W acts as the server, hosting files which can be accessed via a browser. 
To test the connection of your Pico-W, don't forget to change the ``ssid`` and ``password`` in ``network_crediantials.py``.
- Created example frontend web stack.
- Skills and Characteristics auto-fill half and fifth values (though currently not used)
- Will be further fleshed out in time.

### Update Feb 16/24
_Squashed a few bugs and continued work on fleshing out functionality._

- Fixed a bug that would cause critical successes to be displayed incorrectly
- Saving changes is now possible, but will require slight refactoring to generalize functionality across all games.
- Began work on weapon selection to determine damage dice for rolling damage during attacks.
- Added features to PulpCthulhuGame to view pulp talents and change luck.

### Update Mar 1/24
_Continued work on weapon selection to CthulhuCharacter._

- Created example Pulp Cthulhu Character.
- Add menu item for user to select which weapon to use from their list of weapons. 
- Added a `current_weapon` member to `CthulhuCharacter` for accessing weapon stats.

## In Progress
- Fleshing out CharacterSheet class
- Main menu interface
- GameFactory and Game classes
- Web API
- Parsing strings for dice ex: `"1d6 + 2"` == `roll_die(1,6) + 2`

## Future Improvements/ Wishlist
- PCB Design for a "turn-key" solution.
- Simple Drag and Drop UF2 File. 

## Known Issues
- When trying to traverse up over the top of the list, the cursor will move down to the bottom of the screen.
- Certain menu interactions lead to poorly formatted text.
- MEMORYERROR: when attempting to serve up CoC_character_creator.html
- Bug in `select_from_list_menu` that causes lists to sometimes now be fully displayed. _likely an issue with the bounds check._

# Putting it Together

## Bill of Materials
1x USB-Micro Cable + Wall adapter  
1x Pico-W: https://shop.pimoroni.com/products/raspberry-pi-pico-w?variant=40059369619539  
1x Pimoroni Pico RGB Keypad Base: https://shop.pimoroni.com/products/pico-rgb-keypad-base?variant=32369517166675  
1x LCD Display  with I2C Adapter such as the PCF8574: https://www.pishop.us/product/compatible-lcd-display-2-5-lcd-1602-i2c-communication/    
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
        
## Additional Information
_The Pimoroni Micropython uf2 file is required for this project. The lastest release of these files can be found here: https://github.com/pimoroni/pimoroni-pico/releases_


# Fan Material Policy  
“This application uses trademarks and/or copyrights owned by Chaosium Inc/Moon Design Publications LLC, which are used under Chaosium Inc’s Fan Material Policy.
We are expressly prohibited from charging you to use or access this content. This application is not published, endorsed, or specifically approved by Chaosium Inc.
For more information about Chaosium Inc’s products, please visit www.chaosium.com.”

Link: https://www.chaosium.com/fan-material-policy/
