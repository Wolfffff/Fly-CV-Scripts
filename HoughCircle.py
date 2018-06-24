import numpy as np
import argparse
import cv2
from skimage import measure
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())



def calculateHoughCircles(fileName):
    # load the image, clone it for output
    image = cv2.imread(fileName)
    output = image.copy()
    
    #Grayscale
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Gaussian blur
    blur = cv2.GaussianBlur(imgray,(5,5),0)
    #Thresh
    #thresh1 =  cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #cv2.THRESH_BINARY_INV,11,2)
    ret,thresh = cv2.threshold(blur,0,230,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
    #kernel = np.ones((5,5),np.uint8)
    #Consider dilation
    #dilation = cv2.dilate(blur,kernel,iterations = 3)
    edged = cv2.Canny(thresh, 100, 255)

    #Check
    #cv2.imshow("output", np.hstack([imgray,edged]))
    #cv2.waitKey(0)
    circles = cv2.HoughCircles(edged, cv2.HOUGH_GRADIENT, 1.805, 330, minRadius = 120, maxRadius = 190)

    # detect circles in the image
    #https://docs.opencv.org/3.1.0/da/d53/tutorial_py_houghcircles.html
    #VERY parameter specific. This requires tweaking at the photo level and is non generalizable.
    #Standardized pictures should fix this problem. We have a ~95% success rate 
    # ensure at least some circles were found
    total = []
    if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
     
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    #cv2.imshow("test", np.hstack([crop_img]))
                    #print((x-r),(x+r),(y-r),(y+r))
                    crop = output[(y-r):(y+r),(x-r):(x+r)]
                    cropGray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                    ret,threshCrop = cv2.threshold(cropGray,0,230,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
                    height,width = 2*r, 2*r
                    mask = np.zeros((height,width), np.uint8)
                    cv2.circle(mask,(r,r),(r-25),(255,255,255),thickness=-1)
 #                  cv2.imshow("crop", threshCrop)
                    out = threshCrop*mask
                    white = 255-mask
                    newIm = out + white
                    ret,secondThresh = cv2.threshold(newIm,60,255,cv2.THRESH_BINARY)
                    cv2.imshow("out", secondThresh)
                    

 
                    #frame, contours, hierarchy = cv2.findContours(threshCrop, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
                    #print(contours)
                    #cv2.drawContours(threshCrop, contours, -1, (50,50,50), 10)
                    #cv2.imshow("crop", threshCrop)
                    #cv2.imshow("crop", crop)
                    cv2.waitKey(0)
                    #cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                    #cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
     
            # show the output image
            #cv2.imshow("output", np.hstack([output]))
            #cv2.waitKey(0)
    return
calculateHoughCircles(args["image"])
