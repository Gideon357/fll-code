#!/usr/bin/env micropython
# from Griffy.missions import Missions
from multiprocessing import Process
from os import listdir
from sys import stderr
from time import sleep

from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.led import Leds
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4, list_sensors

### WARNING! THIS MENU IS NOT FULLY OPERATIONAL SO DO NOT USE ###


current_options = 0
choices = []
proc = None

"""
Used to create a console menu for switching between programs quickly
without having to return to Brickman to find and launch a program.
Demonstrates the EV3DEV2 Console(), Led(), and Button() classes.
"""


def debug(str):
    """
    Additional debug method in case we do not have access to Griffy class.
    """
    print(str, file=stderr)


def get_positions(console):
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
        "enter": ("C", midcol, midrow),
    }


def wait_for_button_press(button):
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


def menu(
    choices, before_run_function=None, after_run_function=None, skip_to_next_page=True
):
    """
    Console Menu that accepts choices and corresponding functions to call.
    The user must press the same button twice: once to see their choice highlited,
    a second time to confirm and run the function. The EV3 LEDs show each state change:
    Green = Ready for button, Amber = Ready for second button, Red = Running
    Parameters:
    - `choices` a dictionary of tuples "button-name": ("mission-name", function-to-call)
    NOTE: Don't call functions with parentheses, unless preceded by lambda: to defer the call
    - `before_run_function` when not None, call this function before each mission run, passed with mission-name
    - `after_run_function` when not None, call this function after each mission run, passed with mission-name
    """

    global proc
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
            if last == pressed:  # was same button pressed?
                console.reset_console()
                leds.set_color("LEFT", "RED")
                leds.set_color("RIGHT", "RED")

                # call the user's subroutine to run the mission, but catch any errors
                try:
                    name, mission_function = choices[pressed]
                    if before_run_function is not None:
                        before_run_function(name)
                    if name in ("NEXT", "BACK", "OFF"):
                        mission_function()
                    else:
                        # launch a sub process so it could be canceled with the enter button
                        # store the subprocess in self to reference in the stop function
                        proc = Process(target=mission_function)
                        debug("Starting {}".format(name))
                        proc.start()
                        debug("Just started {} in proc {}".format(name, proc.pid))
                        sleep(1)
                        proc.terminate()
                        # TODO: Need to figure out when to call self.proc.join
                except Exception as e:
                    print("**** Exception when running")
                    debug("Exception when running {}".format(e))
                finally:
                    if after_run_function is not None:
                        after_run_function(name)
                    last = None
                    leds.set_color("LEFT", "GREEN")
                    leds.set_color("RIGHT", "GREEN")
            else:  # different button pressed
                last = pressed
                leds.set_color("LEFT", "AMBER")
                leds.set_color("RIGHT", "AMBER")


def terminate():
    """ A function to terminate the process created """
    global proc
    debug("Pressed off")
    try:
        if proc is not None:
            debug("About to kill process {}".format(proc.pid))
            proc.terminate
            debug("Killed process {}".format(proc.pid))
    except Exception as e:
        debug("Exception raised: {}".format(e))
        pass
    finally:
        debug("Setting proc to None")
        proc = None  # Silently ignore any exceptions and set proc back to none


def next():
    global current_options
    global choices
    global menu
    current_options += 1
    menu(choices[current_options], before_run_function=None, after_run_function=None)


def back():
    global current_options
    global choices
    global menu
    current_options -= 1
    menu(choices[current_options], before_run_function=None, after_run_function=None)


def before(mission_name):
    missions.start_tone
    print("before " + mission_name)


def after(mission_name):
    print("after " + mission_name)
    sleep(1)


if __name__ == "__main__":
    missions = Missions()

CHOICES = {
    "up": ("M2", missions.second_run),
    "right": ("M3", missions.third_run),
    "left": ("M1", missions.first_run),
    "down": ("NEXT", next),
    "enter": ("OFF", terminate),
}
CHOICES1 = {
    "up": ("M5", missions.fifth_run),
    "right": ("M6", missions.sixth_run),
    "left": ("M4", missions.fourth_run),
    "down": ("BACK", back),
    "enter": ("OFF", terminate),
}

choices = [CHOICES, CHOICES1]

menu(choices[current_options], before_run_function=None, after_run_function=None)
