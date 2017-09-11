#Python code for performing an Empirical Line Calibration on MicaSense RedEdge imagery
#Minimum requirements: image of at least 1 calibration target taken before or after mission &
#reflectance values corresponding to the MicaSense RedEdge bands for each of the calibration targets

import numpy
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
    master.quit()
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

dirs = []
#have user select calibration target images and corresponding images until they hit cancel
orig_img_dir = '1'
while orig_img_dir:
    h = 1
    while h<=numtars:
        root = Tkinter.Tk()
        root.withdraw() #use to hide tkinter window
        currdir = os.getcwd()
        band1 = str(tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a location for target ' + str(h) + " Band 1 or hit cancel for different target number" ))
        dirs.append(band1)
        h = h + 1
    #get directory for photos that will be edited
    root = Tkinter.Tk()
    img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=orig_img_dir, title='Please select the "SET" folder of images that correspond to the previously selected calibration target image(s).' )) # generates GUI for selecting directory with images
    dirs.append(img_dir)
    dirs.append('x')

    



root = Tkinter.Tk()
root.withdraw() #use to hide tkinter window
currdir = os.getcwd()
save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select your save directory' ))


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
h = 0
while h < numtars:
    #for band 1
    image = imread(caltarband1[h])
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
    image = imread(caltarband1[h][:-5]+'2.tif')
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
    image = imread(caltarband1[h][:-5]+'3.tif')
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
    image = imread(caltarband1[h][:-5]+'4.tif')
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
    image = imread(caltarband1[h][:-5]+'5.tif')
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

    h = h + 1

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


if numtars == 1:
    ref1 = caltarref1[0]
    ref2 = caltarref2[0]
    ref3 = caltarref3[0]
    ref4 = caltarref4[0]
    ref5 = caltarref5[0]
    m1 = (ref1 + 0.05044)/avgtarDN1[0] #Tagle, 2017
    m2 = (ref2 + 0.07579)/avgtarDN2[0] #Tagle, 2017
    m3 = (ref3 + 0.01111)/avgtarDN3[0] #Tagle, 2017
    m4 = (ref4 + 0.01559)/avgtarDN4[0] #Tagle, 2017
    m5 = (ref5 + 0.02259)/avgtarDN5[0] #Tagle, 2017
    c1 = -0.05044 #Tagle, 2017
    c2 = -0.07579 #Tagle, 2017
    c3 = -0.01111 #Tagle, 2017
    c4 = -0.01559 #Tagle, 2017
    c5 = -0.02259 #Tagle, 2017
else:
    m1, c1, r, p, std = stats.linregress(avgtarDN1,caltarref1)
    m2, c2, r, p, std = stats.linregress(avgtarDN2,caltarref2)
    m3, c3, r, p, std = stats.linregress(avgtarDN3,caltarref3)
    m4, c4, r, p, std = stats.linregress(avgtarDN4,caltarref4)
    m5, c5, r, p, std = stats.linregress(avgtarDN5,caltarref5)

#loop through all images in folder
imgpaths = filenames(img_dir)

r = 0
while r < len(imgpaths):
    filename = imgpaths[r]
    name = filename[-14:]
    t = gdal.Open(filename)
    numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())

    if name[-6:]=='_1.tif':
        ref = (m1 * numpyimg) + c1
    elif name[-6:]=='_2.tif':
        ref = (m2 * numpyimg) + c2
    elif name[-6:]=='_3.tif':
        ref = (m3 * numpyimg) + c3
    elif name[-6:]=='_4.tif':
        ref = (m4 * numpyimg) + c4
    elif name[-6:]=='_5.tif':
        ref =(m5 * numpyimg) + c5

    subdir = filename.split(img_dir)
    savedir = save_dir + subdir[0][-8:] + subdir[1][:-15]
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    os.chdir(savedir)
    img = ref*10000
    img = img.astype(numpy.uint16)
    img = PIL.Image.fromarray(img, mode=None)
    img.save(name)
    r = r + 1
    #save new images with reflectance values in new folder
