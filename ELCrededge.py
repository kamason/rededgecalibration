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
numtarslist = []

#function for generating list of images
def filenames(folder):
    os.chdir(folder)
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
            p.append(x)
    
    z = list(set(z))
    g = 0
    l = 0
    while g < len(p):
        while l < len(z):
            u = os.path.join(folder, p[g],z[l])
            #make file path out of all combinations of SET folders, other folders and images
            if os.path.exists(u) == True:
                #if that image / location actually exists append it to the list
                e.append(u)
            l = l + 1
        l = 0
        g = g + 1
    return e
        
    #removes the duplicates in the list
    z = list(set(z))
    #removes the duplicates in the list
    for setdir in y:
        leneb4 = len(e)
        for otherdir in p:
            for img in z:
                u = os.path.join(folder,setdir,otherdir,img)
                #make file path out of all combinations of SET folders, other folders and images
                if os.path.exists(u) == True:
                #if that image / location actually exists append it to the list
                    e.append(u)
    return e

import exiftool

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
Label(master, text="Number of calibration targets:").grid(row=1)
e1 = Entry(master)
e1.grid(row=1, column=1)
Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=W, pady=4)
Button(master, text='Enter', command=take).grid(row=17, column=1, sticky=W, pady=4)

master.mainloop ()

numtars = numtarslist[0]

h = 1

#user enters values for calibration targets by number
while h <= numtars:
    h = h + 1
    n = h -1
    master = Tk()
    master.title("Empirical Line Calibration for MicaSense RedEdge Imagery")
    Label(master, text="Reflectance Value Band 1 for Target " + str(n)+ ":").grid(row=2)
    Label(master, text='Reflectance Value Band 2 for Target ' + str(n)+ ":").grid(row=4)
    Label(master, text="Reflectance Value Band 3 for Target " + str(n)+ ":").grid(row=6)
    Label(master, text="Reflectance Value Band 4 for Target " + str(n)+ ":").grid(row=8)
    Label(master, text="Reflectance Value Band 5 for Target " + str(n)+ ":").grid(row=10)

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
img_dir = '1'
x = 0
dirs.append('x0')
currdir = os.getcwd()
while img_dir !='':
    root = Tkinter.Tk()
    root.withdraw()
    img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the "SET" folder of images that correspond to calibration target image(s) or choose Cancel if done selecting images.' )) # generates GUI for selecting directory with images
    if img_dir != '':
        dirs.append(img_dir)
        h = 1
        while h<=numtars:
            if h == numtars:
                root = Tkinter.Tk()
                root.withdraw() #use to hide tkinter window
                band1 = str(tkFileDialog.askopenfilename(parent=root, initialdir=img_dir, title='Please select a location for target ' + str(h) + " Band 1 or choose Cancel if done selecting targets." ))
                if band1 != '':
                    dirs.append(band1)
                    dirs.append(h)
                h = h + 1
            else:
                root = Tkinter.Tk()
                root.withdraw() #use to hide tkinter window
                band1 = str(tkFileDialog.askopenfilename(parent=root, initialdir=img_dir, title='Please select a location for target ' + str(h) + " Band 1 or choose Cancel for different target number." ))
                if band1 != '':
                    dirs.append(band1)
                    dirs.append(h)
                h = h + 1
        dirs.append('x')
        x = x + 1
        dirs.append('x'+str(x))
        currdir = img_dir
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
    if len(dirh)>4:
        if dirh[-4:]== '.tif':
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
        
            # load the image, clone it, and setup the mouse callback function
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
        
            # for band 3
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
        else:
            h = h + 1
    else:
        h = h + 1

x = dirs.count('x')
a = 0 
h = 0
while a < x:
    index = dirs.index('x'+str(a)) 
    set_dir = dirs[index + 1]
    imgpaths = filenames(set_dir)
    if numtars == 1:
        ref1 = caltarref1[0]
        ref2 = caltarref2[0]
        ref3 = caltarref3[0]
        ref4 = caltarref4[0]
        ref5 = caltarref5[0]
        DNtar1 = avgtarDN1[a]
        DNtar2 = avgtarDN2[a]
        DNtar3 = avgtarDN3[a] 
        DNtar4 = avgtarDN4[a] 
        DNtar5 = avgtarDN5[a] 
        #loop through all images in folder
        r = 0
        while r < len(imgpaths):
            filename = imgpaths[r]
            name = filename[-14:]
            t = gdal.Open(filename)
            numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
        
            if name[-6:]=='_1.tif':
                ref = (numpyimg*ref1)/DNtar1
            elif name[-6:]=='_2.tif':
                ref = (numpyimg*ref2)/DNtar2
            elif name[-6:]=='_3.tif':
                ref = (numpyimg*ref3)/DNtar3
            elif name[-6:]=='_4.tif':
                ref = (numpyimg*ref4)/DNtar4
            elif name[-6:]=='_5.tif':
                ref = (numpyimg*ref5)/DNtar5
        
            fold = set_dir.split('/')
            setdir = fold[-1]
            fold = fold[-2]
            folderdir = save_dir + '/' + fold
            setdir = folderdir + '/' + setdir
            savedir = filename.split(name)
            savedir = savedir[0].split(set_dir)
            savedir = savedir[1]
            savedir = setdir + savedir
            if not os.path.exists(folderdir):
                os.mkdir(folderdir)
            if not os.path.exists(setdir):
                os.mkdir(setdir)
            if not os.path.exists(savedir):
                os.mkdir(savedir)
            os.chdir(savedir)
            #save new images with reflectance values in new folder
            img = PIL.Image.fromarray(ref, mode=None)
            img.save(name)
            r = r + 1
        a = a + 1
           
    elif numtars == 2:
        index2 = dirs.index('x'+str(a+1)) 
        #if two calibration targets were chosen
        if index2 - index == 7:
            #reflectance values for target 1 for each band
            ref1_1 = caltarref1[0]
            ref2_1 = caltarref2[0]
            ref3_1 = caltarref3[0]
            ref4_1 = caltarref4[0]
            ref5_1 = caltarref5[0]
            #reflectance values for target 2 for each band
            ref1_2 = caltarref1[1]
            ref2_2 = caltarref2[1]
            ref3_2 = caltarref3[1]
            ref4_2 = caltarref4[1]
            ref5_2 = caltarref5[1]
            #avg DN values for target 1 for each band
            DN1_1 = avgtarDN1[h]
            DN2_1 = avgtarDN2[h]
            DN3_1 = avgtarDN3[h]
            DN4_1 = avgtarDN4[h]
            DN5_1 = avgtarDN5[h]
            #avg DN values for target 2 for each band
            DN1_2 = avgtarDN1[h+1]
            DN2_2 = avgtarDN2[h+1]
            DN3_2 = avgtarDN3[h+1]
            DN4_2 = avgtarDN4[h+1]
            DN5_2 = avgtarDN5[h+1]
            #slope for conversion equation for each band
            m1 = (ref1_1-ref1_2)/(DN1_1 - DN1_2)
            m2 = (ref2_1-ref2_2)/(DN2_1 - DN2_2)
            m3 = (ref3_1-ref3_2)/(DN3_1 - DN3_2)
            m4 = (ref4_1-ref4_2)/(DN4_1 - DN4_2)
            m5 = (ref5_1-ref5_2)/(DN5_1 - DN5_2)
            #y-intercept for conversion equation for each band
            c1 = ref1_1 -m1 * DN1_1
            c2 = ref2_1 -m2 * DN2_1
            c3 = ref3_1 -m3 * DN3_1
            c4 = ref4_1 -m4 * DN4_1
            c5 = ref5_1 -m5 * DN5_1
                    
            r = 0
            while r < len(imgpaths):
                filename = imgpaths[r]
                name = filename[-14:]
                t = gdal.Open(filename)
                numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
                
                if name[-6:]=='_1.tif':
                    ref = (numpyimg*m1)+c1
                elif name[-6:]=='_2.tif':
                    ref = (numpyimg*m2)+c2
                elif name[-6:]=='_3.tif':
                    ref = (numpyimg*m3)+c3
                elif name[-6:]=='_4.tif':
                    ref = (numpyimg*m4)+c4
                elif name[-6:]=='_5.tif':
                    ref = (numpyimg*m5)+c5
            
                fold = set_dir.split('/')
                setdir = fold[-1]
                fold = fold[-2]
                folderdir = save_dir + '/' + fold
                setdir = folderdir + '/' + setdir
                savedir = filename.split(name)
                savedir = savedir[0].split(set_dir)
                savedir = savedir[1]
                savedir = setdir + savedir
                if not os.path.exists(folderdir):
                    os.mkdir(folderdir)
                if not os.path.exists(setdir):
                    os.mkdir(setdir)
                if not os.path.exists(savedir):
                    os.mkdir(savedir)
                os.chdir(savedir)
    
                img = PIL.Image.fromarray(ref, mode=None)
                img.save(name)
                r = r + 1
            #add 2 to h because 2 avg DN values will be used
            h = h + 2
            a = a + 1
        #if there are two targets but only 1 was used for this folder
        else:
            if dirs[index + 3]==1:
                ref1 = caltarref1[0]
                ref2 = caltarref2[0]
                ref3 = caltarref3[0]
                ref4 = caltarref4[0]
                ref5 = caltarref5[0]
            elif dirs[index + 3]==2:
                ref1 = caltarref1[1]
                ref2 = caltarref2[1]
                ref3 = caltarref3[1]
                ref4 = caltarref4[1]
                ref5 = caltarref5[1]
            DNtar1 = avgtarDN1[h]
            DNtar2 = avgtarDN2[h]
            DNtar3 = avgtarDN3[h] 
            DNtar4 = avgtarDN4[h] 
            DNtar5 = avgtarDN5[h] 
            #loop through all images in folder
            r = 0
            while r < len(imgpaths):
                filename = imgpaths[r]
                name = filename[-14:]
                t = gdal.Open(filename)
                numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
            
                if name[-6:]=='_1.tif':
                    ref = (numpyimg*ref1)/DNtar1
                elif name[-6:]=='_2.tif':
                    ref = (numpyimg*ref2)/DNtar2
                elif name[-6:]=='_3.tif':
                    ref = (numpyimg*ref3)/DNtar3
                elif name[-6:]=='_4.tif':
                    ref = (numpyimg*ref4)/DNtar4
                elif name[-6:]=='_5.tif':
                    ref = (numpyimg*ref5)/DNtar5
            
                fold = set_dir.split('/')
                setdir = fold[-1]
                fold = fold[-2]
                folderdir = save_dir + '/' + fold
                setdir = folderdir + '/' + setdir
                savedir = filename.split(name)
                savedir = savedir[0].split(set_dir)
                savedir = savedir[1]
                savedir = setdir + savedir
                if not os.path.exists(folderdir):
                    os.mkdir(folderdir)
                if not os.path.exists(setdir):
                    os.mkdir(setdir)
                if not os.path.exists(savedir):
                    os.mkdir(savedir)
                os.chdir(savedir)
        
                img = PIL.Image.fromarray(ref, mode=None)
                img.save(name)
                r = r + 1
                #save new images with reflectance values in new folder
            #adding 1 to h because there will only be one avg DN value used from the list
            h = h + 1
            a = a + 1
    elif numtars > 2:
        index2 = dirs.index('x'+str(a+1))
        numtarsforx = ((index2 - index)-3)/2
        if numtarsforx == 1:
            ref1 = caltarref1[dirs[index + 3]-1]
            ref2 = caltarref2[dirs[index + 3]-1]
            ref3 = caltarref3[dirs[index + 3]-1]
            ref4 = caltarref4[dirs[index + 3]-1]
            DNtar1 = avgtarDN1[h]
            DNtar2 = avgtarDN2[h]
            DNtar3 = avgtarDN3[h] 
            DNtar4 = avgtarDN4[h] 
            DNtar5 = avgtarDN5[h] 
            #loop through all images in folder
            r = 0
            while r < len(imgpaths):
                filename = imgpaths[r]
                name = filename[-14:]
                t = gdal.Open(filename)
                numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
            
                if name[-6:]=='_1.tif':
                    ref = (numpyimg*ref1)/DNtar1
                elif name[-6:]=='_2.tif':
                    ref = (numpyimg*ref2)/DNtar2
                elif name[-6:]=='_3.tif':
                    ref = (numpyimg*ref3)/DNtar3
                elif name[-6:]=='_4.tif':
                    ref = (numpyimg*ref4)/DNtar4
                elif name[-6:]=='_5.tif':
                    ref = (numpyimg*ref5)/DNtar5
            
                fold = set_dir.split('/')
                setdir = fold[-1]
                fold = fold[-2]
                folderdir = save_dir + '/' + fold
                setdir = folderdir + '/' + setdir
                savedir = filename.split(name)
                savedir = savedir[0].split(set_dir)
                savedir = savedir[1]
                savedir = setdir + savedir
                if not os.path.exists(folderdir):
                    os.mkdir(folderdir)
                if not os.path.exists(setdir):
                    os.mkdir(setdir)
                if not os.path.exists(savedir):
                    os.mkdir(savedir)
                os.chdir(savedir)
    
                img = PIL.Image.fromarray(ref, mode=None)
                img.save(name)
                r = r + 1
                #save new images with reflectance values in new folder
            #adding 1 to h because there will only be one avg DN value used from the list
            h = h + 1
            a = a + 1
        
        elif numtarsforx == 2:
            #reflectance values for target 1 for each band
            ref1_1 = caltarref1[dirs[index + 3]-1]
            ref2_1 = caltarref2[dirs[index + 3]-1]
            ref3_1 = caltarref3[dirs[index + 3]-1]
            ref4_1 = caltarref4[dirs[index + 3]-1]
            ref5_1 = caltarref5[dirs[index + 3]-1]
            #reflectance values for target 2 for each band
            ref1_2 = caltarref1[dirs[index + 5]-1]
            ref2_2 = caltarref2[dirs[index + 5]-1]
            ref3_2 = caltarref3[dirs[index + 5]-1]
            ref4_2 = caltarref4[dirs[index + 5]-1]
            ref5_2 = caltarref5[dirs[index + 5]-1]
            #avg DN values for target 1 for each band
            DN1_1 = avgtarDN1[h]
            DN2_1 = avgtarDN2[h]
            DN3_1 = avgtarDN3[h]
            DN4_1 = avgtarDN4[h]
            DN5_1 = avgtarDN5[h]
            #avg DN values for target 2 for each band
            DN1_2 = avgtarDN1[h+1]
            DN2_2 = avgtarDN2[h+1]
            DN3_2 = avgtarDN3[h+1]
            DN4_2 = avgtarDN4[h+1]
            DN5_2 = avgtarDN5[h+1]
            #slope for conversion equation for each band
            m1 = (ref1_1-ref1_2)/(DN1_1 - DN1_2)
            m2 = (ref2_1-ref2_2)/(DN2_1 - DN2_2)
            m3 = (ref3_1-ref3_2)/(DN3_1 - DN3_2)
            m4 = (ref4_1-ref4_2)/(DN4_1 - DN4_2)
            m5 = (ref5_1-ref5_2)/(DN5_1 - DN5_2)
            #y-intercept for conversion equation for each band
            c1 = ref1_1 -m1 * DN1_1
            c2 = ref2_1 -m2 * DN2_1
            c3 = ref3_1 -m3 * DN3_1
            c4 = ref4_1 -m4 * DN4_1
            c5 = ref5_1 -m5 * DN5_1
                    
            r = 0
            while r < len(imgpaths):
                filename = imgpaths[r]
                name = filename[-14:]
                t = gdal.Open(filename)
                numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
                
                if name[-6:]=='_1.tif':
                    ref = (numpyimg*m1)+c1
                elif name[-6:]=='_2.tif':
                    ref = (numpyimg*m2)+c2
                elif name[-6:]=='_3.tif':
                    ref = (numpyimg*m3)+c3
                elif name[-6:]=='_4.tif':
                    ref = (numpyimg*m4)+c4
                elif name[-6:]=='_5.tif':
                    ref = (numpyimg*m5)+c5
            
                fold = set_dir.split('/')
                setdir = fold[-1]
                fold = fold[-2]
                folderdir = save_dir + '/' + fold
                setdir = folderdir + '/' + setdir
                savedir = filename.split(name)
                savedir = savedir[0].split(set_dir)
                savedir = savedir[1]
                savedir = setdir + savedir
                if not os.path.exists(folderdir):
                    os.mkdir(folderdir)
                if not os.path.exists(setdir):
                    os.mkdir(setdir)
                if not os.path.exists(savedir):
                    os.mkdir(savedir)
                os.chdir(savedir)
    
                img = PIL.Image.fromarray(ref, mode=None)
                img.save(name)
                r = r + 1
            #add 2 to h because 2 avg DN values will be used
            h = h + 2
            a = a + 1
        
        elif numtarsforx >2:
            listavgDN1 = []
            listcaltarref1 = []
            listavgDN2 = []
            listcaltarref2 = []
            listavgDN3 = []
            listcaltarref3 = []
            listavgDN4 = []
            listcaltarref4 = []
            listavgDN5 = []
            listcaltarref5 = []
            
            j = 0
            o = 3
            while j < numtarsforx:
                listavgDN1.append(avgtarDN1[h+j])
                listavgDN2.append(avgtarDN2[h+j])
                listavgDN3.append(avgtarDN3[h+j])
                listavgDN4.append(avgtarDN4[h+j])
                listavgDN5.append(avgtarDN5[h+j])
                
                listcaltarref1.append(caltarref1[dirs[index + o]-1])
                listcaltarref2.append(caltarref2[dirs[index + o]-1])
                listcaltarref3.append(caltarref3[dirs[index + o]-1])
                listcaltarref4.append(caltarref4[dirs[index + o]-1])
                listcaltarref5.append(caltarref5[dirs[index + o]-1])
                
                o = o + 2
                j = j + 1
            
            
            m1, c1, r1, p1, std1 = stats.linregress(listavgDN1,listcaltarref1)
            m2, c2, r2, p2, std2 = stats.linregress(listavgDN2,listcaltarref2)
            m3, c3, r3, p3, std3 = stats.linregress(listavgDN3,listcaltarref3)
            m4, c4, r4, p4, std4 = stats.linregress(listavgDN4,listcaltarref4)
            m5, c5, r5, p5, std5 = stats.linregress(listavgDN5,listcaltarref5)
            
            r = 0
            while r < len(imgpaths):
                filename = imgpaths[r]
                name = filename[-14:]
                t = gdal.Open(filename)
                numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
                
                if name[-6:]=='_1.tif':
                    ref = (numpyimg*m1)+c1
                elif name[-6:]=='_2.tif':
                    ref = (numpyimg*m2)+c2
                elif name[-6:]=='_3.tif':
                    ref = (numpyimg*m3)+c3
                elif name[-6:]=='_4.tif':
                    ref = (numpyimg*m4)+c4
                elif name[-6:]=='_5.tif':
                    ref = (numpyimg*m5)+c5
                
                fold = set_dir.split('/')
                setdir = fold[-1]
                fold = fold[-2]
                folderdir = save_dir + '/' + fold
                setdir = folderdir + '/' + setdir
                savedir = filename.split(name)
                savedir = savedir[0].split(set_dir)
                savedir = savedir[1]
                savedir = setdir + savedir
                if not os.path.exists(folderdir):
                    os.mkdir(folderdir)
                if not os.path.exists(setdir):
                    os.mkdir(setdir)
                if not os.path.exists(savedir):
                    os.mkdir(savedir)
                os.chdir(savedir)
    
                img = PIL.Image.fromarray(ref, mode=None)
                img.save(name)
                r = r + 1
            #create text document with values from linear regression
            info = open(savedir+'/'+'info.txt','a')
            info.close()
            info2 = open(savedir+'/'+ 'info.txt','w')
            info2.write('Linear regression data:' + "\n" \
            'band number, slope, y-intercept, r value, p value, standard devation' + "\n"\
            '1, '+str(m1)+', '+str(c1)+', '+str(r1)+', '+str(p1)+', '+str(std1)+"\n"+\
            '2, '+str(m2)+', '+str(c2)+', '+str(r2)+', '+str(p2)+', '+str(std2)+"\n"+\
            '3, '+str(m3)+', '+str(c3)+', '+str(r3)+', '+str(p3)+', '+str(std3)+"\n"+\
            '4, '+str(m4)+', '+str(c4)+', '+str(r4)+', '+str(p4)+', '+str(std4)+"\n"+\
            '5, '+str(m5)+', '+str(c5)+', '+str(r5)+', '+str(p5)+', '+str(std5)+"\n")
                        
            info2.close()
            #add 2 to h because 2 avg DN values will be used
            h = h + numtarsforx
            a = a + 1
            
    
    
