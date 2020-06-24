# Got Fixed Do Not Use Anymore
from ev3dev2 import is_micropython
from ev3dev2.button import Button as EV3Button


class Button(EV3Button):
    """
    Override ev3dev2.button to fix _state bug
    TODO: Pull request to fix bug at github
    """

    def __init__(self):
        super(Button, self).__init__()
        if is_micropython:
            self._state = set([])
