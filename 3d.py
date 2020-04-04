# Import all the necessary modules, including linReg which is a Python script
# which should be in the same folder as this file.
from vpython import *
import csv
import linReg

# Set up data structures for storing radii and coordinates imported and scaled
# from the tracking file.
xlist = []
ylist = []
zlist = []
rlist = []

# All dimensions are in cm and are based off real-life dimensions.
# Define dimensions of the pitch to be used in visualisation and scaling of
# coordinates.
creaseLength = 122
pitchWidth = 305.0
pitchLength = 2012.0
pitchThickness = 10

# Store wicket dimensions for the visualisation.
wicketHeight = 71.1
wicketWidth = 22.86
stumpWidth = 4.5

# wideWidth is set to the width of the whole crease on the visualisation.
# lineWidth is set to the width of the actual crease line itself on the
# visualisation.
wideWidth = 264
lineWidth = 5

# Manually define start and end position radii of the ball.
startRadius = 143.6
endRadius = 119.8

# Define the radius of the ball for the visualisation so spheres can be drawn
# to the correct size.
ballRadius = 5
# Set up  a variable FY, the value of which comes from camera intrinsics.
FY = 1520.0

# Create a scaling index for use later when plotting detected data in the
# visualisation.
# scale[1] represents the z axis length of the pitch from the point where
# tracking starts to the stump. It is less than the whole length (2012.0).
# 0.5 is a scaling factor which is part of the conversion between the two
# different coordinate bases - the pixel system and the visualisation system.
scale = [0.5, 1950]

# Create a variable xWaste which is adjusted during testing to make the trail
# fit to the pitch correctly.
xWaste = 690

# Open the file from where the detected coordinates will be read.
with open("finalCoords.csv","r") as f:   
    reader = csv.reader(f)
# Extract x and y coordinates as well as the radius data for each row...
    for row in reader:
        r = float(row[2])
# The x coordinates are adjusted using variable xWaste, and are scaled as part
# of the conversion between the two different coordinate bases.
# 152 is also subtracted from the coordinates, as the centre in the new
# visualisation space is defined as the centre of the pitch, but the ball is
# released from the edge of the pitch - 152 is half the pitch width.
        x = ((float(row[0])-xWaste)*305/500)-152
# 720 is defined as the highest possible y coordinate which could be read in,
# so the y coordinates are first adjusted to reflect 720 as being the new 0,
# as all y coordinates need to be inverted, and then the coordinates are
# scaled for the conversion between the two bases.
        y = (720.0-float(row[1]))*scale[0]
# ...and after extracting them, store them in three separate arrays in order.
        xlist.append(x)
        ylist.append(y)
        rlist.append(r)
# We need to run the linear regression script on the imported radii before we
# can use them to calculate z axis data.
# All coordinates stored in rlist are read into the program.
r_new = linReg.linReg(rlist)
# After calculating the new regressed radii, clear the old rlist...
rlist = []
# ...and write all the new regressed radii to the list instead.
for i in range(len(xlist)):
    rlist.append(r_new[i])

# Now, to get initial z axis coordinates, import all the radii...
for i,radius in enumerate(rlist):
# ...and calculate how far down the pitch the ball is by dividing how much the
# radius has changed by how much it will change by the time it has reached the
# end of the pitch.
    z = abs((startRadius-radius)/(startRadius-endRadius))
# After working out this fraction, calculate z axis coordinates by multiplying
# the fraction by the length of pitch travelled during tracking.
# This length is not the entire pitch length, as tracking starts after the ball
# is released, so we add the difference between the pitch length and where
# tracking starts to the coordinates.
    zlist.append(z*scale[1]+62)

# We are now going to start drawing and creating the visualisation environment
# using VPython.
# Set up the window which will display the visualisation.
# Resolution: 1280 x 720, the name of the window is "HawkEye", range=800 means
# the window is focused on the area +/- 400 of the centre, the colour of the
# background is black, we define the centre of the frame as (0,0,0) around
# which we can rotate.
visualisation = canvas(title="HawkEye", width=1280, height=720, range=800,
                       background=vector(0,0,0), center=vector(0,0,0))
# Adjust the view the user sees when they open the visualisation so they see a
# keeper-like view by default.
# The perspective can be changed by holding down ctrl and dragging the mouse.
visualisation.forward = vector(-1,-0.05,0)

# Draw the ground.
# The first line draws the clay, straw-coloured strip in the centre. Dimensions:
# slightly longer and thicker than pitch dimensions to make sure everything fits
# nicely together.
strip = box(pos=vector(0,0,0), size=vector(pitchLength*1.2,pitchThickness*1.2,
                                           pitchWidth),
            color=vector(0.97,0.94,0.6))
# The second line draws the grass around the strip. Dimensions: slightly longer
# than the length of the pitch by twice the width of the pitch by thickness of
# pitch.
grass = box(pos=vector(0,0,0), size=vector(pitchLength*1.25,pitchThickness,
                                           pitchWidth*2),
            color=vector(0.2,0.7,0.27))
# The third line draws a rectangle between the two wickets on the strip,
# indicating that if the ball bounces here, it is in line with the stumps.
# Dimensions: length of pitch by width of the wickets by thickness of pitch,
# but slightly longer and thicker to make sure everything fits nicely together,
# colour: red.
stumpLine = box(pos=vector(0,0,0), size=vector(pitchLength,pitchThickness*1.3,
                                               wicketWidth), color=vector(1,0,0),
                opacity=0.8)


# Draw wickets and crease lines at the both sides of the pitch, using the same
# structure, but adjusting the position vectors accordingly.

# Draw wickets as three individual cuboids, with predefined dimensions and
# colour them blue. They are all positioned in line with each other, half a
# pitch length away from the centre, all of the same height, equally wide apart.
battingStump1 = box(pos=vector(pitchLength/2,wicketHeight/2,
                               -(wicketWidth/2-stumpWidth/2)),
                    size=vector(5,wicketHeight,stumpWidth), color=color.blue)
battingStump2 = box(pos=vector(pitchLength/2,wicketHeight/2,0),
                    size=vector(5,wicketHeight,stumpWidth), color=color.blue)
battingStump3 = box(pos=vector(pitchLength/2,wicketHeight/2,
                               (wicketWidth/2-stumpWidth/2)),
                    size=vector(5,wicketHeight,stumpWidth), color=color.blue)

bowlingStump1 = box(pos=vector(-pitchLength/2,wicketHeight/2,
                               -(wicketWidth/2-stumpWidth/2)),
                    size=vector(5,wicketHeight,stumpWidth), color=color.blue)
bowlingStump2 = box(pos=vector(-pitchLength/2,wicketHeight/2,0),
                    size=vector(5,wicketHeight,stumpWidth), color=color.blue)
bowlingStump3 = box(pos=vector(-pitchLength/2,wicketHeight/2,
                               (wicketWidth/2-stumpWidth/2)),
                    size=vector(5,wicketHeight,stumpWidth), color=color.blue)

# Draw the crease lines: they are all white, all have the same width, and are
# accurately and evenly drawn around the stumps. They are drawn in identical
# pairs through the use of constants. Where constants aren't used, appropritate
# numerical dimensions are chosen.
line1 = box(pos=vector(pitchLength/2,pitchThickness/2,0),
            size=vector(lineWidth,5,wideWidth), color=color.white)
line2 = box(pos=vector(pitchLength/2,pitchThickness/2,132),
            size=vector(244,5,lineWidth), color=color.white)
line3 = box(pos=vector(pitchLength/2,pitchThickness/2,-132),
            size=vector(244,5,lineWidth), color=color.white)
line4 = box(pos=vector(pitchLength/2-122,pitchThickness/2,0),
            size=vector(lineWidth,5,366), color=color.white)

line1 = box(pos=vector(-pitchLength/2,pitchThickness/2,0),
            size=vector(lineWidth,5,wideWidth), color=color.white)
line2 = box(pos=vector(-pitchLength/2,pitchThickness/2,132),
            size=vector(244,5,lineWidth), color=color.white)
line3 = box(pos=vector(-pitchLength/2,pitchThickness/2,-132),
            size=vector(244,5,lineWidth), color=color.white)
line4 = box(pos=vector(-pitchLength/2+122,pitchThickness/2,0),
            size=vector(lineWidth,5,366), color=color.white)

# Create an array to store all the visualised balls in.
balls = []

# Create a variable storing the total number of coordinates, making iteration
# easier later.
noDetectedPoints = len(xlist)

# Set up a variable FX, the value of which comes from camera intrinsics.
FX = 350

# Initialise yTrail and zTrail variables.
yTrail = ylist[0]*FY/(FY+zlist[0])
zTrail = xlist[0]*zlist[0]/(FX+zlist[0])

# Create an array to store the position coordinates for the balls.
coords3D = []

# For all the x and y coordinates...
for i in range(len(xlist)):
# ...scale both using the perspective projection formula...
    yTrail = ylist[i]*FY/(FY+zlist[i])
    zTrail = xlist[i]*zlist[i]/(FX+zlist[i])
# ...and add them both, alongside the depth coordinates.
    coords3D.append((zlist[i]-((pitchLength-2*creaseLength)/2), yTrail, zTrail))

# Draw all the stored balls.
for idx in range(noDetectedPoints):
# If the balls are within the range of view...
    if coords3D[idx][0] > -400:
# ...plot them as magenta spheres using the saved coordinates.
        balls.append(sphere(pos=vector(coords3D[idx][0],coords3D[idx][1],
                                       coords3D[idx][2]), radius=ballRadius,
                            color=vector(1,0,1)))
# Create cylindrical-shaped path for the ball to make it easier for user to
# view.
# We find displacement for x, y and z directions. Displacement is calculated
# by finding the difference in position of the ball between two consecutive
# frames throughout the video.
# The cylinder shape is then plotted using this displacement.
        if idx > 0:
            displacement = vector(coords3D[idx][0]-coords3D[idx-1][0],
                                  coords3D[idx][1]-coords3D[idx-1][1],
                                  coords3D[idx][2]-coords3D[idx-1][2])
            cylinder(pos=vector(coords3D[idx-1][0], coords3D[idx-1][1],
                                coords3D[idx-1][2]), axis=displacement,
                     radius=ballRadius, color=vector(1,0,1), opacity=0.3)


### Initially set lowY to a high y value as it will be used to find the lowest y
### value.
##lowY = 1000
### This variable will store the index of the bouncing point within the coords
### array.
##lowYIndex = 0
##
### Out of all the detected points...
##for idx in range(noDetectedPoints):
### ...if the y value of any of these points is less than the current lowest y...
##    if coords3D[idx][1] < lowY:
### ...update lowY with this new y value and lowYIndex with the index of the point.
##        lowY = coords3D[idx][1]
##        lowYIndex = idx
### Draw the bouncing point of the ball using the index that was found.
##bounceBall = sphere(pos=vector(coords3D[lowYIndex][0],coords3D[lowYIndex][1],
##                                       coords3D[lowYIndex][2]),
##                    radius=ballRadius,color=vector(1,0,1))
