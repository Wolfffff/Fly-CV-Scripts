import numpy as np import argparse import imutils import cv2 import os
import warnings
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dir", required = True, help = "Path to the image")
args = vars(ap.parse_args())


def calculateHoughCircles(fileName):
    # load the image, clone it for output
    image = cv2.imread(fileName)
    if (image.shape[0] > image.shape[1]):
        image = imutils.rotate_bound(image, 90)
    output = image.copy()

    height,width,depth = image.shape

    #Grayscale
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Gaussian blur
    blur = cv2.medianBlur(imgray,23)
    #Thresh
    ret1,thresh1 = cv2.threshold(blur,0,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
    ret2,thresh = cv2.threshold(blur,(ret1 - 12),255,cv2.THRESH_TOZERO)
    
    edged = cv2.Canny(thresh, 0, 255)

    #Crop image
    cropped = np.zeros((height, width), np.uint8)
    cropped[250:(height - 250), 250:(width - 250)] = -1

    masked = cv2.bitwise_and(edged, edged, mask=cropped)
    
    circles = cv2.HoughCircles(masked, cv2.HOUGH_GRADIENT, 3.6, 320, minRadius = 120, maxRadius = 160)
    
    # detect circles in the image
    #https://docs.opencv.org/3.1.0/da/d53/tutorial_py_houghcircles.html
    #VERY parameter specific. This requires tweaking at the photo level and is non generalizable.
    #Standardized pictures should fix this problem. We have a ~95% success rate 
    # ensure at least some circles were found
    #First check for 96 wells
    if circles.shape[1] != 96:
        warnings.warn("96 wells were not detected")

    sorted = np.empty((8,12))
    temp = 0
    if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            circ = circles.tolist()
            circ.sort(key=lambda x: x[1])
            #Hardcode list structure - rows on horizontals
            Lists = [[] for _ in range(8)]
            Lists[0] = circ[0:12]
            Lists[1] = circ[12:24]
            Lists[2] = circ[24:36]
            Lists[3] = circ[36:48]
            Lists[4] = circ[48:60]
            Lists[5] = circ[60:72]
            Lists[6] = circ[72:84]
            Lists[7] = circ[84:96]
            for l in Lists:
                print(len(l))
                if(len(l) != 12):
                    warnings.warn("Wrong count of wells in a row")
                l.sort(key = lambda x: x[0])

            for i in range(8):
                for n in range(0, 11):
                        (x,y,r) = Lists[i][n]
                        xo = np.round(x).astype("int")
                        yo = np.round(y).astype("int")
                        yo = np.round(r).astype("int")

                        crop = output[(y-r):(y+r),(x-r):(x+r)]
                        crop_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                        ret,threshCrop1 = cv2.threshold(crop_gray,0,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
                        ret, threshCrop = cv2.threshold(crop_gray, (ret-20), 255, cv2.THRESH_TOZERO)

                        ret2, tc2 = cv2.threshold(threshCrop,1,255, cv2.THRESH_BINARY_INV)

                        height,width = 2*r, 2*r
                        mask = np.zeros((height,width), np.uint8)
                        cv2.circle(mask,(r,r),(r-25),(255,255,255),thickness=-1)
                        out = threshCrop*mask
                        white = 255-mask
                        new_im = out + white
                        masked_data = cv2.bitwise_and(tc2, tc2, mask=mask)
                        new_im = masked_data

                        image, contours, hierarchy = cv2.findContours(masked_data, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        contour_list = []
                        for contour in contours:
                            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
                            area = cv2.contourArea(contour)
                            (x, y), radius = cv2.minEnclosingCircle(contour)

                            if (len(approx) > 8) & (area > 1000) & (3.1415*(radius**2)/5 < area):
                                contour_list.append(contour)

                        cv2.drawContours(masked_data, contour_list, -1, (50,50,50), 3)
                        cv2.circle(output, (xo, yo), ro, (0, 255, 0), 4)
                        
            cv2.imshow("output", np.hstack([output]))
            cv2.waitKey(0)
    return

for file in os.listdir(args[0]):
    if file.endswith(".tiff"):
        print(os.path.join(args[0], file))
        calculateHoughCircles(os.path.join(args[0], file))

