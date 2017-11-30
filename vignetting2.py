# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 12:57:17 2017

@author: kmason
"""

#remove vignetting of MicaSense RedEdge imagery
#this code requires that images were taken with RedEdge hardware version 2.1.0 or later
#Keep images in the same directory format as they were taken in 
import os
from osgeo import gdal
import numpy
import exifread
import math
import Tkinter
import tkFileDialog
import PIL
from Tkinter import *

numfoldlist = []

def take():
    numfold = int(e1.get())
    e1.delete(0,END)
    numfoldlist.append(numfold)
    master.destroy ()
    return

master = Tk()
master.title("Vignetting Correction for MicaSense Imagery")
Label(master, text="Number of folders:").grid(row=1)
e1 = Entry(master)
e1.grid(row=1, column=1)
Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=W, pady=4)
Button(master, text='Enter', command=take).grid(row=17, column=1, sticky=W, pady=4)

master.mainloop ()

numfolds = numfoldlist[0]

root = Tkinter.Tk()
currdir = os.getcwd() # current working directory
exiftoolloc = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the directory where exiftool.exe is located'))


imgdirs = []
origimgdirs = []
savedirs = []
    
h = 1
while h <= numfolds:
    root = Tkinter.Tk()
    currdir = os.getcwd() # current working directory
    orig_img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the directory which contains the "SET" folders of your original images with exif information for folder ' + str(h) + '.' )) # generates GUI for selecting directory with images
    origimgdirs.append(orig_img_dir)
    
    #get directory for photos that will be edited
    root = Tkinter.Tk()
    img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=orig_img_dir, title='Please select the directory which contains the "SET" folders of the images to perform a vignette correction on for folder ' + str(h) + '.' )) # generates GUI for selecting directory with images
    imgdirs.append(img_dir)
    
    #get save directory 
    root = Tkinter.Tk()
    save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=img_dir, title='Please select your save directory for folder ' + str(h) + '.' )) # generates GUI for selecting save directory
    savedirs.append(save_dir)
    
    h = h + 1
    
root = Tkinter.Tk()
currdir = os.getcwd() # current working directory
band1 = str(tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a band 1 image')) # generates GUI for selecting directory with images

root = Tkinter.Tk()
band2 = str(tkFileDialog.askopenfilename(parent=root, initialdir=os.path.dirname(band1), title='Please select a band 2 image')) 

root = Tkinter.Tk()
band3 = str(tkFileDialog.askopenfilename(parent=root, initialdir=os.path.dirname(band2), title='Please select a band 3 image')) 

root = Tkinter.Tk()
band4 = str(tkFileDialog.askopenfilename(parent=root, initialdir=os.path.dirname(band3), title='Please select a band 4 image')) 

root = Tkinter.Tk()
band5 = str(tkFileDialog.askopenfilename(parent=root, initialdir=os.path.dirname(band4), title='Please select a band 5 image')) 

# generate list with paths for all images
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

import exiftool 

os.chdir(exiftoolloc)
with exiftool.ExifTool() as et:
    k1 = et.get_tag('XMP:VignettingPolynomial',band1)
    c1 = et.get_tag('XMP:VignettingCenter',band1)
    k2 = et.get_tag('XMP:VignettingPolynomial',band2)
    c2 = et.get_tag('XMP:VignettingCenter',band2)
    k3 = et.get_tag('XMP:VignettingPolynomial',band3)
    c3 = et.get_tag('XMP:VignettingCenter',band3)
    k4 = et.get_tag('XMP:VignettingPolynomial',band4)
    c4 = et.get_tag('XMP:VignettingCenter',band4)
    k5 = et.get_tag('XMP:VignettingPolynomial',band5)
    c5 = et.get_tag('XMP:VignettingCenter',band5)
        
k1_0 = float(k1[0])
k1_1 = k1[1]
k1_2 = k1[2]
k1_3 = k1[3]
k1_4 = k1[4]
k1_5 = k1[5]
c1_x = c1[0]
c1_y = c1[1]

k2_0 = float(k2[0])
k2_1 = k2[1]
k2_2 = k2[2]
k2_3 = k2[3]
k2_4 = k2[4]
k2_5 = k2[5]
c2_x = c2[0]
c2_y = c2[1]

k3_0 = float(k3[0])
k3_1 = k3[1]
k3_2 = k3[2]
k3_3 = k3[3]
k3_4 = k3[4]
k3_5 = k3[5]
c3_x = c3[0]
c3_y = c3[1]

k4_0 = float(k4[0])
k4_1 = k4[1]
k4_2 = k4[2]
k4_3 = k4[3]
k4_4 = k4[4]
k4_5 = k4[5]
c4_x = c4[0]
c4_y = c4[1]

k5_0 = float(k5[0])
k5_1 = k5[1]
k5_2 = k5[2]
k5_3 = k5[3]
k5_4 = k5[4]
k5_5 = k5[5]
c5_x = c5[0]
c5_y = c5[1]

h = 960
w = 1280

newimage = numpy.ones((h,w))
band1vig = numpy.ones((h,w))
band2vig = numpy.ones((h,w))
band3vig = numpy.ones((h,w))
band4vig = numpy.ones((h,w))
band5vig = numpy.ones((h,w))

x = 0
y = 0
            
while x < w:
    while y < h:
        x = x + 1
        y = y + 1
        r = math.sqrt(((x-c1_x)**2)+((y-c1_y)**2))
        k6 = 1 + k1_0 * r + k1_1 * r**2 + k1_2 * r**3 + k1_3 * r**4 + k1_4 * r**5 + k1_5 * r**6
        x = x - 1
        y = y - 1
        band1vig[y,x]=k6
        y = y + 1
    y=0
    x = x + 1
    
x = 0
y = 0
            
while x < w:
    while y < h:
        x = x + 1
        y = y + 1
        r = math.sqrt(((x-c2_x)**2)+((y-c2_y)**2))
        k6 = 1 + k2_0 * r + k2_1 * r**2 + k2_2 * r**3 + k2_3 * r**4 + k2_4 * r**5 + k2_5 * r**6
        x = x - 1
        y = y - 1
        band2vig[y,x]=k6
        y = y + 1
    y=0
    x = x + 1

x = 0
y = 0
            
while x < w:
    while y < h:
        x = x + 1
        y = y + 1
        r = math.sqrt(((x-c3_x)**2)+((y-c3_y)**2))
        k6 = 1 + k3_0 * r + k3_1 * r**2 + k3_2 * r**3 + k3_3 * r**4 + k3_4 * r**5 + k3_5 * r**6
        x = x - 1
        y = y - 1
        band3vig[y,x]=k6
        y = y + 1
    y=0
    x = x + 1

x = 0
y = 0
            
while x < w:
    while y < h:
        x = x + 1
        y = y + 1
        r = math.sqrt(((x-c4_x)**2)+((y-c4_y)**2))
        k6 = 1 + k4_0 * r + k4_1 * r**2 + k4_2 * r**3 + k4_3 * r**4 + k4_4 * r**5 + k4_5 * r**6
        x = x - 1
        y = y - 1
        band4vig[y,x]=k6
        y = y + 1
    y=0
    x = x + 1

x = 0
y = 0
            
while x < w:
    while y < h:
        x = x + 1
        y = y + 1
        r = math.sqrt(((x-c5_x)**2)+((y-c5_y)**2))
        k6 = 1 + k5_0 * r + k5_1 * r**2 + k5_2 * r**3 + k5_3 * r**4 + k5_4 * r**5 + k5_5 * r**6
        x = x - 1
        y = y - 1
        band5vig[y,x]=k6
        y = y + 1
    y=0
    x = x + 1
    


d = 0

while d < numfolds:
    origimgpaths = filenames(origimgdirs[d])
    
    numimgs = len(origimgpaths)

    a = 0

    while a < numimgs:
        origfilename = origimgpaths[a]
        subdir = origfilename.split(origimgdirs[d])
        filename = imgdirs[d] + subdir[1]
        if not os.path.exists(filename):
            a = a + 1
        else:
            name = filename[-14:]
            t = gdal.Open(filename)
            numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
            
            
            if name[-6:]=='_1.tif':
                newimage = numpyimg / band1vig
            elif name[-6:]=='_2.tif':
                newimage = numpyimg / band2vig
            elif name[-6:]=='_3.tif':
                newimage = numpyimg / band3vig
            elif name[-6:]=='_4.tif':
                newimage = numpyimg / band4vig
            elif name[-6:]=='_5.tif':
                newimage = numpyimg / band5vig
            
            #create appropriate subdirectories
            savedir = savedirs[d] + subdir[1][:-15]
            subdir1 = subdir[1].split('SET')
            setdir = savedirs[d] + subdir1[0]+'SET'
            if not os.path.exists(setdir):
                os.mkdir(setdir)
            if not os.path.exists(savedir):
                os.mkdir(savedir)
            os.chdir(savedir)
            img = PIL.Image.fromarray(newimage, mode=None)
            img.save(name)
            a = a + 1
    d = d + 1
