# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 12:57:17 2017

@author: kmason
"""

#MicaSense Radiometric Calibration
#this code requires that images were taken with firmware versions prior to version 2.1.0 
#Keep images in the same directory format as they were taken in 
import exiftool 
import os
from osgeo import gdal
import numpy
import exifread
import math
import Tkinter
import tkFileDialog
import PIL
from Tkinter import *

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

filepaths = filenames(origimgdirs[0])

#determine what serial number the camera is and therefore what the vignette and radiometric cal values are. These are for two of the cameras owned by the USGS UAS office 
os.chdir(exiftoolloc)
with exiftool.ExifTool() as et:
    serial = et.get_tag('EXIF:SerialNumber',filepaths[0])

if serial == 1531006:
    k1_0 = -0.00004784429402884530
    k1_1 = -0.0000004559984711420020
    k1_2 = -0.00000000172526016620634
    k1_3 = 0.000000000005438827640296330
    k1_4 = -0.000000000000006359076010658570
    k1_5 =0.0000000000000000027055914458888100
    c1_x = 689.3951749
    c1_y = 477.1678405
    rad1 = [0.00014591400,0.00000013947900,0.00001171450]

    k2_0 = 0.00008724477927375020
    k2_1 = -0.0000016053530628013300				
    k2_2 = 0.0000000040472304989155200
    k2_3 = -0.000000000008542231047927250
    k2_4 = 0.000000000000009707908703762270
    k2_5 = -0.0000000000000000042805320361592500
    c2_x = 712.9262925
    c2_y = 455.7646062
    rad2 = [0.00012569800,0.00000009203210,0.00001581420]
    
    k3_0 = 0.00002363612626092820					
    k3_1 =-0.0000006478245058894830
    k3_2 = -0.0000000003095003811975150
    k3_3 = 0.000000000002481424129668860
    k3_4 = -0.000000000000002859027202911350
    k3_5 =0.0000000000000000009568066542263470
    c3_x =702.7437345 
    c3_y = 431.5500564
    rad3 = [0.00025870600,0.00000009278370,0.00002788740]
    
    k4_0 = 0.00018896320932567000					
    k4_1 = -0.0000032564128796881600
    k4_2 = 0.0000000112579086070368000
    k4_3 = -0.000000000023622198449941300
    k4_4 = 0.000000000000025716329906312500
    k4_5 =-0.0000000000000000110233441985026000
    c4_x = 671.5867643	
    c4_y = 449.945113
    rad4 = [0.00019302100,0.00000010185200,0.00001706930]
    
    k5_0 = -0.00004666915238069860					
    k5_1 = -0.0000003258910195939760
    k5_2 = -0.0000000007313605758376910
    k5_3 = 0.000000000001844741483216840
    k5_4 =-0.000000000000001254962598679470
    k5_5 =0.0000000000000000001554707844376210
    c5_x = 703.913993	
    c5_y = 508.2166396
    rad5 = [0.00031533500,0.00000009833990,0.00002005600]
    
elif serial == 1713086:
    k1_0 = -0.00010768884059428800				
    k1_1 = 1.453038535435910E-06	
    k1_2 = -1.065506784930780E-08
    k1_3 = 2.993053193207770E-11
    k1_4 = -3.769961030959350E-14
    k1_5 = 1.713564892713680E-17
    c1_x = 666.8525792	
    c1_y = 479.30329886002926
    rad1 = [0.0001485265647572850,0.00000011513760700956700,2.057200605650490E-05]
    
    k2_0 = 0.00001287230480691720				
    k2_1 = -4.008651682454170E-08
    k2_2 = -3.085450949637610E-09
    k2_3 = 1.154302467232390E-11
    k2_4 = -1.689265147565320E-14
    k2_5 = 8.230132315998020E-18
    c2_x =679.0137029
    c2_y =	482.8568877
    rad2 = [0.0001325676652239550,0.00000009022318867852970,4.418551081622310E-05]
    
    k3_0 = -0.00016360969139864800			
    k3_1 = 1.725668598145220E-06	
    k3_2 = -1.088244904760710E-08
    k3_3 = 2.719460120080890E-11	
    k3_4 = -3.201471848668360E-14
    k3_5 = 1.399062994156210E-17
    c3_x = 694.7178873	
    c3_y = 487.9652092
    rad3 = [0.0002535142381403440,0.00000009375849530315410,4.115940332011590E-05]
    
    k4_0 = 0.00018049936917355200					
    k4_1 = -3.420102454141070E-06
    k4_2 = 2.448789320443610E-09
    k4_3 = 1.398429159770970E-11
    k4_4 = -2.912354424954570E-14
    k4_5 = 1.586413272517840E-17
    c4_x = 659.5018134	
    c4_y = 480.678442
    rad4 = [0.0003921943710743300,0.00000013267123493480900,6.702402548182740E-05]
    
    k5_0 = -0.00004168505269309120				
    k5_1 = 3.929191621361570E-07	
    k5_2 = -9.790041268627970E-09
    k5_3 = 3.118344947758960E-11
    k5_4 =-3.952755641875870E-14
    k5_5 =1.7649669186792800E-17
    c5_x = 698.8158501	
    c5_y = 477.819949
    rad5 = [0.0003794794576877150,0.00000010775579482430700,1.416796807072190E-05]

h = 960
w = 1280
#height and width in pixels of micasense rededge image

#making numpy arrays that are the same size as the micasense images but are made up of ones
#these will become the vignette model that the raw iamges will be divided by
newimage = numpy.ones((h,w))
band1vig = numpy.ones((h,w))
band2vig = numpy.ones((h,w))
band3vig = numpy.ones((h,w))
band4vig = numpy.ones((h,w))
band5vig = numpy.ones((h,w))

#applying the polynomial equation based on the center of vignetting to the arrays of one for each band
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
    

d = 0
#for looping through folders


while d < numfolds:
    #determining the file paths for the images in the image directory provided by the user
    origimgpaths = filenames(origimgdirs[d])
    
    numimgs = len(origimgpaths)

    a = 0
    
    # extract the dark row values which is different for each image
    os.chdir(exiftoolloc)
    with exiftool.ExifTool() as et:
        darkrow = et.get_tag_batch('XMP:DarkRowValue',origimgpaths[:])
    
    #loop through images in folder "d"
    while a < numimgs:  
        #calculate the average dark value and normalize it by 2^16 (for 16 bit images)
        #might want to put a feature that checks to see what bit the image was taken in because some people take MicaSense images in 12 bit rather than 16 so you would use 2^12 instead
        dravg = numpy.mean(darkrow[a])
        pbl = dravg/65536.0
        
        filename = origimgpaths[a]
        
        #open the image as a numpy array
        name = filename[-14:]
        t = gdal.Open(filename)
        numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
        
        
        # reads exposure and ISO speed
        
        f = open(filename,'rb')
        # reading exif of image, generates a dictionary
        tags = exifread.process_file(f, details=False)
        # getting specific information from exif tags
        # checking to make sure there is a value in the exif 
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
            K = float(K)
            K = K/100.0

        if exp == 'x' or K == 'x':
            #if the exif is missing exposure or ISO value, skip that image
            a = a + 1
        else:
            #normalize pixel values by 2^16 for 16 bit and 2^12 for 12 bit
            normalpixel = numpyimg/(65536.0)
            
            #create a blank image for putting calculated radiance values into
            newimage = numpy.zeros((h,w))
            
            #determine which band and therefore which radiometric cal values to use.
            if name[-6:]=='_1.tif':
                a1 = float(rad1[0])
                a2 = float(rad1[1])
                a3 = float(rad1[2])
            elif name[-6:]=='_2.tif':
                a1 = float(rad2[0])
                a2 = float(rad2[1])
                a3 = float(rad2[2])
            elif name[-6:]=='_3.tif':
                a1 = float(rad3[0])
                a2 = float(rad3[1])
                a3 = float(rad3[2])
            elif name[-6:]=='_4.tif':
                a1 = float(rad4[0])
                a2 = float(rad4[1])
                a3 = float(rad4[2])
            elif name[-6:]=='_5.tif':
                a1 = float(rad5[0])
                a2 = float(rad5[1])
                a3 = float(rad5[2])
    
            x = 0
            y = 0
            
            while x < w:
                while y < h:
                    newimage[y,x]= (a1/K) * ((normalpixel[y,x]-pbl)/(exp+(a2*(y+1)-(a3*exp*(y+1)))))
                    y = y + 1
                y=0
                x = x + 1
            
            if name[-6:]=='_1.tif':
                newimage = newimage/ band1vig
            elif name[-6:]=='_2.tif':
                newimage = newimage / band2vig
            elif name[-6:]=='_3.tif':
                newimage = newimage / band3vig
            elif name[-6:]=='_4.tif':
                newimage = newimage / band4vig
            elif name[-6:]=='_5.tif':
                newimage = newimage / band5vig
            
            #if there is a value that is less than zero make it zero
            newimage[newimage < 0]= 0
            
            #Saving the images in the same file format as they were originally
            #checking if folder is already there and if not, the folder is generated
            #The file structure is essentially \\PATHOFSAVEDIRECTORY\\000SET\\000
            #You have to determine what number the set folder is (i.e. 000SET or 001SET or 002SET) as well as which final folder number (000, 001, 002 etc.)
            #split filename at image directory
            subdir = filename.split(origimgdirs[d]) 
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
            img = PIL.Image.fromarray(newimage, mode=None)
            img.save(name)
            a = a + 1
    d = d + 1
