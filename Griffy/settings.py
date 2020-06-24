# TODO: display boolean state on the screen for DEBUG and GYRO -- need to see if gyro is on or off!

import errno
import json
import os


class Settings:
    """
    Settings class used to read
    write settings to a json file
    filename required
    """

    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            raise Exception("Settings file not found: {}".format(filename))
        with open(filename, "r") as json_file:
            self.settings = json.load(json_file)

    def write(self):
        """
        Write to the json file
        """
        with open(self.filename, "w") as json_file:
            json.dump(self.settings, json_file, indent=4, sort_keys=True)

    def get(self, setting, default=None):
        """
        Return `setting` from self.settings
        If it does not exist, return default value if passed
        """
        return self.settings.get(setting, default)
