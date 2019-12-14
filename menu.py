#!/usr/bin/env micropython
from time import sleep
from sys import stderr
from os import listdir
from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.led import Leds
from ev3dev2.sensor import list_sensors, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from Griffy.missions import Missions
from threading import Thread

current_options = 0
choices = []

"""
Used to create a console menu for switching between programs quickly
without having to return to Brickman to find and launch a program.
Demonstrates the EV3DEV2 Console(), Led(), and Button() classes.
"""


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
        "enter": ("C", midcol, midrow)
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


def menu(choices, before_run_function=None, after_run_function=None, skip_to_next_page=True):
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
                    mission_thread = Thread(target=mission_function)
                    mission_thread.start()
                except Exception as ex:
                    print("**** Exception when running")
                    raise(ex)
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


if __name__ == "__main__":
    missions = Missions(debug_on=False)

    def calibrate():
        """ Placeholder for call to your calibration logic to set the black and white values for your color sensors """
        print("calibrating...")
        sleep(1)

    def show_sensors(iterations):
        """ Show the EV3 sensors, current mode and value """
        sensors = list(list_sensors(address=[INPUT_1, INPUT_2, INPUT_3]))   # , INPUT_4
        for _ in range(iterations):
            for sensor in sensors:
                print("{} {}: {}".format(sensor.address, sensor.mode, sensor.value()))
                sleep(.5)
        sleep(10)

    def mission1():
        print("mission 1...")
        sleep(1)

    def mission2():
        print("mission 2...")
        sleep(1)

    def mission3():
        print("mission 3...")
        sleep(1)
        raise Exception('Raised error')
        
    def stop():
    

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

    CHOICES = {
        "up": ("M2", missions.second_run),
        "right": ("M3", missions.third_run),
        "left": ("M1", missions.first_run),
        "down": ("NEXT", next),
        "enter": ("OFF", stop)
    }
    CHOICES1 = {
        "up": ("M5", missions.fifth_run),
        "right": ("M6", missions.sixth_run),
        "left": ("M4", missions.fourth_run),
        "down": ("BACK", back),
        "enter": ("OFF", stop)
    }
    
    choices = [CHOICES,CHOICES1]


    menu(choices[current_options], before_run_function=None, after_run_function=None)
