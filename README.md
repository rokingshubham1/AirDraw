# AirDraw

Computer vision aided virtual board implemented with OpenCV


We will be using the computer vision techniques of OpenCV to build this project. The preffered language is python due to its exhaustive libraries and easy to use syntax but understanding the basics it can be implemented in any OpenCV supported language.

this virtual board have very low-cost hardware requirement, usually accessible in our daily lives, for an easy installation: a webcam-equipped computer, and an LED pointing device known as AirPen.
AirDraw uses computer vision techniques for detecting the pointing device and tracking its trajectory or locus to write on the screen. This facilitates its user to literally write on the air, no need of pads or any other hardware.

## Acknowledgements

 - [Ai Python video games](https://www.linkedin.com/posts/nihal-sinha-9946a41b6_ai-python-videogames-ugcPost-6845702251315552256-IG2P)
 - [LCD Writing Tablet](https://youtu.be/vWS85tHfmFk)


## System Requirements



•	Computer/Processor: 90MHz or higher processor

•	Memory: 256 RAM (128 recommended)

•	Operating System: Windows operating systems

•	Peripheral/Miscellaneous: Mouse, Keyboard, Webcam


## Algorithm
The algorithm that we have used here for processing and the functionalities to add so here’s a breakdown of each step of our application.

1.	Find the color range of the target object and save it.
2.	Apply the correct morphological operations to reduce noise in the video
3.	Detect and track the colored object with contour detection.
4.	Find the object’s x,y location coordinates to draw on the screen.
5.	Add a Wiper functionality to wipe off the whole screen.
6.	Add a Saving Functionality to save the page drawn on the white sheet.
7.	Add an Eraser Functionality to erase parts of the drawing.

## Installation

Download this repository by clicking the green button on the upper right corner.

or for advanced users.

```bash
  git clone https://github.com/SkandTiwari/AirDraw.git
```
this project requires python 3.6 or above to run, make sure to install latest version of python.
if already installed please check it's version by typing following in CLI. 
```bash
  python --version
```
commands for installing packages and dependencies.

1. openCV
```bash
  pip install opencv-python
```
2. Numpy
```bash
pip install numpy
```
3. tkinter for GUI
```bash
pip install tk
```
or
```bash
pip install python-tk
```

## Screenshots

[![gif-1.gif](https://i.postimg.cc/C1bGNGP4/gif-1.gif)](https://postimg.cc/TLY52DXy)
white board
[![gif-2.gif](https://i.postimg.cc/1XCfc4QH/gif-2.gif)](https://postimg.cc/sGWj3j1Q)
color and hue settings
[![gif-3.gif](https://i.postimg.cc/tgppJp0C/gif-3.gif)](https://postimg.cc/BjYdwWQd)
camboard
[![Screenshot-68.png](https://i.postimg.cc/kMfFGGth/Screenshot-68.png)](https://postimg.cc/Dm4bY26q)
main menu
