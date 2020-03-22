#!/usr/bin/env micropython
from Griffy.menu import Menu
from Griffy.missions import Missions

DEBUG_ON = True
START_PAGE = 0 # which page of the menu to start on


missions = Missions(debug_on=DEBUG_ON)

PAGE1 = {
    # "COMMAND (up./right/left/down/enter)": {"DISPLAY_NAME", function ("next", "back")
    "up": ("M2", missions.second_run),
    "right": ("M3", missions.third_run),
    "left": ("M1", missions.first_run),
    "down": ("NEXT", "next"),
    "enter": ("M4", missions.fourth_run)
}
PAGE2 = {
    "up": ("M6", missions.sixth_run),
    "right": ("M7", missions.seventh_run),
    "left": ("M5", missions.fifth_run),
    "down": ("BACK", "back"),
    "enter": ("M8", missions.eighth_run)
}
PAGES = [PAGE1, PAGE2]

menu = Menu(start_page=START_PAGE, menu_pages=PAGES, debug_on=DEBUG_ON)
menu.display_menu(start_page=START_PAGE)


        # def show_sensors(self, iterations):
        #     """ Show the EV3 sensors, current mode and value """
        #     sensors = list(list_sensors(address=[INPUT_1, INPUT_2, INPUT_3]))   # , INPUT_4
        #     for _ in range(iterations):
        #         for sensor in sensors:
        #             print("{} {}: {}".format(sensor.address, sensor.mode, sensor.value()))
        #             sleep(.5)
        #     sleep(10)