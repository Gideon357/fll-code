"""
This program will allow for a menu that displays all programs instead of the menu browser saving 20 seconds of time in loading.
TODO:
Add run at start
"""
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.console import Console

class loader:
    def __init__(self):
        button = Button()
        menuItems = []
        displayNum = 0
        while True:
            for i in range(len(menuItems)):
                menuItems[i] = "nil"

    class menuObject:

        def __init__(self, name, functionName, programNumber, programName):
            self.functionName = functionName
            self.programName = programName
            self.programNumber = programNumber
            self.name = name
            menuItems[programNumber] = {"objectName": name, "programName":programName, "functionName":functionName}

        def run(self):
            functionName
            currentProgram = currentProgram + 1 

    class menu:
        def __init__(self):
            on_left()
            on_right()
            on_enter()
        def __del__(self):
            pass
        def on_left(self)
            while True:
                if button.left:
                    currentProgram = currentProgram - 1
                else:
                    sleep(0.01)
        def on_right(self)
            while True:
                if button.left:
                    currentProgram = currentProgram + 1
                else:
                    sleep(0.01)
        def on_enter(self)
            while True:
                if button.enter:
                    objName = menuItems[currentProgram][objectName]
                    objName.run()
                else:
                    sleep(0.01)                        
        def display(self):
            while True:
                console.text_at(menuItems[currentProgram][programName], True)
        