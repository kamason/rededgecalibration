# Correction of imagery based on the sun angle 
import os
from osgeo import gdal
import numpy
import exifread
import math
import Tkinter
from Tkinter import *
import tkFileDialog
import PIL
from sunpy import sun
import time
import timezonefinder
import pytz
import datetime

numfoldlist = []

def take():
    numfold = int(e1.get())
    e1.delete(0,END)
    numfoldlist.append(numfold)
    master.destroy ()
    return

master = Tk()
master.title("Sun Angle Correction for MicaSense RedEdge Imagery")
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
    orig_img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the directory which contains "SET" folders of your original images with exif information. ' )) # generates GUI for selecting directory with images
    origimgdirs.append(orig_img_dir)
    
    #get directory for photos that will be edited
    root = Tkinter.Tk()
    img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=orig_img_dir, title='Please select the directory which contains "SET" folders of the images to perform a sun angle correction on. ' )) # generates GUI for selecting directory with images
    imgdirs.append(img_dir)
    
    #get save directory 
    root = Tkinter.Tk()
    save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=img_dir, title='Please select your save directory.' )) # generates GUI for selecting save directory
    savedirs.append(save_dir)
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

#looping through folders and photos and generating new sun angle corrected photos
d = 0
#empty list for saving DLS values

import exifread 
tf = timezonefinder.TimezoneFinder()

while d < numfolds:
        
    #looping through photos and generating new sun angle corrected photos
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
            name = origfilename[-14:]
            t = gdal.Open(filename)
            numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
            
            #generating exif dictionary
            f = open(origfilename,'rb')
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

            
            time = (year, month, day, hour, minute, second)
            
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
    
            
            if not 'GPS GPSLongitude' in tags:
                latrad = 'x'
                print filename + ' has no Longitude information!'
            else:
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
                    lat1 = float(-1) * (latdeg + ((latmin + (latsec/float(60)))/float(60)))
                elif latsign == 'N':
                    lat1 = latdeg + ((latmin + (latsec/float(60)))/float(60))
                    
                latrad = math.radians(lat1)
            
            if not 'GPS GPSLongitude' in tags:
                long1 = 'x'
                print filename + ' has no Longitude information!'
            else:
                long_cent1 = str(tags['GPS GPSLongitude'])
                long_cent2 = long_cent1.split('[')
                long_cent3 = long_cent2[1]
                long_cent4 = long_cent3.split(']')
                long_cent5 = long_cent4[0]
                long_cent6 = long_cent5.split(',')
                long_cent_deg = float(long_cent6[0])
                long_cent_min = float(long_cent6[1])
                long_cent_sec1 = long_cent6[2]
                long_cent_sec2 = long_cent_sec1.split('/')
                long_cent_sec = float(long_cent_sec2[0])/ float(long_cent_sec2[1])
                long_sign = str(tags['GPS GPSLongitudeRef'])
                if long_sign == 'W':
                    long1 = float(-1) * (long_cent_deg + ((long_cent_min + (long_cent_sec/float(60)))/float(60)))
                elif long_sign == 'E' :
                    long1 = long_cent_deg + ((long_cent_min + (long_cent_sec/float(60)))/float(60))
            
            if latrad == 'x' or long1 == 'x':
                print 'Files will not be generated for ' + filename
                a = a + 1
            else:
                timezonename = str(tf.timezone_at(lng= long1,lat = lat1 ))
                utcoffset = int(pytz.timezone(timezonename).localize(datetime.datetime(year,month,day)).strftime('%z'))/100
                
                #calculating hour angle
                localhour = hour + utcoffset
                h = ((float(localhour) + (float(minute)/60) + (float(second)/60/60))-12)*15
                hrad = math.radians(h)
                        
                # Calculating sun angle in radians
                selevang = math.sin(latrad)*math.sin(sundecrad)+math.cos(latrad)*math.cos(sundecrad)*math.cos(hrad)
                
                newimage = numpyimg /selevang
                print filename + ': ' + str(selevang)
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