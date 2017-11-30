#Python code for performing an Empirical Line Calibration on MicaSense RedEdge imagery
#Minimum requirements: image of at least 1 calibration target taken before or after mission &
#reflectance values corresponding to the MicaSense RedEdge bands for each of the calibration targets

import numpy
import time
import cv2
import math
import os
from skimage.io import imread
from libtiff import TIFFimage
from osgeo import gdal
from scipy import stats
import PIL
import Tkinter
import tkFileDialog
from Tkinter import *


# generating empty lists for the target image paths and reflectance values to be referenced later
caltarref1 = []
caltarref2 = []
caltarref3 = []
caltarref4 = []
caltarref5 = []

#get user input
def take():
    numtars = int(e1.get())
    e1.delete(0,END)
    numtarslist.append(numtars)
    master.destroy ()
    return

#get user input
def take2():
    # assigning variables to the user inputs
    ref1 = float(e2.get())
    caltarref1.append(ref1)
    ref2 = float(e3.get())
    caltarref2.append(ref2)
    ref3 = float(e4.get())
    caltarref3.append(ref3)
    ref4  = float(e5.get())
    caltarref4.append(ref4)
    ref5  = float(e6.get())
    caltarref5.append(ref5)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)
    e6.delete(0,END)
    master.destroy()
    return


    
master = Tk()
master.title("Empirical Line Calibration for MicaSense RedEdge Imagery")
Label(master, text="Reflectance Value Band 1:").grid(row=2)
Label(master, text="Reflectance Value Band 2:").grid(row=4)
Label(master, text="Reflectance Value Band 3:").grid(row=6)
Label(master, text="Reflectance Value Band 4:").grid(row=8)
Label(master, text="Reflectance Value Band 5:").grid(row=10)

e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)

e2.grid(row=2, column=1)
e3.grid(row=4, column=1)
e4.grid(row=6, column=1)
e5.grid(row=8, column =1)
e6.grid(row=10, column =1)

Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=W, pady=4)
Button(master, text='Enter', command=take2).grid(row=17, column=1, sticky=W, pady=4)

master.mainloop( )

#list of calibration target locations, target number, image locations
dirs = []

#have user select calibration target images and corresponding images until they hit cancel
band1 = '1'
currdir = os.getcwd()
while band1 !='':
    root = Tkinter.Tk()
    root.withdraw()
    band1 = str(tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a location for target band 1' ))
    if band1 != '':
        dirs.append(band1)
    currdir = os.path.dirname(band1)

    #get directory for photos that will be edited

root = Tkinter.Tk()
root.withdraw() #use to hide tkinter window
currdir = os.getcwd()
save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select your save directory:' ))


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


#empty lists for average DN of each target band 1-5
avgtarDN1 = []
avgtarDN2 = []
avgtarDN3 = []
avgtarDN4 = []
avgtarDN5 = []

from Tkinter import *
import tkMessageBox

window = Tk()
window.wm_withdraw()
window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
tkMessageBox.showinfo(message="Left click and hold on top left corner of target and drag cursor down to bottom right corner of target, release when complete. Press 'c' to accept box as drawn, press 'r' to redraw box.")


# load the image, clone it, and setup the mouse callback function
# loops through each target image/band in the dirs list, calculates the average DN for that band, and appends it.

h = 0
while h < len(dirs):
    dirh = str(dirs[h])
    #for band 1
    image = imread(dirs[h])
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
    
    #for band 2
    image = imread(dirs[h][:-5]+'2.tif')
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
        roi2 = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]

    #for band 3
    image = imread(dirs[h][:-5]+'3.tif')
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
    
    #for band 4
    image = imread(dirs[h][:-5]+'4.tif')
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
    
    #for band 5
    image = imread(dirs[h][:-5]+'5.tif')
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
        
    DN1 = numpy.mean(roi1)
    avgtarDN1.append(DN1)
    DN2 = numpy.mean(roi2)
    avgtarDN2.append(DN2)
    DN3 = numpy.mean(roi3)
    avgtarDN3.append(DN3)
    DN4 = numpy.mean(roi4)
    avgtarDN4.append(DN4)
    DN5 = numpy.mean(roi5)
    avgtarDN5.append(DN5)
            
    h = h + 1

listmultfact1 = []
listmultfact2 = []
listmultfact3 = []
listmultfact4 = []
listmultfact5 = []

#calculate the DN * ref for each value
x = len(avgtarDN1)
j = 0 
while j < x:
    DNref1 = avgtarDN1[j]*caltarref1[0]
    DNref2 = avgtarDN2[j]*caltarref2[0]
    DNref3 = avgtarDN3[j]*caltarref3[0]
    DNref4 = avgtarDN4[j]*caltarref4[0]
    DNref5 = avgtarDN5[j]*caltarref5[0]
    MaxDNref = max(DNref1,DNref2,DNref3,DNref4,DNref5)
    multfact1 = MaxDNref / DNref1
    listmultfact1.append(multfact1)
    multfact2 =  MaxDNref / DNref2
    listmultfact2.append(multfact2)
    multfact3 =  MaxDNref / DNref3
    listmultfact3.append(multfact3)
    multfact4 =  MaxDNref / DNref4
    listmultfact4.append(multfact4)
    multfact5 =  MaxDNref / DNref5
    listmultfact5.append(multfact5)
    j = j + 1


#average all of the values for each band
avg1 = numpy.mean(listmultfact1)
avg2 = numpy.mean(listmultfact2)
avg3 = numpy.mean(listmultfact3)
avg4 = numpy.mean(listmultfact4)
avg5 = numpy.mean(listmultfact5)

#stdev all of the values
stdev1 = numpy.std(listmultfact1)
stdev2 = numpy.std(listmultfact2)
stdev3 = numpy.std(listmultfact3)
stdev4 = numpy.std(listmultfact4)
stdev5 = numpy.std(listmultfact5)

#export as .txt to save_dir
info = open(save_dir+'/'+'info.txt','a')
info.close()
info2 = open(save_dir+'/'+ 'info.txt','w')
info2.write('Multiplication Values:' + "\n" \
            'band number, avg multiplication value, stdev' + "\n"\
            '1, '+str(avg1)+', '+str(stdev1)+ "\n"+\
            '2, '+str(avg2)+', '+str(stdev2)+ "\n"+\
            '3, '+str(avg3)+', '+str(stdev3)+ "\n"+\
            '4, '+str(avg4)+', '+str(stdev4)+ "\n"+\
            '5, '+str(avg5)+', '+str(stdev5)+ "\n")
                        
info2.close()

    
    
