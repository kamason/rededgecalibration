# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 13:01:46 2017

@author: kmason
"""

#radiance conversion using MicaSense modules
import micasense.utils as msutils
import micasense.metadata as metadata
import Tkinter
import tkFileDialog
import PIL
from Tkinter import *
import os
import matplotlib.pyplot as plt


#List for holding number of folders taken from Tkinter GUI
numfoldlist = []

#function for saving user input to Tkinter GUI
def take():
    numfold = int(e1.get())
    e1.delete(0,END)
    numfoldlist.append(numfold)
    master.destroy ()
    return

#GUI for asking user how many folders the user will be inputting
master = Tk()
master.title("Radiometric Correction for MicaSense Imagery")
Label(master, text="Number of folders:").grid(row=1)
e1 = Entry(master)
e1.grid(row=1, column=1)
Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=W, pady=4)
Button(master, text='Enter', command=take).grid(row=17, column=1, sticky=W, pady=4)

master.mainloop ()

#extracting the number of folders from the list, this is just a quirk of Tkinter
numfolds = numfoldlist[0]

#ask user where exiftool.exe is located. This is neccessary for using the exiftool module.
root = Tkinter.Tk()
currdir = os.getcwd() # current working directory
exiftoolloc = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the directory where exiftool.exe is located'))


#empty list for image directories and save directories. There will be the same number of each that corresponds to the number of folders.
origimgdirs = []
savedirs = []

#For every folder user selects image directory of images to be corrected and save directory 
h = 1
while h <= numfolds:
    root = Tkinter.Tk()
    currdir = os.getcwd() # current working directory
    orig_img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the directory which contains the "SET" folders of your original images with exif information for folder ' + str(h) + '.' )) # generates GUI for selecting directory with images
    origimgdirs.append(orig_img_dir)
    
    #get save directory 
    root = Tkinter.Tk()
    save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=orig_img_dir, title='Please select your save directory for folder ' + str(h) + '.' )) # generates GUI for selecting save directory
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

d = 0
#for looping through folders
while d < numfolds:
    #determining the file paths for the images in the image directory provided by the user
    origimgpaths = filenames(origimgdirs[d])
    
    numimgs = len(origimgpaths)
    
    a = 0
    #loop through images in folder "d"
    while a < numimgs:

        imageName = origimgpaths[a]
        imageRaw=plt.imread(imageName)
        name = imageName[-14:]
        exiftoolPath = None
        if os.name == 'nt':
            exiftoolPath = exiftoolloc
        # get image metadata
        meta = metadata.Metadata(imageName, exiftoolPath=exiftoolPath)
        
        #calculating radiance image from raw image using micasense module 
        radianceImage, L, V, R = msutils.raw_image_to_radiance(meta, imageRaw)
        
        #Saving the images in the same file format as they were originally
        #checking if folder is already there and if not, the folder is generated
        #The file structure is essentially \\PATHOFSAVEDIRECTORY\\000SET\\000
        #You have to determine what number the set folder is (i.e. 000SET or 001SET or 002SET) as well as which final folder number (000, 001, 002 etc.)
        #split filename at image directory
        subdir = imageName.split(origimgdirs[d]) 
        # merging save directory for folder "d" with the SET and 000 folders for the specific image file
        savedir = savedirs[d] + subdir[1][:-15]
        subdir1 = subdir[1].split('SET')
        setdir = savedirs[d] + subdir1[0]+'SET'
        #if the path doesn't exist, make it
        if not os.path.exists(setdir):
            os.mkdir(setdir)
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        os.chdir(savedir)
        img = PIL.Image.fromarray(radianceImage, mode=None)
        img.save(name)
        #save image as tif
        a = a + 1
    d = d + 1