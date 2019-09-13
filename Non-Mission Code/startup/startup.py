from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.console import Console
from codes import menu.py,startup_menu.py, motor_control.py """add files for other programs here"""

startup() = startup_menu.menu
motorControl(self, motor_control.start(),2, Motor Control) = startup_menu.menuObject
missionMenu(self, startup_menu.start(),1,File Browser ) =  startup_menu.menuObject

# initialize programs as objects here, using "menu.menuObject" not "startup_menu.menuObject"