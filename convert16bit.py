# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 15:59:20 2017

@author: kmason

"""
# for converting from float images to 16 bit images and keeping relationships between values
# must run this code on the entire set of images that will be used in an orthophoto as well as the calibration target images that will be used for ELC
import os
from osgeo import gdal
import numpy
import tkFileDialog
import Tkinter
from Tkinter import *
import PIL

numfoldlist = []

def take():
    numfold = int(e1.get())
    e1.delete(0,END)
    numfoldlist.append(numfold)
    master.destroy ()
    return

master = Tk()
master.title("Convert Float Imagery to 16 bit Unsigned Integer")
Label(master, text="Number of folders:").grid(row=1)
e1 = Entry(master)
e1.grid(row=1, column=1)
Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=W, pady=4)
Button(master, text='Enter', command=take).grid(row=17, column=1, sticky=W, pady=4)

master.mainloop ()

numfolds = numfoldlist[0]

imgdirs = []
savedirs = []

h = 1
currdir = os.getcwd()
while h <= numfolds:
    #get directory for photos that will be edited
    root = Tkinter.Tk()
    img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the directory which contains the "SET" folders of the float images to convert to 16 bit for folder ' + str(h) + '.' )) # generates GUI for selecting directory with images
    imgdirs.append(img_dir)
    
    #get save directory 
    root = Tkinter.Tk()
    save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=img_dir, title='Please select your save directory for folder ' + str(h) + '.' )) # generates GUI for selecting save directory
    savedirs.append(save_dir)
    currdir = img_dir
    h = h + 1

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
        leneb4 = len(e)
        for otherdir in p:
            for img in z:
                u = os.path.join(folder,setdir,otherdir,img)
                #make file path out of all combinations of SET folders, other folders and images
                if os.path.exists(u) == True:
                #if that image / location actually exists append it to the list
                    e.append(u)
    return e

maxDNs = []
minDNs = []

d = 0

while d < numfolds:
    origimgpaths = filenames(imgdirs[d])
    # going through each image and determining the DLS value and adding it to a list to calculate the maximum later

    numimgs = len(origimgpaths)
    a = 0 
            
    while a < numimgs:
        origfilename = origimgpaths[a]
        subdir = origfilename.split(imgdirs[d])
        filename = imgdirs[d] + subdir[1]
        if not os.path.exists(filename):
            a = a + 1
        else:
            name = filename[-14:]
            t = gdal.Open(filename)
            numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
            maxDN = numpy.amax(numpyimg)
            maxDNs.append(maxDN)
            minDN = numpy.amin(numpyimg)
            minDNs.append(minDN)
            a = a + 1
    d = d + 1

maxmaxDNs = max(maxDNs)
minminDNs = min(minDNs)

def normalize(image,minall,maxall):
    floatimg = image.astype(float)
    #converts 16bit numpy array to float
    normalimg = ((floatimg - minall) * 65535) / (maxall-minall)
    #normalizes image to between 0 and 1 and then to 16 bit range
    newimage = normalimg.astype(numpy.uint16)
    #changes image back from float to 16bit
    return newimage

d = 0 

while d < numfolds:
    origimgpaths = filenames(imgdirs[d])
    # going through each image and determining the DLS value and adding it to a list to calculate the maximum later

    numimgs = len(origimgpaths)
    a = 0 
            
    while a < numimgs:
        origfilename = origimgpaths[a]
        subdir = origfilename.split(imgdirs[d])
        filename = imgdirs[d] + subdir[1]
        if not os.path.exists(filename):
            a = a + 1
        else:
            name = filename[-14:]
            t = gdal.Open(filename)
            numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
            
            img = normalize(numpyimg,minminDNs,maxmaxDNs)
            
            savedir = savedirs[d] + subdir[1][:-15]
            subdir1 = subdir[1].split('SET')
            setdir = savedirs[d] + subdir1[0]+'SET'
            if not os.path.exists(setdir):
                os.mkdir(setdir)
            if not os.path.exists(savedir):
                os.mkdir(savedir)
            os.chdir(savedir)
            # performs exposure compensation on images using equation from Pix4D, 2017
            img = PIL.Image.fromarray(img, mode=None)
            img.save(name)
            a = a + 1
    info = open(savedirs[d]+'/'+'info.txt','a')
    info.close()
    info2 = open(savedirs[d]+'/'+ 'info.txt','w')
    info2.write('Information for converting from 16 bit back to original values' + "\n" + 'Max DN: ' + str(maxmaxDNs) + "\n" +  'Min DN: '+ str(minminDNs))
    info2.close()
    d = d + 1
    

