"""
This program will allow for a menu that displays all programs instead of the menu browser saving 20 seconds of time in loading.
When this is complete, we will set it to automatically run on setup by runing the "run_on_setup.sh" file
TODO:
Create code that automatically adds .py files named under certain conventions 
Add run at start
"""
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.console import Console

button = Button()
menuItems = []
a = true
displayNum = 0

while a:
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
        b = true
    def runProgram(objectName):
        objectName.run()
    def __del__(self):
        pass
    def on_left(self,state)
        while b:
            if state:
                currentProgram = currentProgram - 1
    def on_right(self,state)
        while b:
            if state:
                currentProgram = currentProgram + 1
     def on_enter(self)
        while b:
            objName = menuItems[currentProgram][objectName]
            objName.run()
    def display(self):
        while b:
            console.text_at(menuItems[currentProgram][programName], True)
    







