import numpy as np
import argparse
import cv2
from skimage import measure
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(args["image"])
output = image.copy()
imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(imgray,(9,9),0)
ret3,thresh = cv2.threshold(blur,0,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
edged = cv2.Canny(thresh,150, 255)
cv2.imshow("output", np.hstack([imgray,thresh,edged]))
cv2.waitKey(0)

#ret, thresh = cv2.threshold(imgray, 100, 255, 0)
#thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#            cv2.THRESH_BINARY,99,2)


#cv2.imshow("cont", np.hstack([np.array(contours)]))
#cv2.imshow("edges", np.hstack([th3]))
#cv2.waitKey(0)
circles = cv2.HoughCircles(edged, cv2.HOUGH_GRADIENT, 1.805, 330, minRadius = 120, maxRadius = 190)

# detect circles in the image
#https://docs.opencv.org/3.1.0/da/d53/tutorial_py_houghcircles.html
#VERY parameter specific. This requires tweaking at the photo level and is non generalizable.
#Standardized pictures should fix this problem. We have a ~95% success rate 
#circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 1.705, 330, minRadius = 80, maxRadius = 250)
print(circles)
# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
 
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 
	# show the output image
	cv2.imshow("output", np.hstack([output]))
	cv2.waitKey(0)
