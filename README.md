# ball-track

Creates a visualisation similar to Hawk-Eye for a single delivery recorded in a video file.

Can be run on a much smaller budget than Hawk-Eye so potential application for use at the non-professional level.

## Instructions

Open Command Prompt in Windows and navigate to the directory the code is stored in.

Then, run `python csrt.py –video FILENAME.mp4` where FILENAME is the name of the video file with the test footage (e.g. tf3Trim.mp4). You have to draw a bounding box around the cricket ball during the video, and make sure that the ball is always inside the bounding box. If not, then run again until it is. Draw the bounding box by pressing the 's' key when the ball comes into view. This pauses the video until you draw the box and press Enter.

Run `python tracking.py` and wait patiently for the program to finish.

Finally, run `python 3d.py` and the visualisation should open. You can hold ctrl and drag your mouse to change view, or hold alt and drag to adjust zoom.

If using the test footage uploaded to the GitHub, please use these settings in 3d.py and tracking.py (if not, then you will have to adjust these settings yourselves by finding out the largest and smallest values of your regressed radii, and by finding a suitable way of setting the scales to reflect how much tracking is missed in your video):

**tf3Trim.mp4:**

In line 34, `startRadius = 143.6`

In line 35, `endRadius = 119.8`

In line 49, `scale = [0.5,1950]`

In line 97, `zlist.append(z*scale[1]+62)`

**tf2Trim.mp4:**

In line 34, `startRadius = 142.0`

In line 35, `endRadius = 99.7`

In line 49, `scale = [0.5,1800]`

In line 97, `zlist.append(z*scale[1]+212)`

## Prerequisites

- OpenCV
- NumPy
- VPython 7
- Windows
