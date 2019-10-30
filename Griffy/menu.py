from griffy import
from time import sleep
from os import listdir
from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.led import Leds
from ev3dev2.sensor import list_sensors, INPUT_1, INPUT_2, INPUT_3, INPUT_4



class menu:
    def __init__():
        self.current_options = 0
        self.midrow = 1 + console.rows // 2
        self.midcol = 1 + console.columns // 2


    def get_positions(console):
        
        # horiz_alignment, col, row
        return {
            "up": ("C", self.midcol, 1),
            "right": ("R", console.columns, self.midrow),
            "down": ("C", midcol, self.console.rows),
            "left": ("L", 1, self.midrow),
            "enter": ("C", self.midcol, self.midrow)
        }


    def wait_for_button_press(button):
    
        pressed = None
        while True:
            allpressed = button.buttons_pressed
            if bool(allpressed):
                pressed = allpressed[0]  # just get the first one
                while not button.wait_for_released(pressed):
                    pass
                break
        return pressed


    def menu(choices, before_run_function=None, after_run_function=None):
      
        console = Console()
        leds = Leds()
        button = Button()

        leds.all_off()
        leds.set_color("LEFT", "GREEN")
        leds.set_color("RIGHT", "GREEN")
        menu_positions = get_positions(console)

        last = None  # the last choice--initialize to None

        while True:
            # display the menu of choices, but show the last choice in inverse
            console.reset_console()
            for btn, (name, _) in choices.items():
                align, col, row = menu_positions[btn]
                console.text_at(name, col, row, inverse=(btn == last), alignment=align)

            pressed = wait_for_button_press(button)

            # get the choice for the button pressed
            if pressed in choices:
                if last == pressed:   # was same button pressed?
                    console.reset_console()
                    leds.set_color("LEFT", "RED")
                    leds.set_color("RIGHT", "RED")

                    # call the user's subroutine to run the mission, but catch any errors
                    try:
                        name, mission_function = choices[pressed]
                        if before_run_function is not None:
                            before_run_function(name)
                        mission_function()
                    except Exception as ex:
                        print("**** Exception when running")
                        print(ex)
                    finally:
                        if after_run_function is not None:
                            after_run_function(name)
                        last = None
                        leds.set_color("LEFT", "GREEN")
                        leds.set_color("RIGHT", "GREEN")
                else:   # different button pressed
                    last = pressed
                    leds.set_color("LEFT", "AMBER")
                    leds.set_color("RIGHT", "AMBER")
        def next_page():
            global current_options 
            current_options = current_options + 1
            menu(choices[current_options], before_run_function=before, after_run_function=after)

            


