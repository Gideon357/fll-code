# Griffy ev2dev2 setup (2019 FLL)

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

#### Install Python from Brew
```bash
brew install python
```

#### Update to use brew python over system
```bash
# add to ~/.bash_profile
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
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

## Connect EV3 to VS Code

### TODO: write instructions

## TODO

* ~~Create new code repo for meetings and non-code documentation~~
* Move meetings to new repo
