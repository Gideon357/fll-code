#!/usr/bin/env micropython
from ev3dev2.console import Console
from Griffy.button import Button
from time import sleep

words = ["Paralel lines are so similar, it's a shame they never meet", "Hello World", "Gracious Proffesionalisim"]




class testMenu:
        console = Console()
        console.set_font('Lat15-TerminusBold16.psf.gz', True)
        btn = Button()

        def __init__(self):
                self.mid_col = self.console.columns // 2
                self.mid_row = self.console.rows // 2
                self.currentStr = 0

        def command_loop(self):
                self.draw_menu()
                self.btn.on_up = self.up_pressed()
                self.btn.on_down = self.down_pressed()
                while not self.btn.enter:
                        self.btn.process()
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
                self.console.text_at(words[self.currentStr], column=self.mid_col, row=self.mid_row, reset_console=True, inverse=False, alignment="C")
                        
menu = testMenu()
menu.command_loop()

#!/usr/bin/env python3
from ev3dev2.button import Button
from ev3dev2.sound import Sound

btn = Button()
sound = Sound()

btn.wait_for_bump('left')
sound.beep()
btn.wait_for_pressed(['up', 'down'])
sound.beep()
btn.wait_for_released('right')
sound.beep()
