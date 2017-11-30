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
img_dir = str(tkFileDialog.askopenfilename(parent=root, initialdir=os.getcwd(), title='Please select the orthophoto for brightness correction' )) # generates GUI for selecting directory with images
    
#get save directory 
root = Tkinter.Tk()
save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=os.getcwd(), title='Please select your save directory' )) # generates GUI for selecting save directory



def normalize(image,minall,maxall):
    floatimg = image.astype(float)
    #converts 16bit numpy array to float
    maxval = image.max()
    minval = image.min()
    
    factor = float(maxall)/float(maxval)
    normalimg = ((floatimg - float(minval)) * factor)
    #normalizes image to between 0 and 1 and then to 16 bit range
    return normalimg

def normalize16(image,minall,maxall):
    floatimg = image.astype(float)
    #converts 16bit numpy array to float
    normalimg = ((floatimg - minall) * 65535) / (maxall-minall)
    #normalizes image to between 0 and 1 and then to 16 bit range
    newimage = normalimg.astype(numpy.uint16)
    #changes image back from float to 16bit
    return newimage



name = img_dir.split('/')
name = name[-1:][0][:-4]+'_BC_16bit.tif'
t = gdal.Open(img_dir)
#seperating out each band
numpyimg1 = numpy.array(t.GetRasterBand(1).ReadAsArray())
numpyimg2 = numpy.array(t.GetRasterBand(2).ReadAsArray())
numpyimg3 = numpy.array(t.GetRasterBand(3).ReadAsArray())
numpyimg4 = numpy.array(t.GetRasterBand(4).ReadAsArray())
numpyimg5 = numpy.array(t.GetRasterBand(5).ReadAsArray())

minDN1 = numpyimg1.min()
minDN2 = numpyimg2.min()
minDN3 = numpyimg3.min()
minDN4 = numpyimg4.min()
minDN5 = numpyimg5.min()

maxDN1 = numpyimg1.max()
maxDN2 = numpyimg2.max()
maxDN3 = numpyimg3.max()
maxDN4 = numpyimg4.max()
maxDN5 = numpyimg5.max()

maxDN = max(maxDN1, maxDN2, maxDN3, maxDN4, maxDN5)
minDN = max(minDN1, minDN2, minDN3, minDN4, minDN5)

#unnormalizing each band seperately
img1 = normalize(numpyimg1,minDN,maxDN)
img1 = normalize16(img1,minDN,maxDN)
img2 = normalize(numpyimg2,minDN,maxDN)
img2 = normalize16(img2,minDN,maxDN)
img3 = normalize(numpyimg3,minDN,maxDN)
img3 = normalize16(img3,minDN,maxDN)
img4 = normalize(numpyimg4,minDN,maxDN)
img4 = normalize16(img4,minDN,maxDN)
img5 = normalize(numpyimg5,minDN,maxDN)
img5 = normalize16(img5,minDN,maxDN)

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



            
            

