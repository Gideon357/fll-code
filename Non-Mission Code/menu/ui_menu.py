import gi

gi.require_version('Ev3devKit', '0.5')
from gi.repository import Ev3devKit
gi.require_version('Grx', '3.0')
from gi.repository import Grx
gi.require_version('GObject', '2.0')
from gi.repository import GObject

def __init__(self):
    """Creates a new instance of a demo window."""

    Ev3devKit.UiWindow.__init__(self)

    menu = Ev3devKit.UiMenu.new()
    menu.set_padding_right(10)
    menu.set_padding_left(10)
    self.add(menu)

def add_object(name,func):
    name = Ev3devKit.UiMenuItem    
    name.get_button().connect('pressed', func)
    menu.add_menu_item(name)


def resto():
    print("IT WORKS")

def foo():
    print("bar")

add_object("ya", resto)
add_object("pa", foo)

