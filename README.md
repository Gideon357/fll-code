# Griffy ev2dev2 setup (2019 FLL)

## Quick Links to Docs

* [Udemy EV3](https://www.udemy.com/course/ev3-python/learn/lecture/15000204#overview) User: alex@schmelkin.com / Pass: oYjt84H,UVAZg
* [ev3dev2 Homepage](https://sites.google.com/site/ev3devpython/learn_ev3_python)
* [ev3dev2 documentation](https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/)
* [EV3Dev Device Browser](https://github.com/ev3dev/vscode-ev3dev-browser/wiki/Settings)
* [Object Oriented Python](https://youtu.be/ZDa-Z5JzLYM)

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

#### Tell your system to use the new python as default

```bash
# insert as first line of .bash_profile the export PATH setting
# created .bash_profile if it doesn't exist
ex -sc '1i|export PATH="/usr/local/opt/python/libexec/bin:$PATH"' -cx .bash_profile
```

### Create a venv for ev3dev2 programming

```bash
cd # change directory to your home dir
mkdir .venvs # directory to store all virtual environments
python3 -mvenv .venvs/ev3dev2 # create the empty environment
. .venvs/ev3dev2/bin/activate # turn on the environment
pip install --upgrade pip # upgrade pip (python package installer) to latest version
# install Python requirements including python-ev3dev2 and pylint from requirements.txt
pip install -r requirements.txt
```

NOTE: the below step was already completed in the `.vscode/settings.json` file in the git repo
In order to tell VS Code to use this venv when you're developing for ev3dev2, we store the location of the python interpreter in `.vscode/settings.json`:

```json
    "python.pythonPath": "~/.venvs/ev3dev2/bin/python3"
```

### Clone Repository

* Before cloning the repo, ensure that an [SSH key has been created](https://confluence.atlassian.com/bitbucket/set-up-an-ssh-key-728138079.html) and is in bitbucket.
* Ensure full permisions are given by repo owner.

1. Quit and reload VSCode
2. Git clone via CMD-SHIFT-P and enter repo: `git@bitbucket.org:gearheadgriffins/griffy-dev2.git`
3. Choose location in ~/Documents or wherever (not Desktop)
4. If this causes error run the same command in terminal and select yes to accept new host identifier
5. Open the Folder in VSCode

### That's it!! Congratulations, you're done

## Connect EV3 to VS Code and Internet

Follow the [bluetooth instructions at ev3dev.org](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/)

## When we need to update ev3dev Libraries without reflashing for new version

1. right click on ev3dev in EV3DEV DEVICE BROWSER
2. select SSH
3. run upgrade command below to update both python3 and micropython libraries

```bash
sudo apt update && sudo apt install python3-ev3dev2 micropython-ev3dev2
```

### How to change EV3dev2 Hostname

```bash
sudo nano /etc/hostname
```

root pass: maker

change the hostname on line 1

<kbd>CTRL</kbd>+<kbd>O</kbd>

<kbd> enter </kbd>

<kbd>CTRL</kbd>+<kbd>X</kbd>

```bash
sudo nano /etc/hosts
```

change "localhost" on the first line to the same hostname

<kbd>CTRL</kbd>+<kbd>O</kbd>

<kbd> enter </kbd>

<kbd>CTRL</kbd>+<kbd>X</kbd>

## List of Hostnames

* First Griffy: Griffy_A
* Second_Griffy: Griffy_B
* Test Brick: Test_Brick

### TODO
