import Tkinter
import PIL
from osgeo import gdal
import os
import numpy
import exifread
import exiftool
import tkFileDialog
from Tkinter import *
import math 

numfoldlist = []

def take():
    numfold = int(e1.get())
    e1.delete(0,END)
    numfoldlist.append(numfold)
    master.destroy ()
    return

master = Tk()
master.title("Exposure Compensation, DLS Correction and Vignetting Correction for MicaSense RedEdge Imagery")
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
while h <= numfolds:
    #only perform an Exposure Compensation if you camera was on automatic mode (i.e. had changing shutter speed)
    root = Tkinter.Tk()
    currdir = os.getcwd() # current working directory
    img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select your image directory for folder ' + str(h) )) # generates GUI for selecting directory with images
    imgdirs.append(img_dir)
    
    root = Tkinter.Tk()
    save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=img_dir, title='Please select your save directory for folder ' + str(h) )) # generates GUI for selecting save directory
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

#looping through folders and photos and generating new sun angle corrected photos
d = 0
#empty list for saving DLS values

while d < numfolds:
    # opens each image as numpyarray
    imgpaths = filenames(imgdirs[d])
    # going through each image and determining the DLS value and adding it to a list to calculate the maximum later

    numimgs = len(imgpaths)
    
    os.chdir('E:\Georef_UAS_Program')
    with exiftool.ExifTool() as et:
        DLS = et.get_tag_batch('XMP:SpectralIrradiance',imgpaths[:])
        j = et.get_tag_batch('XMP:VignettingPolynomial',imgpaths[:])
        c = et.get_tag_batch('XMP:VignettingCenter',imgpaths[:])
        
    a = 0
    while a < numimgs:
        filename = imgpaths[a]
        name = filename[-14:]
        t = gdal.Open(filename)
        numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
    
        # reads exposure, aperture and ISO speed
        import exifread
        f = open(filename,'rb')
        # reading exif of image, generates a dictionary
        tags = exifread.process_file(f, details=False)
        # getting specific information from exif tags
        # aperture
        if not 'EXIF FNumber' in tags:
            k = 'x'
            print filename + ' has no FNumber information!'
        else:
            k = tags['EXIF FNumber']
            k = str(k)
            k = k.split('/')
            k = float(k[0])/float(k[1])
    
        # exposure
        if not 'EXIF ExposureTime' in tags:
            exp = 'x'
            print filename + ' has no Exposure information!'
        else:
            exp = tags['EXIF ExposureTime']
            exp = str(exp)
            exp = exp.split('/')
            exp = float(exp[0])/float(exp[1])
    
        #ISO
        if not 'EXIF ISOSpeed' in tags:
            K = 'x'
            print filename + ' has no ISO information!'
        else:
            K = tags['EXIF ISOSpeed']
            K = str(K)
            K = int(K)
    
        # saving images in the same subdirectory format in the save directory
        if k == 'x' or exp == 'x' or K == 'x':
            a = a + 1
        else:
            #perform exposure compensation
            numpyimg = numpyimg * ((((1/k)**2)/(exp*K)))
            
            #perform DLS compensation
            DLSnum = float(DLS[a])
            numpyimg = numpyimg * (1/DLSnum)
            
            #perform vignette correction
            dimensions = numpyimg.shape
            h = int(dimensions[0])
            w = int(dimensions[1])
            newimage = numpy.zeros((h,w))
            #change directory to exiftool
            kk = j[a]
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
            
            subdir = filename.split(imgdirs[d])        
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
            # exports images as tiffs
    d = d + 1
