# Import all the necessary packages.
import argparse
import cv2
import csv

# Create an argument parser so the user can choose which video file to run the
# tracking algorithm on.
ap = argparse.ArgumentParser()
# The user will have to run the program like this: python csrt.py --video
# FILENAME.mp4
ap.add_argument("--video", type=str
                )
# Store the user entry as a key in a dictionary so that the video file name can
# be found later.
args = vars(ap.parse_args())

# Initialise frame grabbing from the video file supplied by the user.
camera = cv2.VideoCapture(args["video"])

# Set up a variable boundingBox which will initialise the bounding box and can
# be used to check whether a bounding box has been initialised yet or not.
boundingBox = None

# Initialise the CSRT tracker.
CSRT = cv2.TrackerCSRT_create()

# Create an array coords to store x and y coordinates tracked by the software.
coords = []

# Use a while loop to read all the frames in the video.
while True:
# Read the frame.
    ballTracking = camera.read()
    ballTracking = ballTracking[1] if args.get("video", False) else ballTracking
# Break the while loop at the end of the video.
    if ballTracking is None:
        break
# Only if the bounding box has already been drawn...
    if boundingBox is not None:
# ...update the CSRT tracker for the new frame...
        (success, box) = CSRT.update(ballTracking)

# ...and only if the CSRT tracker was able to detect the ball...
        if success:
# ...extract dimensions for drawing the box and draw the box onto the frame.
            (x, y, width, height) = [int(i) for i in box]
            cv2.rectangle(ballTracking, (x, y), (x + width, y + height),
                    (255, 0, 0), 3)
# Add the found x and y coordinates to the coords array.
        coords.append([x,y])

# Display the box and the frame in a window live so the user can watch to make
# sure that tracking is working smoothly.
    cv2.imshow("Ball Tracking", ballTracking)
    key = cv2.waitKey(1) & 0xFF

# The 's' key must be pressed before the user can select the bounding box.
    if key == ord("s"):
# The user selects the bounding box by dragging their mouse to create a
# rectangle on the frame window shown on the screen.
# showCrosshair makes it easier for the user to make sure the ball is at the
# centre of the box drawn.
        boundingBox = cv2.selectROI("Ball Tracking", ballTracking,
                                    fromCenter=False,
                showCrosshair=True)
# Start the CSRT tracker using the initially selected bounding box coordinates.
        CSRT.init(ballTracking, boundingBox)

# Create functionality for the user to terminate the program by pressing the
# key 'q'.
    elif key == ord("q"):
            break

# Close the window displaying the video.
cv2.destroyAllWindows()

# Open a new CSV file for editing.
with open("initialCoordsNew.csv","w") as f:
# Write the x and y coordinates to the file separating each entry by a row.
    writer = csv.writer(f,delimiter=",", lineterminator="\n")
    writer.writerows(coords)
