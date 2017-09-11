# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 15:59:20 2017

@author: kmason

"""
# Convert 16 bit Unsigned Integer ortho back to original values
import os
from osgeo import gdal, gdal_array
import numpy
import tkFileDialog
from Tkinter import *
import Tkinter
import PIL
from numpy import genfromtxt


root = Tkinter.Tk()
img_dir = str(tkFileDialog.askopenfilename(parent=root, initialdir=os.getcwd(), title='Please select the orthophoto for converting from 16 bit to original values' )) # generates GUI for selecting directory with images
    
#get save directory 
root = Tkinter.Tk()
save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=os.getcwd(), title='Please select your save directory' )) # generates GUI for selecting save directory

#get info.txt file for max and min information
root = Tkinter.Tk()
info_dir = str(tkFileDialog.askopenfilename(parent=root, initialdir=img_dir, title='Please select your info.txt file generated when you converted from original to 16 bit values' )) # generates GUI for selecting save directory

def unnormalize(image,minall,maxall):
    floatimg = image.astype(float)
    #converts 16bit numpy array to float
    newimage = ((floatimg*(maxall-minall))/65535)+minall
    #normalizes image to between 0 and 1 and then to 16 bit range
    #changes image back from float to 16bit
    return newimage

table = genfromtxt(info_dir, delimiter=",", dtype=None)
maxDN = table[1].split(':')
maxDN = float(maxDN[1])
minDN = table[2].split(':')
minDN = float(minDN[1])

name = img_dir.split('/')
name = name[-1:][0][:-4]+'_non16bit.tif'
t = gdal.Open(img_dir)
#seperating out each band
numpyimg1 = numpy.array(t.GetRasterBand(1).ReadAsArray())
numpyimg2 = numpy.array(t.GetRasterBand(2).ReadAsArray())
numpyimg3 = numpy.array(t.GetRasterBand(3).ReadAsArray())
numpyimg4 = numpy.array(t.GetRasterBand(4).ReadAsArray())
numpyimg5 = numpy.array(t.GetRasterBand(5).ReadAsArray())
#unnormalizing each band seperately
img1 = unnormalize(numpyimg1,minDN,maxDN)
img2 = unnormalize(numpyimg2,minDN,maxDN)
img3 = unnormalize(numpyimg3,minDN,maxDN)
img4 = unnormalize(numpyimg4,minDN,maxDN)
img5 = unnormalize(numpyimg5,minDN,maxDN)

x_size = t.RasterXSize
y_size = t.RasterYSize
srs = t.GetProjectionRef()
geo_transform = t.GetGeoTransform()

os.chdir(save_dir)
driver = gdal.GetDriverByName("GTiff")
dataset_out = driver.Create ( name, x_size, y_size, 5, gdal.GDT_Float32 )
dataset_out.SetGeoTransform(geo_transform)
dataset_out.SetProjection(srs)
dataset_out.GetRasterBand(1).WriteArray(img1.astype(numpy.float32))
dataset_out.GetRasterBand(2).WriteArray(img2.astype(numpy.float32))
dataset_out.GetRasterBand(3).WriteArray(img3.astype(numpy.float32))
dataset_out.GetRasterBand(4).WriteArray(img4.astype(numpy.float32))
dataset_out.GetRasterBand(5).WriteArray(img5.astype(numpy.float32))
dataset_out = None

            
            

