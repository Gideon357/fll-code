#!/usr/bin/env micropython
from ev3dev2.console import Console
from Griffy.button import Button
from time import sleep

words = ["Paralel lines are so similar, it's a shame they never meet", "Hello World", "Gracious Proffesionalisim"]




class testMenu:
        console = Console()
        console.set_font('Lat15-TerminusBold16.psf.gz', True)

        def __init__(self):
                self.mid_col = self.console.columns // 2
                self.mid_row = self.console.rows // 2
                self.currentStr = 0


        def command_loop(self):
                self.draw_menu()
                btn = Button()
                btn.on_up = self.up_pressed()
                btn.on_down = self.down_pressed()
                while not btn.enter:
                        btn.process()
                        sleep(0.01)
        
        def up_pressed(self):
                self.currentStr = self.currentStr + 1
                self.draw_menu()

        def down_pressed(self):
                self.currentStr = self.currentStr - 1
                self.draw_menu()

        def draw_menu(self):
                """ Displays Current Strings 
                TODO: Add Multiple Options"""
                self.console.text_at(words[self.currentStr], column=self.mid_col, row=self.mid_row, True, False, alignment="C")
        
menu = testMenu()
menu.command_loop()