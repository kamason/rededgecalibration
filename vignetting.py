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

d = 0

while d < numfolds:
    origimgpaths = filenames(origimgdirs[d])
    
    numimgs = len(origimgpaths)

    a = 0
    
    os.chdir('F:\Workspace')
    with exiftool.ExifTool() as et:
        k = et.get_tag_batch('XMP:VignettingPolynomial',origimgpaths[:])
        c = et.get_tag_batch('XMP:VignettingCenter',origimgpaths[:])

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
            dimensions = numpyimg.shape
            h = int(dimensions[0])
            w = int(dimensions[1])
            newimage = numpy.zeros((h,w))
            #change directory to exiftool
            kk = k[a]
            cc = c[a]
            
            k0 = float(kk[0])
            k1 = kk[1]
            k2 = kk[2]
            k3 = kk[3]
            k4 = kk[4]
            k5 = kk[5]
            cx = cc[0]
            cy = cc[1]
        
            x = 0
            y = 0
            
            while x < w:
                while y < h:
                    x = x + 1
                    y = y + 1
                    r = math.sqrt(((x-cx)**2)+((y-cy)**2))
                    k6 = 1 + k0 * r + k1 * r**2 + k2 * r**3 + k3 * r**4 + k4 * r**5 + k5 * r**6
                    x = x - 1
                    y = y - 1
                    newimage[y,x]=numpyimg[y,x]/k6
                    y = y + 1
                y=0
                x = x + 1
            #save new matrix as new image
            #create appropriate subdirectories
            savedir = savedirs[d] + subdir[1][:-15]
            subdir1 = subdir[1].split('SET')
            setdir = savedirs[d] + subdir1[0]+'SET'
            if not os.path.exists(setdir):
                os.mkdir(setdir)
            if not os.path.exists(savedir):
                os.mkdir(savedir)
            os.chdir(savedir)
            # performs exposure compensation on images using equation from Pix4D, 2017
            img = PIL.Image.fromarray(newimage, mode=None)
            img.save(name)
            a = a + 1
    d = d + 1
