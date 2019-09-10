# Griffy ev2dev2 setup (2019 FLL)

## Quick Links to Docs

* [ev3dev2 Homepage](https://sites.google.com/site/ev3devpython/)
* [ev3dev2 documentation](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/)

## Setting up VS Code + Python

### Visual Studio Code

Roughly followed [vscode-hello-python](https://github.com/ev3dev/vscode-hello-python)

* Download and install [Visual Studio Code](https://code.visualstudio.com/download)
* Add Extensions:
  * ev3dev-browser (by ev3dev) - used to load programs to EV3
  * markdownlint - used to check syntax in Markdown files
  * Python

### Install Homebrew, the OS X Package Manager

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### Install Python 3

```bash
brew install python
```

### Create a venv for ev3dev2 programming

```bash
cd # change directory to your home dir
mkdir .venvs # directory to store all virtual environments
python -mvenv .venvs/ev3dev2 # create the empty environment
. .venvs/ev3dev2/bin/activate # turn on the environment
pip install --upgrade pip # upgrade pip (python package installer) to latest version
pip install python-ev3dev2 # install to OS X the ev3dev2 libraries for command completion
```

In order to tell VS Code to use this venv when you're developing for ev3dev2, we store the location of the python interpreter in .vscode/settings.json (already saved in git):

```json
    "python.pythonPath": "~/.venvs/ev3dev2/bin/python3"
```

## Connect EV3 to VS Code and Internet

Follow the [bluetooth instructions at ev3dev.org](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/)

## Update ev3dev Libraries

1. right click on ev3dev in EV3DEV DEVICE BROWSER
2. select SSH
3. run upgrade command below to update both python3 and micropython libraries

```bash
sudo apt update && sudo apt install python3-ev3dev2 micropython-ev3dev2
```

## TODO

* Create new code repo for meetings and non-code documentation
