# TODO: fix font size after coming back from calibrate light or sensor reading, the robot reports a font but it's not correctly drawing that font

from time import sleep
from sys import stderr
from os import listdir
from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.led import Leds
from ev3dev2.sensor import list_sensors, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sound import Sound

class Menu():
    """
    A GUI menu that helps us control what we run
    in a competition
    """

    def __init__(self, start_page=0, menu_pages=[], debug_on=True):
        """ TODO: Create documentation for how to dstructure menu_pages"""
        self.current_page = start_page # Represents the current page/list of menu items being displayed
        self.menu_pages = menu_pages # A list of lists for all of the pages for the menu items
        self.debug_on = debug_on

    def menu_tone(self):
        player = Sound()
        player.play_tone(1000, 0.5, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    def press_tone(self):
        player = Sound()
        player.play_tone(750, 0.2, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        player.play_tone(1250, 0.2, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    def debug(self, str):
        """Print to stderr the debug message ``str`` if self.debug is True."""
        if self.debug_on:
            print(str, file=stderr)

    def get_menu_positions(self, console):
        """
        Compute a dictionary keyed by button names with horizontal alignment,
        and column/row location to show each choice on the EV3 LCD console.
        Parameter:
        - `console` (Console): an instance of the EV3 Console() class
        returns a dictionary keyed by button names with column/row location
        """

        midrow = 1 + console.rows // 2
        midcol = 1 + console.columns // 2
        # horiz_alignment, col, row
        return {
            "up": ("C", midcol, 1),
            "right": ("R", console.columns, midrow),
            "down": ("C", midcol, console.rows),
            "left": ("L", 1, midrow),
            "enter": ("C", midcol, midrow)
        }

    def wait_for_button_press(self, button):
        """
        Wait for a button to be pressed and released.
        Parameter:
        - `button` (Button): an instance of the EV3 Button() class
        return the Button name that was pressed.
        """
        pressed = None
        while True:
            allpressed = button.buttons_pressed
            if bool(allpressed):
                pressed = allpressed[0]  # just get the first one
                while not button.wait_for_released(pressed):
                    pass
                break
        return pressed

    def display_menu(self, start_page=0, before_run_function=None, after_run_function=None, skip_to_next_page=True):
        """
        Console Menu that accepts choices and corresponding functions to call.
        The user must press the same button twice: once to see their choice highlited,
        a second time to confirm and run the function. The EV3 LEDs show each state change:
        Green = Ready for button, Amber = Ready for second button, Red = Running
        Parameters:
        - `choices` a dictionary of tuples "button-name": ("function-name", function-to-call)
        NOTE: Don't call functions with parentheses, unless preceded by lambda: to defer the call
        - `before_run_function` when not None, call this function before each function run, passed with function-name
        - `after_run_function` when not None, call this function after each function run, passed with function-name
        """

        self.current_page = start_page

        console = Console()
        leds = Leds()
        button = Button()

        leds.all_off()
        leds.set_color("LEFT", "GREEN")
        leds.set_color("RIGHT", "GREEN")
        menu_positions = self.get_menu_positions(console)

        last = None  # the last choice--initialize to None

        self.menu_tone()
        self.debug("Starting Menu")
        while True:
            # display the menu of choices, but show the last choice in inverse
            console.reset_console()
            self.debug("Reset the display screen")
            console.set_font('Lat15-TerminusBold24x12.psf.gz', True)
            
            # store the currently selected menu page
            menu_page = self.menu_pages[self.current_page]
            # store the currently selected menu items
            menu_options_on_page = menu_page.items() 
            
            for btn, (name, _) in menu_options_on_page:
                align, col, row = menu_positions[btn]
                console.text_at(name, col, row, inverse=(btn == last), alignment=align)
            self.debug("Waiting for button press...")
            pressed = self.wait_for_button_press(button)
            self.debug("Registered button press: {}".format(pressed))
            
            # get the choice for the button pressed
            if pressed in menu_page:
                if last == pressed:   # was same button pressed?
                    console.reset_console()
                    leds.set_color("LEFT", "RED")
                    leds.set_color("RIGHT", "RED")

                    # call the user's subroutine to run the function, but catch any errors
                    try:
                        name, run_function = menu_page[pressed]
                        if before_run_function is not None:
                            self.debug('Running before function')
                            before_run_function(name)
                        self.press_tone()
                        type_of_run_function = type(run_function)
                        self.debug("Type of run_function: {}".format(type_of_run_function))

                        if isinstance(run_function, str):
                            self.debug("Running {}".format(run_function))
                            if run_function == 'next':
                                self.debug("About to call next")
                                self.next()
                            elif run_function =='back':
                                self.debug("About to call back")
                                self.back()
                        elif callable(run_function):
                            run_function()
                    except Exception as e:
                        print("**** Exception when running")
                        raise(e)
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

    def next(self):
        self.current_page += 1
        self.debug("Incremented current_page to {}".format(self.current_page))
        #self.menu(self.menu_pages[self.current_page], before_run_function=None, after_run_function=None)
    
    def back(self):
        self.current_page -= 1
        self.debug("Decremented current_page to {}".format(self.current_page))
        #self.menu(self.menu_pages[self.current_page], before_run_function=None, after_run_function=None)
        