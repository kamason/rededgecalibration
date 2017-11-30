# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:20:37 2017

@author: kmason
"""
from Tkinter import *
import Tkinter
import os
import PIL
import numpy
from osgeo import gdal
import tkFileDialog
from skimage.io import imread
import cv2
from scipy import stats
import exifread
import time
import datetime
from heapq import nsmallest

#ELC Code for Reading MicaSense RedEdge Images and performing an empirical line calibration on them
#This code assumes you have two calibration targets with different reflectances for each instance 
#This code chooses a calibration target based on time values
# All corrections (such as vignette, exposure, etc.) must have been done to all images before putting them in this code

DN1_light= []
DN2_light = []
DN3_light = []
DN4_light = []
DN5_light = []
DN1_dark = []
DN2_dark = []
DN3_dark = []
DN4_dark = []
DN5_dark = []

numfoldlist = []
imgdirs = []
savedirs = []

def take2():
    numfold = int(e1.get())
    e1.delete(0,END)
    numfoldlist.append(numfold)
    master.destroy ()
    return

master = Tk()
master.title("Empirical Line Calibration based on Irradiance Values for MicaSense RedEdge Imagery")
Label(master, text="Number of folders:").grid(row=1)
e1 = Entry(master)
e1.grid(row=1, column=1)
Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=W, pady=4)
Button(master, text='Enter', command=take2).grid(row=17, column=1, sticky=W, pady=4)

master.mainloop ()

numfolds = numfoldlist[0]

h = 1
currdir = os.getcwd()
currdir2 = os.getcwd()
while h <= numfolds:
    root = Tkinter.Tk()
    root.withdraw()
    img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select your image directory for folder ' + str(h) )) # generates GUI for selecting directory with images
    imgdirs.append(img_dir)
    root = Tkinter.Tk()
    root.withdraw()
    save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=img_dir, title='Please select your save directory for folder ' + str(h) )) # generates GUI for selecting save directory
    savedirs.append(save_dir)
    currdir = img_dir
    
    h = h + 1
    

# generating empty lists for the target image paths and reflectance values to be referenced later
tarref1 = []
tarref2 = []
tarref3 = []
tarref4 = []
tarref5 = []

#function for generating list of images
def filenames(folder):
    os.chdir(folder)
    y = []
    #SET directories (such as 001SET )
    p = []
    #other dirs such as (000, 001, etc.)
    z = []
    #image names
    e = []
    #image directory names
    for path, subdirs, files in os.walk(os.getcwd()):
        #appends list of .tif files to image names list
        for t in files:
                if t.endswith('.tif'):
                    z.append(t)
        #appends both SET and other subdirectories to list 
        for x in subdirs:
            if x.endswith('SET'):
                y.append(x)
            else:
                p.append(x)

    p = list(set(p))
    #removes the duplicates in the list
    z = list(set(z))
    #removes the duplicates in the list
    for setdir in y:
        for otherdir in p:
            for img in z:
                u = os.path.join(folder,setdir,otherdir,img)
                #make file path out of all combinations of SET folders, other folders and images
                if os.path.exists(u) == True:
                #if that image / location actually exists append it to the list
                    e.append(u)
    return e


#get user input
def take():
    # assigning variables to the user inputs
    ref1 = float(e2.get())
    tarref1.append(ref1)
    ref2 = float(e3.get())
    tarref2.append(ref2)
    ref3 = float(e4.get())
    tarref3.append(ref3)
    ref4  = float(e5.get())
    tarref4.append(ref4)
    ref5  = float(e6.get())
    tarref5.append(ref5)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)
    e6.delete(0,END)
    master.quit()
    master.destroy()
    return

h = 1

#user enters values for calibration targets by number
while h <= 2:
    h = h + 1
    if h == 2:
        n = 'light'
    elif h==3:
        n = 'dark'
    
    master = Tk()
    master.title("Empirical Line Calibration for MicaSense RedEdge Imagery")
    Label(master, text="Reflectance Value Band 1 for " + n + " target:").grid(row=2)
    Label(master, text='Reflectance Value Band 2 for ' + n + ' target:').grid(row=4)
    Label(master, text="Reflectance Value Band 3 for " + n + " target:").grid(row=6)
    Label(master, text="Reflectance Value Band 4 for "+ n + " target:").grid(row=8)
    Label(master, text="Reflectance Value Band 5 for "+ n +" target:").grid(row=10)

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
    Button(master, text='Enter', command=take).grid(row=17, column=1, sticky=W, pady=4)

    master.mainloop( )



ref1light = tarref1[0]
ref2light = tarref2[0]
ref3light = tarref3[0]
ref4light = tarref4[0]
ref5light = tarref5[0]
ref1dark = tarref1[1]
ref2dark = tarref2[1]
ref3dark = tarref3[1]
ref4dark = tarref4[1]
ref5dark = tarref5[1]

tardirs = []

#have user select original calibration target images until they hit cancel
band1 = '1'
currdir = os.getcwd()
while band1 !='':
    root = Tkinter.Tk()
    root.withdraw() #use to hide tkinter window
    band1 = str(tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Please select an original Band 1 image of both calibration targets or choose Cancel if done selecting images.' ))
    currdir = band1
    if band1 != '':
        tardirs.append(band1)
        
# image directories are in imgdirs, save directories are in savedirs, original calibration target locations are in tardirs

# get location of calibrated target images by using calibrated original images directory
newpath = imgdirs[0].split('/')
tardirs2 = []

for x in tardirs:
    y = x.split('/')
    o = newpath[:]+y[-3:]
    u = ''
    for i in o:
        u = u + i + '//'
    u = u[:-2]
    tardirs2.append(u)

from Tkinter import *
import tkMessageBox

window = Tk()
window.wm_withdraw()
window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
tkMessageBox.showinfo(message="Left click and hold on top left corner of target and drag cursor down to bottom right corner of target, release when complete. Press 'c' to accept box as drawn, press 'r' to redraw box.")

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
#select targets and average DN

b = 0
while b < len(tardirs):
    #band 1 light
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    tkMessageBox.showinfo(message="Band 1 target " + str(b+1) + " light target")
    
    image = imread(tardirs[b])
    clone = image.copy()
    clone2 = imread(tardirs2[b])
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
        roi1light = clone2[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
    #band 1 dark
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    tkMessageBox.showinfo(message="Band 1 target " + str(b+1) + " dark target")
    
    image = imread(tardirs[b])
    clone = image.copy()
    clone2 = imread(tardirs2[b])
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
        roi1dark = clone2[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
    #band 2 light
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    tkMessageBox.showinfo(message="Band 2 target " + str(b+1) + " light target")
    
    image = imread(tardirs[b][:-5]+'2.tif')
    clone = image.copy()
    clone2 = imread(tardirs2[b][:-5]+'2.tif')
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
        roi2light = clone2[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            
    #band 2 dark
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    tkMessageBox.showinfo(message="Band 2 target " + str(b+1) + " dark target")
    
    image = imread(tardirs[b][:-5]+'2.tif')
    clone = image.copy()
    clone2 = imread(tardirs2[b][:-5]+'2.tif')
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
        roi2dark = clone2[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
    #band 3 light
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    tkMessageBox.showinfo(message="Band 3 target " + str(b+1) + " light target")
    
    image = imread(tardirs[b][:-5]+'3.tif')
    clone = image.copy()
    clone2 = imread(tardirs2[b][:-5]+'3.tif')
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
        roi3light = clone2[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            
    #band 3 dark
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    tkMessageBox.showinfo(message="Band 3 target " + str(b+1) + " dark target")
    
    image = imread(tardirs[b][:-5]+'3.tif')
    clone = image.copy()
    clone2 = imread(tardirs2[b][:-5]+'3.tif')
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
        roi3dark = clone2[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
    #band 4 light
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    tkMessageBox.showinfo(message="Band 4 target " + str(b+1) + " light target")
    
    image = imread(tardirs[b][:-5]+'4.tif')
    clone = image.copy()
    clone2 = imread(tardirs2[b][:-5]+'4.tif')
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
        roi4light = clone2[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            
    #band 4 dark
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    tkMessageBox.showinfo(message="Band 4 target " + str(b+1) + " dark target")
    
    image = imread(tardirs[b][:-5]+'4.tif')
    clone = image.copy()
    clone2 = imread(tardirs2[b][:-5]+'4.tif')
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
        roi4dark = clone2[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
    #band 5 light
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    tkMessageBox.showinfo(message="Band 5 target " + str(b+1) + " light target")
    
    image = imread(tardirs[b][:-5]+'5.tif')
    clone = image.copy()
    clone2 = imread(tardirs2[b][:-5]+'5.tif')
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
        roi5light = clone2[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            
    #band 5 dark
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    tkMessageBox.showinfo(message="Band 5 target " + str(b+1) + " dark target")
    
    image = imread(tardirs[b][:-5]+'5.tif')
    clone = image.copy()
    clone2 = imread(tardirs2[b][:-5]+'5.tif')
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
        roi5dark = clone2[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            
    DN1_light.append(roi1light.mean())    
    DN2_light.append(roi2light.mean())
    DN3_light.append(roi3light.mean())
    DN4_light.append(roi4light.mean())
    DN5_light.append(roi5light.mean())
    DN1_dark.append(roi1dark.mean())
    DN2_dark.append(roi2dark.mean())
    DN3_dark.append(roi3dark.mean())
    DN4_dark.append(roi4dark.mean())
    DN5_dark.append(roi5dark.mean())
    
    b = b + 1

time1 = []
s = 0

while s < len(tardirs):
    # read the time values from the exif of the target images
    #band 1
    f = open(tardirs[s],'rb')
    tags = exifread.process_file(f, details=False)
    photodatetime = tags['EXIF DateTimeDigitized']
    photodatetime = str(photodatetime)
    photodatetime = photodatetime.split(':')
    day = photodatetime[2].split(' ')
    # hour must be in UTC time
    hour = int(day[1])
    
    minute = int(photodatetime[3])
    second = int(photodatetime[4])
            
    time = hour + (minute/float(60))+ (second/float(60)/float(60))
    
    time1.append(time)
    s = s+1
    



d = 0
#open each 
while d < numfolds:
    
    # opens each image as numpyarray
    imgpaths = filenames(imgdirs[d])
    origpaths = []
    for x in imgpaths:
        y = x.split('\\')
        z = tardirs[0].split('/')
        o = z[:-3]+y[-3:]
        u = ''
        for i in o:
            u = u + i + '//'
        u = u[:-2]
        origpaths.append(u)
    

    numimgs = len(imgpaths)
        
    a = 0
    while a < numimgs:
        filename = imgpaths[a]
        origfilename = origpaths[a]
        name = filename[-14:]
        
        #read time from exif info
        f = open(origfilename,'rb')
        tags = exifread.process_file(f, details=False)
        photodatetime = tags['EXIF DateTimeDigitized']
        photodatetime = str(photodatetime)
        photodatetime = photodatetime.split(':')
        day = photodatetime[2].split(' ')
        # hour must be in UTC time
        hour = int(day[1])
    
        minute = int(photodatetime[3])
        second = int(photodatetime[4])
            
        time = hour + (minute/float(60))+ (second/float(60)/float(60))
        
        t = gdal.Open(filename)
        numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())

        #determine which two panels to use for equation based on time
        timeclose = nsmallest(2,time1,key=lambda x:abs(x-time))
        mintime = min(timeclose)
        maxtime = max(timeclose)
        
        locmax = time1.index(maxtime)
        locmin = time1.index(mintime)
        
        
        #determine which band and calculate equation for converting DN to ref based on time, and then convert DN to ref
        if name[-6:]=='_1.tif':
            DNlight_m = (DN1_light[locmax]-DN1_light[locmin])/(maxtime-mintime)
            DNdark_m = (DN1_dark[locmax]-DN1_dark[locmin])/(maxtime-mintime)
            DNlight_c = DN1_light[locmax]-(DNlight_m*maxtime)
            DNdark_c = DN1_dark[locmax]-(DNdark_m*maxtime)
            DNlight = (DNlight_m*time)+DNlight_c
            DNdark = (DNdark_m*time)+DNdark_c
            m = (ref1light-ref1dark)/(DNlight-DNdark)
            c = ref1light-(m*DNlight)
            ref = (numpyimg*m)+c
        elif name[-6:]=='_2.tif':
            DNlight_m = (DN2_light[locmax]-DN2_light[locmin])/(maxtime-mintime)
            DNdark_m = (DN2_dark[locmax]-DN2_dark[locmin])/(maxtime-mintime)
            DNlight_c = DN2_light[locmax]-(DNlight_m*maxtime)
            DNdark_c = DN2_dark[locmax]-(DNdark_m*maxtime)
            DNlight = (DNlight_m*time)+DNlight_c
            DNdark = (DNdark_m*time)+DNdark_c
            m = (ref2light-ref1dark)/(DNlight-DNdark)
            c = ref2light-(m*DNlight)
            ref = (numpyimg*m)+c
        elif name[-6:]=='_3.tif':
            DNlight_m = (DN3_light[locmax]-DN3_light[locmin])/(maxtime-mintime)
            DNdark_m = (DN3_dark[locmax]-DN3_dark[locmin])/(maxtime-mintime)
            DNlight_c = DN3_light[locmax]-(DNlight_m*maxtime)
            DNdark_c = DN3_dark[locmax]-(DNdark_m*maxtime)
            DNlight = (DNlight_m*time)+DNlight_c
            DNdark = (DNdark_m*time)+DNdark_c
            m = (ref3light-ref1dark)/(DNlight-DNdark)
            c = ref3light-(m*DNlight)
            ref = (numpyimg*m)+c
        elif name[-6:]=='_4.tif':
            DNlight_m = (DN4_light[locmax]-DN4_light[locmin])/(maxtime-mintime)
            DNdark_m = (DN4_dark[locmax]-DN4_dark[locmin])/(maxtime-mintime)
            DNlight_c = DN4_light[locmax]-(DNlight_m*maxtime)
            DNdark_c = DN4_dark[locmax]-(DNdark_m*maxtime)
            DNlight = (DNlight_m*time)+DNlight_c
            DNdark = (DNdark_m*time)+DNdark_c
            m = (ref4light-ref1dark)/(DNlight-DNdark)
            c = ref4light-(m*DNlight)
            ref = (numpyimg*m)+c
        elif name[-6:]=='_5.tif':
            DNlight_m = (DN5_light[locmax]-DN5_light[locmin])/(maxtime-mintime)
            DNdark_m = (DN5_dark[locmax]-DN5_dark[locmin])/(maxtime-mintime)
            DNlight_c = DN5_light[locmax]-(DNlight_m*maxtime)
            DNdark_c = DN5_dark[locmax]-(DNdark_m*maxtime)
            DNlight = (DNlight_m*time)+DNlight_c
            DNdark = (DNdark_m*time)+DNdark_c
            m = (ref5light-ref1dark)/(DNlight-DNdark)
            c = ref5light-(m*DNlight)
            ref = (numpyimg*m)+c
            
        subdir = filename.split(imgdirs[d])        
        savedir = savedirs[d] + subdir[1][:-15]
        subdir1 = subdir[1].split('SET')
        setdir = savedirs[d] + subdir1[0]+'SET'
        if not os.path.exists(setdir):
            os.mkdir(setdir)
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        os.chdir(savedir)
        img = PIL.Image.fromarray(ref, mode=None)
        img.save(name)
        a = a + 1
            # exports images as tiffs
    d = d + 1