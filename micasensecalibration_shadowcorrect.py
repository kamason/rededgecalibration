# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 14:38:34 2017

@author: kmason
"""
import numpy
import cv2
import math
import os
from skimage.io import imread
from libtiff import TIFFimage

illband1 = input("Illuminated Target Band 1 Path: ")
illband2 = input("Illuminated Target Band 2 Path: ")
illband3 = input("Illuminated Target Band 3 Path: ")
illband4 = input("Illuminated Target Band 4 Path: ")
illband5 = input("Illuminated Target Band 5 Path: ")
sband1 = input("Shadowed Target Band 1 Path: ")
sband2 = input("Shadowed Target Band 2 Path: ")
sband3 = input("Shadowed Target Band 3 Path: ")
sband4 = input("Shadowed Target Band 4 Path: ")
sband5 = input("Shadowed Target Band 5 Path: ")
illref1 =  input("Panel Reflectance Value for Band 1:")
illref2 = input("Panel Reflectance Value for Band 2:")
illref3 = input("Panel Reflectance Value for Band 3:")
illref4 = input("Panel Reflectance Value for Band 4:")
illref5 = input("Panel Reflectance Value for Band 5:")
img_dir = input("Image Directory:")
save_dir = input("Save Path:")

#read panel images and calculate LUT for each band 
 
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
 
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)

# load the image, clone it, and setup the mouse callback function
image = imread(illband1)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
    
cv2.destroyAllWindows() 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	roi1 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
 
# load the image, clone it, and setup the mouse callback function
image = imread(illband2)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
   
cv2.destroyAllWindows()
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	roi2 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]

image = imread(illband3)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
    
cv2.destroyAllWindows() 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	roi3 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
image = imread(illband4)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
    
cv2.destroyAllWindows() 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	roi4 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
image = imread(illband5)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
    
cv2.destroyAllWindows() 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	roi5 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
    
refPt = []
cropping = False
 
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)

# load the image, clone it, and setup the mouse callback function
image = imread(sband1)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
    
cv2.destroyAllWindows() 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	rois1 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
 
# load the image, clone it, and setup the mouse callback function
image = imread(sband2)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
   
cv2.destroyAllWindows()
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	rois2 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]

image = imread(sband3)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
    
cv2.destroyAllWindows() 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	rois3 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
image = imread(sband4)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
    
cv2.destroyAllWindows() 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	rois4 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
image = imread(sband5)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
    
cv2.destroyAllWindows() 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	rois5 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]

# calculate y int for each band previously using dark and light panel
# this value will be consistant
# yint1 =
# yint2 = 
# yint3 = 
# yint4 = 
# yint5 =  

DCp1i = numpy.mean(roi1)
DCp2i = numpy.mean(roi2)
DCp3i = numpy.mean(roi3)
DCp4i = numpy.mean(roi4)
DCp5i = numpy.mean(roi5)
DCp1s = numpy.mean(rois1)
DCp2s = numpy.mean(rois2)
DCp3s = numpy.mean(rois3)
DCp4s = numpy.mean(rois4)
DCp5s = numpy.mean(rois5)
pp1 = -1 * math.log(illref1)
pp2 = -1 * math.log(illref2)
pp3 = -1 * math.log(illref3)
pp4 = -1 * math.log(illref4)
pp5 = -1 * math.log(illref5)
mi1 = (pp1-yint1/DCp1i)
mi2 = (pp2-yint2/DCp2i)
mi3 = (pp3-yint3/DCp3i)
mi4 = (pp4-yint4/DCp4i)
mi5 = (pp5-yint5/DCp5i)
ms1 = (pp1-yint1/DCp1s)
ms2 = (pp2-yint2/DCp2s)
ms3 = (pp3-yint3/DCp3s)
ms4 = (pp4-yint4/DCp4s)
ms5 = (pp5-yint5/DCp5s)


#loop through all images in folder
for filename in os.listdir(img_dir):
    os.chdir(img_dir)
    f = imread(filename)
    x = copy.copy(f)
    if filename[-6:]=='_1.tif':
        # determine otsus threshold for shadow for each 
        img = cv2.imread(filename,0)
        ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh = ret2 * 256
        f[f<thresh]=0 #shadowed pixels
        x[x>=thresh]=0 #illuminated pixels
        f =ms1*f+yint1 #calibrate shadowed regions using equation for shadowed panel
        x = mi1*x+yint1 #calibrate illuminated regions using equaiton for illuminated panel
        f[f==yint1]=0
        x[x==yint1]=0
        y = f + x
        z = math.exp(y*-1)
        name = filename[:-6]+'ref_1.tif'
    elif filename[-6:]=='_2.tif':
        img = cv2.imread(filename,0)
        ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh = ret2 * 256
        f[f<thresh]=0 #shadowed pixels
        x[x>=thresh]=0 #illuminated pixels
        f =ms2*f+yint2 #calibrate shadowed regions using equation for shadowed panel
        x = mi2*x+yint2 #calibrate illuminated regions using equaiton for illuminated panel
        f[f==yint2]=0
        x[x==yint2]=0
        y = f + x
        z = math.exp(y*-1)
        name = filename[:-6]+'ref_2.tif'
    elif filename[-6:]=='_3.tif':
        img = cv2.imread(filename,0)
        ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh = ret2 * 256
        f[f<thresh]=0 #shadowed pixels
        x[x>=thresh]=0 #illuminated pixels
        f =ms3*f+yint3 #calibrate shadowed regions using equation for shadowed panel
        x = mi3*x+yint3 #calibrate illuminated regions using equaiton for illuminated panel
        f[f==yint3]=0
        x[x==yint3]=0
        y = f + x
        z = math.exp(y*-1)
        name = filename[:-6]+'ref_3.tif'
    elif filename[-6:]=='_4.tif':
        img = cv2.imread(filename,0)
        ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh = ret2 * 256
        f[f<thresh]=0 #shadowed pixels
        x[x>=thresh]=0 #illuminated pixels
        f =ms4*f+yint4 #calibrate shadowed regions using equation for shadowed panel
        x = mi4*x+yint4 #calibrate illuminated regions using equaiton for illuminated panel
        f[f==yint4]=0
        x[x==yint4]=0
        y = f + x
        z = math.exp(y*-1)
        name = filename[:-6]+'ref_4.tif'
    elif filename[-6:]=='_5.tif':
        img = cv2.imread(filename,0)
        ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh = ret2 * 256
        f[f<thresh]=0 #shadowed pixels
        x[x>=thresh]=0 #illuminated pixels
        f =ms2*f+yint5 #calibrate shadowed regions using equation for shadowed panel
        x = mi2*x+yint5 #calibrate illuminated regions using equaiton for illuminated panel
        f[f==yint5]=0
        x[x==yint5]=0
        y = f + x
        z = math.exp(y*-1)
        name = filename[:-6]+'ref_5.tif'
    newimg = TIFFimage(z, description='')
    newimg.write_file(name, compression='lzw')
#save new images with reflectance values in new folder
#copy exif information from original image
