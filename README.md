# Overview

To run:
`python pathmaker.py`

Draw on a grid to obstruct the shortest path between two points.

## Controls

Left click					: Disable a cell

Shift + Left click	:	Enable a cell

Right click					: Increase cell height

Shift + Right click	: Decrease cell height

Spacebar						: Draw the shortest path

3										: Draw the grid in 3d

# Installation

Linux
```
$ apt-get install python3-tk
$ git clone https://github.com/lwintervold/pathmaker
$ cd pathmaker
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Windows
```
$ git clone https://github.com/lwintervold/pathmaker
$ cd pathmaker
$ python -m venv venv
$ .\venv\Scripts\activate
$ pip install --requirement .\requirements.txt
```
