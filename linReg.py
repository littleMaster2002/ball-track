# Import all the necessary modules.
import numpy as np

# We are going to define a regression function which takes all the saved radii
# as an argument.
def linReg(importedRadii):
# Initialisation of variables and arrays.
    frameNoCounter = 0
    radii = []
    frameNos = []
    weights = []
# Import all radii as radius...
    for radius in importedRadii:
# ...and add them to the radii array.
        radii.append(radius)
        frameNos.append(frameNoCounter)
# We apply different weights to the data held in radii depending on how close
# the ball is when the radius is measured.
# This is because points with large error variance require smaller weights and
# vice versa.
        if frameNoCounter < len(importedRadii)/4:
            weights.append(3)
        elif frameNoCounter < len(importedRadii)/2:
            weights.append(2)
        else:
            weights.append(1)
# Increment frameNoCounter by 1 at the end of processing each piece of data.
        frameNoCounter += 1
# We use least squares polynomial fit - this minimises the squared error.
# We are fitting a polynomial curve of degree 1 to the frame numbers and the
# radii.
    polynomialFit = np.polyfit(frameNos, radii, 1, None, False, weights, False)
# Extract the polynomial expression.
    polynomialExpression = np.poly1d(polynomialFit)

# Then we substitute our x values (frame number) into the polynomial
# expression and the y values are returned.
    finalX = frameNos
    finalY = polynomialExpression(finalX)
    return finalY
