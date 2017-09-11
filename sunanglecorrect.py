# Correction of imagery based on the sun angle 
import os
from osgeo import gdal
import numpy
import exifread
import math
import Tkinter
import tkFileDialog
import PIL
from sunpy import sun
import time


root = Tkinter.Tk()
currdir = os.getcwd() # current working directory
orig_img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the directory which contains "SET" folders of your original images with exif information. ' )) # generates GUI for selecting directory with images

#get directory for photos that will be edited
root = Tkinter.Tk()
img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=orig_img_dir, title='Please select the directory which contains "SET" folders of the images to perform a sun angle correction on. ' )) # generates GUI for selecting directory with images

#get save directory 
root = Tkinter.Tk()
save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=img_dir, title='Please select your save directory.' )) # generates GUI for selecting save directory

UTCoffset = time.timezone/3600.0

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

#looping through photos and generating new sun angle corrected photos
origimgpaths = filenames(orig_img_dir)

x = 0
y = 0

a = 0

import exifread 

while a < len(origimgpaths):
    origfilename = origimgpaths[a]
    name = origfilename[-14:]
    subdir = origfilename.split(orig_img_dir)
    filename = img_dir + subdir[1]
    if not os.path.exists(filename):
        a = a + 1
    else:
        t = gdal.Open(filename)
        numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
        dimensions = numpyimg.shape
        h = int(dimensions[0])
        w = int(dimensions[1])
        newimage = numpy.zeros((h,w))
        
        #generating exif dictionary
        f = open(filename,'rb')
        tags = exifread.process_file(f, details=False)
        photodatetime = tags['EXIF DateTimeDigitized']
        photodatetime = str(photodatetime)
        photodatetime = photodatetime.split(':')
        year = int(photodatetime[0])
        month = int(photodatetime[1])
        day = photodatetime[2].split(' ')
        # hour must be in UTC time
        hour = int(day[1])
        day = int(day[0])
        minute = int(photodatetime[3])
        second = int(photodatetime[4])
        
        millisecond = tags['EXIF SubSecTime']
        millisecond = str(millisecond)
        millisecond = millisecond[:6]
        millisecond = int(millisecond)
        
        time = (year, month, day, hour, minute, second, millisecond)
        
        #calculating solar declination angle at time photo was taken
        sundec = sun.true_declination(time)
        sundec = str(sundec)
        sundec = sundec.split('d')
        sundecdeg = float(sundec[0])
        sundec = sundec[1].split('m')
        sundecmin = float(sundec[0])
        sundec = sundec[1].split('s')
        sundecsec = float(sundec[0])
        
        sundec = sundecdeg + (sundecmin/60) + (sundecsec/60/60)
        sundecrad = math.radians(sundec)

        #calculating hour angle
        localhour = hour + UTCoffset
        h = ((float(localhour) + (float(minute)/60) + (float(second)/60/60))-12)*15
        hrad = math.radians(h)
        

        lat1 = str(tags['GPS GPSLatitude'])
        lat2 = lat1.split('[')
        lat3 = lat2[1]
        lat4 = lat3.split(']')
        lat5 = lat4[0]
        lat6 = lat5.split(',')
        latdeg = float(lat6[0])
        latmin = float(lat6[1])
        latsec1 = lat6[2]
        latsec2 = latsec1.split('/')
        latsec = float(latsec2[0])/ float(latsec2[1])
        latsign = str(tags['GPS GPSLatitudeRef'])
        if latsign == 'S':
            lat = float(-1) * (latdeg + ((latmin + (latsec/float(60)))/float(60)))
        elif latsign == 'N':
            lat = latdeg + ((latmin + (latsec/float(60)))/float(60))
            
        latrad = math.radians(lat)
                
        # Calculating sun angle in radians
        selevang = math.asin(math.sin(latrad)*math.sin(sundecrad)+math.cos(latrad)*math.cos(sundecrad)*math.cos(hrad))
        
        newimage = numpyimg / math.sin(selevang)
        
        #save new matrix as new image
        #create appropriate subdirectories
        savedir = save_dir + subdir[1][:-15]
        subdir1 = subdir[1].split('SET')
        setdir = save_dir + subdir1[0]+'SET'
        if not os.path.exists(setdir):
            os.mkdir(setdir)
        if not os.path.exists(savedir):
            os.mkdir(savedir)
            
        os.chdir(savedir)
        # performs exposure compensation on images using equation from Pix4D, 2017
        img = PIL.Image.fromarray(newimage, mode=None)
        img.save(name)
        a = a + 1