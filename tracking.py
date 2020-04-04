# Import all the necessary modules.
import numpy as np
import cv2
import csv

# Created an array to store all the radii calculated by the program.
radiusList = []

# Initialisation of frame grabbing from video file.
camera = cv2.VideoCapture("tf3Trim.mp4")

# Create boolean variable which can be set to True or False depending on
# whether or not the user wants to watch the algorithm working.
visualise = True

# Used as a method of making sure all frames are grabbed from the video to make
# sure the radii data is complete.
counter = 0

# Function to find radius of ball - requires a frame image.
def Radius(importedFrame):
    
# Because the cricket ball has such high contrast, we can use image thresholding
# and colour conversion to combat this.
    maxIntensity = 255
    minIntensity = 0
    threshold = 75

# Use the CLAHE algorithm to improve contrast with surroundings.
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(2,2))
    importedFrame = clahe.apply(importedFrame)

# Use the Gaussian Blur algorithm to reduce image noise.
    blurredFrame = cv2.GaussianBlur(importedFrame,(5,5),0)
# This is called slicing - the height and width of the frame in pixels can be
# found. 
    height, width = blurredFrame.shape[:2]
# To find the centre coordinates of the frame, halve the width and height of the
# frame.
    frameCentreX = round(width/2)
    frameCentreY = round(height/2)

# Find the average colour around the centre of the blurred frame.
    avgColourBall = 0.0
# We index 6 times because we calculate the average colour of six pixels
# radially from the centre of the frame.
    for dx in range(1,6):
        for dy in range(1,6):
            avgColourBall += blurredFrame[frameCentreY + dy][frameCentreX + dx]

# Adjust the tolerable brightness threshold according to the average colour of
# the ball. This therefore adapts to every situation.
    if avgColourBall > 120.0:
        threshold = 100.0
    elif avgColourBall > 100.0:
        threshold = 95.0
    elif avgColourBall > 80.0:
        threshold = min(90.0,avgColourBall)
    elif avgColourBall < 65.0:
        threshold = 65.0
    else:
        threshold = 75.0

# Set pixel values by scanning through all the pixels in the frame and checking
# against the threshold.
    for i in range(len(blurredFrame)):
        for j in range(len(blurredFrame[0])):
            if blurredFrame[i][j] < threshold:
                blurredFrame[i][j] = maxIntensity
            else:
                blurredFrame[i][j] = minIntensity

# Find the contours of the frame using the tree retrieval mode and chain
# approximation storing all points.
    contours = cv2.findContours(blurredFrame,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)[0]
# Draw the contours of all objects in the frame, drawing a 1-pixel wide outline.
    cv2.drawContours(blurredFrame, contours, -1, (255,0,0),1)


# Set up initial values for variables which will store data of points on
# circles which will be drawn around contours.
    radius = 0
    centreX = 0
    centreY = 0

# Find the contour closest to the centre.
    for contour in contours:
# Draw circles around all the objects which have contours drawn around them.
        (x,y),r = cv2.minEnclosingCircle(contour)
# Reject the point if the radius of the detected circle is far too small.
        if r < 1:
            continue
# Store the coordinates of the contour determined to be the closest to the
# centre of the frame.
        centreX = x
        centreY = y
        radius = r

# If no circles can be found, reject the frame.
    if len(contours) == 0:
        return False

    circleIndex = 0
# Out of all the circles, find the largest one and store the contour index of
# this circle.
    for i,j in enumerate(contours):
        if len(j) > len(contours[circleIndex]):
            circleIndex = i

# Find and draw an appropriate circle using the points of the specified largest
# circle.
# This circle is deemed to be a trace of the ball, so the radius of the circle
# is the radius of the ball in pixels.
    (centreX,centreY),radius = cv2.minEnclosingCircle(contours[circleIndex])
    cv2.circle(importedFrame,(int(centreX),int(centreY)),int(radius),(255,0,0),2)

    if visualise:
        cv2.imshow("Visualisation",importedFrame)
        cv2.waitKey(1)
    radiusList.append(radius)

    return True

# Create array for storing x and y coordinates.
coords = []

# Open the CSV file containing the x and y coordinates.
with open("initialCoordsNew.csv","r") as f:
    reader = csv.reader(f)
# Add all the x and y coordinates to an array.
    for row in reader:
        coords.append(row)

while counter < len(coords):
# Grab the video frame.
    (grabbed1, frame1) = cv2.VideoCapture("tf3Trim.mp4").read()
# Convert the image to grayscale as part of image thresholding.
    greyImage = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
# Make a copy of the image so that another cropped version can be made.
    imgCopy = greyImage.copy()
# We are going to crop the image so it zooms in on the ball: the image will be
# 200px x 200px.
    xBound = int(coords[counter][0]) + 200
    yBound = int(coords[counter][1]) + 200
# Crop the image.
    ballImg = imgCopy[int(coords[counter][0]): xBound,
                      int(coords[counter][1]): yBound]
# Run the radius function on the cropped image.
    found = Radius(ballImg)
# Increment the counter by 1 as this is the end of a run.
    counter += 1

# Create an array which will store x and y coordinates together with radii data.
finalCoords = []

# For all the coordinates and radii...
for i in range(len(coords)):
# ...add them all to an array, separating each entry as a separate 2D array.
    finalCoords.append([int(coords[i][0]), int(coords[i][1]),
                        round(radiusList[i])])

# Open a new CSV file for editing.
with open("finalCoords.csv","w") as f:
# Write the coords array to the CSV file.
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerows(finalCoords)
        
# Close any visualisation windows.
cv2.destroyAllWindows()
