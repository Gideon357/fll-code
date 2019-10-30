#!/usr/bin/env micropython

from Griffy import menu, missions

if __name__ == '__main__':
    menu = menu.menu()
    CHOICES2 = {
            "up": ("MI1", missions.mission1),
            "right": ("MI2", missions.mission2),
            "left": ("MI3", missions.mission3),
            "down": ("SHOW", lambda: show_sensors(5)),
            "enter": ("NEXT", missions.next_page)
        }
    CHOICES2 = {
            "up": ("MI1", missions.mission1),
            "right": ("MI2", missions.mission2),
            "left": ("MI3", missions.mission3),
            "down": ("SHOW", lambda: show_sensors(5)),
            "enter": ("NEXT", missions.next_page)
        }
    choices = [CHOICES1, CHOICES2]

    menu(choices[menu.current_options], before_run_function=before, after_run_function=after)

