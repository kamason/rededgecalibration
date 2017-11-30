# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 15:59:20 2017

@author: kmason

"""
# Correct exposure compensated ortho for brightness differences between bands
import os
from osgeo import gdal, gdal_array
import numpy
import tkFileDialog
from Tkinter import *
import Tkinter
import PIL
from numpy import genfromtxt


root = Tkinter.Tk()
img_dir = str(tkFileDialog.askopenfilename(parent=root, initialdir=os.getcwd(), title='Please select the orthophoto: ' )) # generates GUI for selecting directory with images
    
#get save directory 
root = Tkinter.Tk()
save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=os.path.dirname(img_dir), title='Please select your save directory:' )) # generates GUI for selecting save directory


name = img_dir.split('/')
name = name[-1:][0][:-4]+'_corrected.tif'
t = gdal.Open(img_dir)
#seperating out each band
numpyimg1 = numpy.array(t.GetRasterBand(1).ReadAsArray())
numpyimg2 = numpy.array(t.GetRasterBand(2).ReadAsArray())
numpyimg3 = numpy.array(t.GetRasterBand(3).ReadAsArray())
numpyimg4 = numpy.array(t.GetRasterBand(4).ReadAsArray())
numpyimg5 = numpy.array(t.GetRasterBand(5).ReadAsArray())
#unnormalizing each band seperately
img1 = numpyimg1 * 1.17690998434
img2 = numpyimg2
img3 = numpyimg3 * 2.32330134871
img4 = numpyimg4 * 4.8033760412
img5 = numpyimg5 * 4.63704730693

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



            
            

