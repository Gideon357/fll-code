#!/usr/bin/env micropython
from Griffy.menu import Menu
from Griffy.griffy import Griffy

DEBUG_ON = True
START_PAGE = 0 # which page of the menu to start on


griffy = Griffy(debug_on=DEBUG_ON)

PAGE1 = {
    # "COMMAND (up./right/left/down/enter)": {"DISPLAY_NAME", function ("next", "back")
    "up": ("GY ON/OFF", griffy.flip_gyro_sensor_setting),
    "right": ("READ", 'next'),
    "left": ("CALI", griffy.write_light_to_settings),
    "down": ("CAL GY", griffy.calibrate_gyro),
    "enter": ("DBG", griffy.flip_debug_setting)
}
PAGE2 = {
    "up": ("SE2", lambda: griffy.display_gyro_sensor('left')),
    "right": ("SE3", lambda: griffy.display_gyro_sensor('right')),
    "left": ("SE1", lambda: griffy.display_color_sensor('left')),
    "down": ("SE4", lambda: griffy.display_color_sensor('right')),
    "enter": ("BACK", 'back')
}
PAGES = [PAGE1, PAGE2]

menu = Menu(start_page=START_PAGE, menu_pages=PAGES, debug_on=DEBUG_ON)
menu.display_menu(start_page=START_PAGE)
