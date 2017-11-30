# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 08:45:18 2017

@author: kmason
"""
import os
import Tkinter
import tkFileDialog
import PIL
from Tkinter import *
import numpy
from osgeo import gdal
import math

imglist = []

band1 = 'x'
currdir = os.getcwd()
while band1 !='':
    root = Tkinter.Tk()
    band1 = str(tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a band 1 image'))
    if band1 != '':
        imglist.append(band1)
    currdir = os.path.dirname(band1)

band1 = imglist[0]
band2 = band1[:-5]+'2.tif'
band3 = band1[:-5]+'3.tif'
band4 = band1[:-5]+'4.tif'
band5 = band1[:-5]+'5.tif'

print imglist        
        
import exiftool 

os.chdir('F:\Workspace')
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
    
z = len(imglist)

u = 0

while u < z:
    band1 = imglist[u]
    band2 = band1[:-5]+'2.tif'
    band3 = band1[:-5]+'3.tif'
    band4 = band1[:-5]+'4.tif'
    band5 = band1[:-5]+'5.tif'
    
    t = gdal.Open(band1)
    numpyimg1 = numpy.array(t.GetRasterBand(1).ReadAsArray())
    t = gdal.Open(band2)
    numpyimg2 = numpy.array(t.GetRasterBand(1).ReadAsArray())
    t = gdal.Open(band3)
    numpyimg3 = numpy.array(t.GetRasterBand(1).ReadAsArray())
    t = gdal.Open(band4)
    numpyimg4 = numpy.array(t.GetRasterBand(1).ReadAsArray())
    t = gdal.Open(band5)
    numpyimg5 = numpy.array(t.GetRasterBand(1).ReadAsArray())
    
    newimage1 = numpyimg1 / band1vig
    newimage2 = numpyimg2 / band2vig
    newimage3 = numpyimg3 / band3vig
    newimage4 = numpyimg4 / band4vig
    newimage5 = numpyimg5 / band5vig
    
    name = band1[-14:]
    savedir = os.path.dirname(band1)
    os.chdir(savedir) 
    img = PIL.Image.fromarray(newimage1, mode=None)
    img.save(name[:-4]+'_vigcorr.tif')
    img = PIL.Image.fromarray(newimage2, mode=None)
    img.save(name[:-5]+'2_vigcorr.tif')
    img = PIL.Image.fromarray(newimage3, mode=None)
    img.save(name[:-5]+'3_vigcorr.tif')
    img = PIL.Image.fromarray(newimage4, mode=None)
    img.save(name[:-5]+'4_vigcorr.tif')
    img = PIL.Image.fromarray(newimage5, mode=None)
    img.save(name[:-5]+'5_vigcorr.tif')
    
    u = u + 1