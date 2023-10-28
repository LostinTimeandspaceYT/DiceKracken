import picokeypad


class Color:
    """
    This class can be expanded upon to create more colors.
    """
    white = 	(0xff, 0xff, 0xff)
    lt_blue = 	(0x00, 0x20, 0x20)
    green = 	(0x00, 0xff, 0x00)
    red = 		(0xff, 0x00, 0x00)
    blue = 		(0x00, 0x00, 0xff)
    yellow = 	(0x20, 0x20, 0x00)
    purple = 	(0x66, 0x00, 0xcc)
    pink = 		(0x99, 0x00, 0x99)
    black = 	(0x00, 0x00, 0x00)
    

class KeypadController:
    
    def __init__(self):
        # for checking states
        self._prev_btn_states = 0 
        
        self.keypad = picokeypad.PicoKeypad()
        self.keypad.set_brightness(0.50) # accepts a float from 0 - 1.0
        self.buttons = {
            0: Color.black,  
            1: Color.black,
            2: Color.black,
            3: Color.black,
            4: Color.black,  
            5: Color.black,
            6: Color.black,
            7: Color.black,
            8: Color.black,  
            9: Color.black,
            10: Color.lt_blue,
            11: Color.yellow,
            12: Color.green,  
            13: Color.red,
            14: Color.black,
            15: Color.black,
            }
        # light-up the keys
        self.default_layout()
        
    def get_button_press(self, btn_range=16):
        done = False
        pressed = 0
        while not done:
            btn_states = self.keypad.get_button_states()
            button = 0
            if self._prev_btn_states != btn_states:
                self._prev_btn_states = btn_states
                
                # First we have to find the button that was pressed
                for find in range(btn_range):
                    if btn_states & 0x01 > 0:
                        # make sure no other buttons were pressed
                        if not (btn_states & (~0x01)):
                            done = True
                            pressed = button
                        break
                    # else, check the next button
                    btn_states >>= 1
                    button += 1
        return pressed

        
    def check_num_buttons(self):
        result = 0
        done = False
        decimal_place = 10
        lit = []
        while not done:
            btn_states = self.keypad.get_button_states()
            
            if self._prev_btn_states != btn_states:
                self._prev_btn_states = btn_states
                # First we have to find the button that was pressed
                button = 0

                changed = False
                for find in range(12):
                    if btn_states & 0x01 > 0:
                        # make sure no other buttons were pressed
                        if not (btn_states & (~0x01)):  
                            changed = True
                        break
                    # else, check the next button
                    btn_states >>= 1
                    button += 1
                
                # toggle the color of the button
                if decimal_place == 10 and button < 10:
                    self.buttons[button] = Color.pink
                    result += (button * decimal_place)
                    decimal_place /= 10
                    lit.append(button)
                    
                elif decimal_place == 1 and button < 10:
                    self.buttons[button] = Color.lt_blue
                    result += button
                    lit.append(button)
                
                elif button == 11:
                    # reset the numbers
                    self.reset_number_buttons() 
                    changed = False
                    result = 0
                    if decimal_place == 1:
                        decimal_place *= 10
                        
                elif button == 10:
                    done = True
                            
                if changed:
                    self.light_button(button, self.buttons[button])

        self.reset_number_buttons()
        return int(result)               
            
    def light_button(self, button: int, color: tuple):
        """
        Lights the desired button to the specified color
        
        :param button - int value 0-15
        :param color - Color.your_color [class included in this module]
        :return None
        """
        self.keypad.illuminate(button, *color)
        self.keypad.update()
        
    def reset_number_buttons(self):
        for i in range(10):
            self.buttons[i] = Color.black
            self.light_button(i, self.buttons[i])
    
    def light_buttons(self, vals, color: tuple):
        """
        Lights a range of buttons to the specified color
        
        :param vals - list of buttons to 
        :param color - Color.your_color [class included in this module]
        :return None
        """        
        for i in range(vals):
            self.keypad.illuminate(i, *color)
        self.keypad.update()

    def default_layout(self):
        for i in range(16):  
            self.light_button(i, self.buttons[i])
