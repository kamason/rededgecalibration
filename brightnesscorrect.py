import Tkinter
import sys
import ttk
from Tkinter import *
import PIL
from osgeo import gdal
import os
import numpy
import exifread
import tkFileDialog

numfoldlist = []

def take():
    numfold = int(e1.get())
    e1.delete(0,END)
    numfoldlist.append(numfold)
    master.destroy ()
    return

master = Tk()
master.title("Brightness Correction")
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
    img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the directory which contains the "SET" folders images to perform a brightness correction on for folder ' + str(h) + '.' )) # generates GUI for selecting directory with images
    imgdirs.append(img_dir)
    
    #get save directory 
    root = Tkinter.Tk()
    save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=img_dir, title='Please select your save directory for folder ' + str(h) + '.' )) # generates GUI for selecting save directory
    savedirs.append(save_dir)
    currdir = img_dir
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

while d < numfolds:
    imgpaths = filenames(imgdirs[d])

    # opens each image as numpyarray
    r = 0
    while r < len(imgpaths):
        filename = imgpaths[r]
        name = filename[-14:]
        t = gdal.Open(filename)
        numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
                    
        if name[-6:]=='_1.tif':
            img = numpyimg * 1.17690998434
        elif name[-6:]=='_2.tif':
            img = numpyimg
        elif name[-6:]=='_3.tif':
            img = numpyimg * 2.32330134871
        elif name[-6:]=='_4.tif':
            img = numpyimg * 4.8033760412
        elif name[-6:]=='_5.tif':
            img = numpyimg * 4.63704730693
                            
        subdir = filename.split(img_dir)        
        savedir = savedirs[d] + subdir[1][:-15]
        subdir1 = subdir[1].split('SET')
        setdir = savedirs[d] + subdir1[0]+'SET'
        if not os.path.exists(setdir):
            os.mkdir(setdir)
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        os.chdir(savedir)
        img = PIL.Image.fromarray(img, mode=None)
        img.save(name)
        r = r + 1

    d = d + 1