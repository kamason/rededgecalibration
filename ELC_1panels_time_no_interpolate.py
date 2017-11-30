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

#Reading MicaSense RedEdge Images and performing an empirical line calibration on them
#This code assumes you have one calibration target 
#This code chooses a calibration target based on time values
#This code is for converting radiance images to reflectance images 

#Empty lists for panel averages
DN1_light= []
DN2_light = []
DN3_light = []
DN4_light = []
DN5_light = []

#Empty list for panel standard devations
stdev1 = []
stdev2 = []
stdev3 = []
stdev4 = []
stdev5 = []

#List for holding number of folders taken from Tkinter GUI
numfoldlist = []
#List for holding image folders, there will be as many directories as there are folders
imgdirs = []
#List for holding save directories. There will be as many save directories as there are image directories above.
savedirs = []

def take2():
    numfold = int(e1.get())
    e1.delete(0,END)
    numfoldlist.append(numfold)
    master.destroy ()
    return

#GUI for asking user how many folders they will be inputting
master = Tk()
master.title("Empirical Line Calibration based on Irradiance Values for MicaSense RedEdge Imagery")
Label(master, text="Number of folders:").grid(row=1)
e1 = Entry(master)
e1.grid(row=1, column=1)
Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=W, pady=4)
Button(master, text='Enter', command=take2).grid(row=17, column=1, sticky=W, pady=4)

master.mainloop ()

#extracting the number of folders from the list, this is just a quirk of Tkinter
numfolds = numfoldlist[0]

#For every folder the user will input an image directory for location of radiance images and a save directory
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


#get user input for reference values of panel
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

master = Tk()
master.title("Empirical Line Calibration for MicaSense RedEdge Imagery")
Label(master, text="Reflectance Value Band 1 for target:").grid(row=2)
Label(master, text='Reflectance Value Band 2 for target:').grid(row=4)
Label(master, text="Reflectance Value Band 3 for target:").grid(row=6)
Label(master, text="Reflectance Value Band 4 for target:").grid(row=8)
Label(master, text="Reflectance Value Band 5 for target:").grid(row=10)

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

tardirs = []

#have user select original calibration target images until they hit cancel, these images are  not the radiance images, but the original raw images.
band1 = '1'
currdir = imgdirs[0]
while band1 !='':
    root = Tkinter.Tk()
    root.withdraw() #use to hide tkinter window
    band1 = str(tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Please select an original Band 1 image of calibration target or choose Cancel if done selecting images.' ))
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
    
    
    #band 2 light
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    
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
            
    
    #band 3 light
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    
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
    
    #band 4 light
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    
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
            
    
    #band 5 light
    window = Tk()
    window.wm_withdraw()
    window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
    
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
            
            
    DN1_light.append(roi1light.mean())    
    DN2_light.append(roi2light.mean())
    DN3_light.append(roi3light.mean())
    DN4_light.append(roi4light.mean())
    DN5_light.append(roi5light.mean())
    stdev1.append(roi1light.std())
    stdev2.append(roi2light.std())
    stdev3.append(roi3light.std())
    stdev4.append(roi4light.std())
    stdev5.append(roi5light.std())
    
    b = b + 1

time1 = []
#this will be a list of times for panel images
s = 0

# This will be the noise % calculation for the panels that will go in a txt file 
noise1 = []
noise2 = []
noise3 = []
noise4 = []
noise5 = []

y = 0
# calculating noise %
while y < len(DN1_light):
    noise1.append(stdev1[y]/DN1_light[y])
    noise2.append(stdev2[y]/DN2_light[y])
    noise3.append(stdev3[y]/DN3_light[y])
    noise4.append(stdev4[y]/DN4_light[y])
    noise5.append(stdev5[y]/DN5_light[y])
    y = y + 1

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
            
    time = (hour + (minute/float(60))+ (second/float(60)/float(60)))
    
    time1.append(time)
    s = s+1
    
#save panel averages and standard deviations as a txt file
text = 'Band 1 Averages:' + str(DN1_light) +'\n' \
'Band 1 Standard Deviations:' + str(stdev1)+'\n'\
'Band 1 Noise %:' + str(noise1)+'\n'\
'Band 2 Averages:' + str(DN2_light)+'\n' \
'Band 2 Standard Deviations:' + str(stdev2)+'\n'\
'Band 2 Noise %:' + str(noise2)+'\n'\
'Band 3 Averages:' + str(DN3_light) +'\n'\
'Band 3 Standard Deviations:' + str(stdev3)+'\n'\
'Band 3 Noise %:' + str(noise3)+'\n'\
'Band 4 Averages:' + str(DN4_light) +'\n'\
'Band 4 Standard Deviations:' + str(stdev4)+'\n'\
'Band 4 Noise %:' + str(noise4)+'\n'\
'Band 5 Averages:' + str(DN5_light) +'\n'\
'Band 5 Standard Deviations:' + str(stdev5)+'\n'\
'Band 5 Noise %:' + str(noise5)+'\n'\

new_file = open(savedirs[0] + '/info.txt', 'w')
new_file.write(text)
new_file.close()

d = 0
#open each 
while d < numfolds:
    
    # opens each image as numpyarray
    imgpaths = filenames(imgdirs[d])
    #determining the original image paths based on the original target image paths to get original exif info
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
        #path to image being corrected (radiance)
        filename = imgpaths[a]
        #path to original raw version of that image with exif info
        origfilename = origpaths[a]
        #name of image
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
        
        #open image and convert to numpy array
        t = gdal.Open(filename)
        numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
        
        difftime = []
        
        #determine the differences between image time and panel times to find the panel that was taken at the closest time
        for x in time1:
            difftime.append(abs(time - x))
        
        #determining the index value for the minimum time difference to determine which panel to use for calibration
        locclose = difftime.index(min(difftime))
        
        #determine which band and calculate equation for converting DN to ref based on time, and then convert DN to ref
        if name[-6:]=='_1.tif':
            #finding the average panel values for the panel with the closest time to the image
            DNlight = DN1_light[locclose]
            #calculating factor for converting to reflectance
            m = (ref1light/DNlight)
            #convert to reflectance
            ref = (numpyimg)*m
        elif name[-6:]=='_2.tif':
            DNlight = DN2_light[locclose]
            m = (ref2light/DNlight)
            ref = (numpyimg)*m
        elif name[-6:]=='_3.tif':
            DNlight = DN3_light[locclose]
            m = (ref3light/DNlight)
            ref = (numpyimg)*m
        elif name[-6:]=='_4.tif':
            DNlight = DN4_light[locclose]
            m = (ref4light/DNlight)
            ref = (numpyimg)*m
        elif name[-6:]=='_5.tif':
            DNlight = DN5_light[locclose]
            m = (ref5light/DNlight)
            ref = (numpyimg)*m
        
        #Saving the images in the same file format as they were originally
        #checking if folder is already there and if not, the folder is generated
        #The file structure is essentially \\PATHOFSAVEDIRECTORY\\000SET\\000
        #You have to determine what number the set folder is (i.e. 000SET or 001SET or 002SET) as well as which final folder number (000, 001, 002 etc.)
        subdir = filename.split(imgdirs[d])        
        savedir = savedirs[d] + subdir[1][:-15]
        subdir1 = subdir[1].split('SET')
        setdir = savedirs[d] + subdir1[0]+'SET'
        if not os.path.exists(setdir):
            os.mkdir(setdir)
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        os.chdir(savedir)
        #save image as a floating tif
        img = PIL.Image.fromarray(ref, mode=None)
        img.save(name)
        a = a + 1
    d = d + 1