#!/usr/bin/env micropython
import griffy
import numpy
from ev3dev2.console import Console
from griffy.button import Button 

currentProgram = 0
btn = Button() 

def bar():
    print("it works")

def foo():
    print("IT WORKS")

objects = [{"name":"foo","function":foo(), 'number':'1'}, 
{"name":"bar", "function":bar(), "number":'0'},
]

newObjects = numpy.asarray(objects)

for i in range(len(objects)):
    print(objects[i]["name"])

def on_up(state):
    if state:
        currentProgram = currentProgram + 1
        shiftValue = objects.qsize(objects) - currentProgram
        objects.roll(newObjects, shiftValue)
        print(">" + newObjects[0]["name"] + "\n")
        for i in range(0, int(len(objects) + 1)):
            print(newObjects[i]["name"] + "\n")

def on_down(state):
    if state:
        currentProgram = currentProgram - 1
        shiftValue = objects.qsize(objects) - currentProgram
        negShift = int("-" + str(shiftValue))
        objects.roll(newObjects, negShift)
        print(">" + newObjects[0]["name"] + "\n")
        for i in range(0, int(len(objects) + 1)):
            print(newObjects[i]["name"] + "\n")

def on_enter(state):
    if state:
        objects[currentProgram]["function"]
        currentProgram = currentProgram + 1
        print(">" + newObjects[0]["name"] + "\n")
        for i in range(0, int(len(objects) + 1)):
            print(newObjects[i]["name"] + "\n")

def commandLoop():
    btn.on_down = on_down()
    btn.on_enter = on_enter()
    btn.on_up = on_up()

if __name__ == "__main__":
    commandLoop()