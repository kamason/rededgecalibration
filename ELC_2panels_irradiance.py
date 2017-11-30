# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:20:37 2017

@author: kmason
"""
from Tkinter import *
import tkMessageBox
import Tkinter
import os
import PIL
import numpy
from osgeo import gdal
import tkFileDialog
from skimage.io import imread
import cv2
from scipy import stats
import exiftool
import matplotlib.pyplot as plt

#ELC Code for Reading MicaSense RedEdge Images and performing an empirical line calibration on them
#This code assumes you have two calibration targets with different reflectances for each instance 
#This code chooses a calibration target based on irradiance values 
# All corrections (such as vignette, exposure, etc.) must have been done to all images previously for this code

# Empty lists for putting the averaged DN values of each of the panels (dark and light) for each of the bands (1-5)
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

#empty list for putting the number of folders that the user inputs
#"folders" are the directory that contains the "SET" folders
numfoldlist = []
#empty list for putting image directories / individual "folders"
imgdirs = []
#empty list for putting the save directories for each of the "folders"
savedirs = []

#function for getting the number of folders from user input
def take2():
    numfold = int(e1.get())
    e1.delete(0,END)
    numfoldlist.append(numfold)
    master.destroy ()
    return

#Tkinter GUI for getting number of folders from user
master = Tk()
master.title("Empirical Line Calibration based on Irradiance Values for MicaSense RedEdge Imagery")
Label(master, text="Number of folders:").grid(row=1)
e1 = Entry(master)
e1.grid(row=1, column=1)
Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=W, pady=4)
Button(master, text='Enter', command=take2).grid(row=17, column=1, sticky=W, pady=4)

master.mainloop ()

#Tkinter GUI for selecting the directory where the exiftool.exe is located
#this .exe file works with the exiftool module which is the only way that I've found to extract the irradiance and vignetting data from the exif of the images
root = Tkinter.Tk()
currdir = os.getcwd() # current working directory
exiftoolloc = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the directory where exiftool.exe is located'))


#extracting number of folders from list
numfolds = numfoldlist[0]

#Tkinter GUI for selecting image directories for each "folder" and save directories
#loops through number of folders
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
    save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir2, title='Please select your save directory for folder ' + str(h) )) # generates GUI for selecting save directory
    savedirs.append(save_dir)
    currdir = img_dir
    currdir2 = save_dir
    
    h = h + 1
    

# generating empty lists for the target image paths and reflectance values to be referenced later
tarref1 = []
tarref2 = []
tarref3 = []
tarref4 = []
tarref5 = []

#function for generating list of image locations

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


#extracting values from list
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

#creating empty list for target directories
tardirs = []

#have user select original calibration target images until they hit cancel
band1 = '1'
currdir = os.getcwd()
while band1 !='':
    root = Tkinter.Tk()
    root.withdraw() #use to hide tkinter window
    band1 = str(tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Please select an original Band 1 calibration target image or choose Cancel if done selecting images.' ))
    currdir = band1
    if band1 != '':
        tardirs.append(band1)
        
# image directories are in imgdirs, save directories are in savedirs, original calibration target locations are in tardirs

# get location of calibrated target images by using calibrated original images directory
newpath = imgdirs[0].split('/')
tardirs2 = []

for x in tardirs:
    y = x.split('/')
    o = newpath[:-1]+y[-3:]
    u = ''
    for i in o:
        u = u + i + '//'
    u = u[:-2]
    tardirs2.append(u)


#Tkinter GUI with message on how to select panels in imagery
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
#loop through targets

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
    
    #appending average DN values of panels to their corresponding lists
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
    
    #looping through all target images
    b = b + 1

# up until now we only have paths of target images for band 1
# now we will determine the paths for bands 2 - 5 
tardirsb2 = []
tardirsb3 = []
tardirsb4 = []
tardirsb5 = []

for u in tardirs:
    b2 = u[:-5] + '2.tif'
    tardirsb2.append(b2)
    b3 = u[:-5] + '3.tif'
    tardirsb3.append(b3)
    b4 = u[:-5] + '4.tif'
    tardirsb4.append(b4)
    b5 = u[:-5] + '5.tif'
    tardirsb5.append(b5)
 
# read the irradiance values from the exif of the target images bands 1 - 5
os.chdir('F:\Workspace')
with exiftool.ExifTool() as et:
    DLS1 = et.get_tag_batch('XMP:SpectralIrradiance',tardirs[:])
    DLS2 = et.get_tag_batch('XMP:SpectralIrradiance',tardirsb2[:])
    DLS3 = et.get_tag_batch('XMP:SpectralIrradiance',tardirsb3[:])
    DLS4 = et.get_tag_batch('XMP:SpectralIrradiance',tardirsb4[:])
    DLS5 = et.get_tag_batch('XMP:SpectralIrradiance',tardirsb5[:])

#calculate the slope of the DN vs. irradiance for dark and light targets

DLS1 = [float(i) for i in DLS1]
DLS2 = [float(i) for i in DLS2]
DLS3 = [float(i) for i in DLS3]
DLS4 = [float(i) for i in DLS4]
DLS5 = [float(i) for i in DLS5]

#dark
m1d, c1d, r1d, p1d, std1d = stats.linregress(DN1_dark,DLS1)
m2d, c2d, r2d, p2d, std2d = stats.linregress(DN2_dark,DLS2)
m3d, c3d, r3d, p3d, std3d = stats.linregress(DN3_dark,DLS3)
m4d, c4d, r4d, p4d, std4d = stats.linregress(DN4_dark,DLS4)
m5d, c5d, r5d, p5d, std5d = stats.linregress(DN5_dark,DLS5)

#light
m1l, c1l, r1l, p1l, std1l = stats.linregress(DN1_light,DLS1)
m2l, c2l, r2l, p2l, std2l = stats.linregress(DN2_light,DLS2)
m3l, c3l, r3l, p3l, std3l = stats.linregress(DN3_light,DLS3)
m4l, c4l, r4l, p4l, std4l = stats.linregress(DN4_light,DLS4)
m5l, c5l, r5l, p5l, std5l = stats.linregress(DN5_light,DLS5)

#display all scatter plots from dark of relationship between irradiance and DN
plt.figure(1)
plt.subplot(3,2,1)
plt.title('Band 1 - Dark')
plt.scatter(DN1_dark,DLS1)
plt.plot(DN1_dark,DLS1)
plt.xlabel('DN')
plt.ylabel('Irrad')

plt.subplot(3,2,2)
plt.title('Band 2 - Dark')
plt.scatter(DN2_dark,DLS2)
plt.plot(DN2_dark,DLS2)
plt.xlabel('DN')
plt.ylabel('Irrad')

plt.subplot(3,2,3)
plt.title('Band 3 - Dark')
plt.scatter(DN3_dark,DLS3)
plt.plot(DN3_dark,DLS3)
plt.xlabel('DN')
plt.ylabel('Irrad')

plt.subplot(3,2,4)
plt.title('Band 4 - Dark')
plt.scatter(DN4_dark,DLS4)
plt.plot(DN4_dark,DLS4)
plt.xlabel('DN')
plt.ylabel('Irrad')

plt.subplot(3,2,5)
plt.title('Band 5 - Dark')
plt.scatter(DN5_dark,DLS5)
plt.plot(DN5_dark,DLS5)
plt.xlabel('DN')
plt.ylabel('Irrad')

plt.tight_layout()

plt.show()

#display all scatter plots from light between irradiance and DN
plt.figure(2)
plt.subplot(3,2,1)
plt.title('Band 1 - Light')
plt.scatter(DN1_light,DLS1)
plt.plot(DN1_light,DLS1)
plt.xlabel('DN')
plt.ylabel('Irrad')

plt.subplot(3,2,2)
plt.title('Band 2 - Light')
plt.scatter(DN2_light,DLS2)
plt.plot(DN2_light,DLS2)
plt.xlabel('DN')
plt.ylabel('Irrad')

plt.subplot(3,2,3)
plt.title('Band 3 - Light')
plt.scatter(DN3_light,DLS3)
plt.plot(DN3_light,DLS3)
plt.xlabel('DN')
plt.ylabel('Irrad')

plt.subplot(3,2,4)
plt.title('Band 4 - Light')
plt.scatter(DN4_light,DLS4)
plt.plot(DN4_light,DLS4)
plt.xlabel('DN')
plt.ylabel('Irrad')

plt.subplot(3,2,5)
plt.title('Band 5 - Light')
plt.scatter(DN5_light,DLS5)
plt.plot(DN5_light,DLS5)
plt.xlabel('DN')
plt.ylabel('Irrad')

plt.tight_layout()

plt.show()


d = 0

#loop through each folder
while d < numfolds:
    
    imgpaths = filenames(imgdirs[d])
    
    #finding the original image paths for extracting time info
    #this assumes that the images being calibrated are not the original images, they are the vignette corrected images so in order to get original time images were taken the original image paths must be known, this is retrieved from the target directories
    origpaths = []
    for x in imgpaths:
        y = x.split('\\')
        z = tardirs[0].split('/')
        t = y[-4].split('/')
        o = z[:-4]+t[-1:]+y[-3:]
        u = ''
        for i in o:
            u = u + i + '//'
        u = u[:-2]
        origpaths.append(u)

    numimgs = len(imgpaths)
    
    #change directory to location where exiftool.exe is located
    os.chdir(exiftoolloc)
    with exiftool.ExifTool() as et:
        DLS = et.get_tag_batch('XMP:SpectralIrradiance',origpaths[:])
        
    a = 0
    while a < numimgs:
        filename = imgpaths[a]
        name = filename[-14:]
        t = gdal.Open(filename)
        numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
        DLSnum = float(DLS[a])
        
        #determine which band and calculate equation for converting DN to ref based on irradiance, and then convert DN to ref
        if name[-6:]=='_1.tif':
            DNlight = (DLSnum - c1l)/(m1l)
            DNdark = (DLSnum - c1d)/(m1d)
            m = (ref1light-ref1dark)/(DNlight-DNdark)
            c = (ref1light - m)*DNlight
            ref = (numpyimg*m)+c
        elif name[-6:]=='_2.tif':
            DNlight = (DLSnum - c2l)/(m2l)
            DNdark = (DLSnum - c2d)/(m2d)
            m = (ref2light-ref2dark)/(DNlight-DNdark)
            c = (ref2light - m)*DNlight
            ref = (numpyimg*m)+c
        elif name[-6:]=='_3.tif':
            DNlight = (DLSnum - c3l)/(m3l)
            DNdark = (DLSnum - c3d)/(m3d)
            m = (ref3light-ref3dark)/(DNlight-DNdark)
            c = (ref3light - m)*DNlight
            ref = (numpyimg*m)+c
        elif name[-6:]=='_4.tif':
            DNlight = (DLSnum - c4l)/(m4l)
            DNdark = (DLSnum - c4d)/(m4d)
            m = (ref4light-ref4dark)/(DNlight-DNdark)
            c = (ref4light - m)*DNlight
            ref = (numpyimg*m)+c
        elif name[-6:]=='_5.tif':
            DNlight = (DLSnum - c5l)/(m5l)
            DNdark = (DLSnum - c5d)/(m5d)
            m = (ref5light-ref5dark)/(DNlight-DNdark)
            c = (ref5light - m)*DNlight
            ref = (numpyimg*m)+c
        #generating save directory to be in the same file format as image paths
        subdir = filename.split(imgdirs[d])        
        savedir = savedirs[d] + subdir[1][:-15]
        subdir1 = subdir[1].split('SET')
        setdir = savedirs[d] + subdir1[0]+'SET'
        if not os.path.exists(setdir):
            os.mkdir(setdir)
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        os.chdir(savedir)
        #save numpy array as .tiff
        #this new image will not have the exif info from the original images
        img = PIL.Image.fromarray(ref, mode=None)
        img.save(name)
        a = a + 1
        #looping through images
    d = d + 1
    #looping through folders