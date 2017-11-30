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
# create blank list for putting number of folders in
# when I refer to folders I am talking about the folder that contains the "SET" folders

def take():
    numfold = int(e1.get())
    e1.delete(0,END)
    numfoldlist.append(numfold)
    master.destroy ()
    return
#function for saving the number of folders that the user inputs with the Tkinter GUI

# creating a Tkinter GUI for asking user for number of folders
master = Tk()
master.title("Exposure Compensation, DLS Correction and Vignetting Correction for MicaSense RedEdge Imagery")
Label(master, text="Number of folders:").grid(row=1)
e1 = Entry(master)
e1.grid(row=1, column=1)
Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=W, pady=4)
Button(master, text='Enter', command=take).grid(row=17, column=1, sticky=W, pady=4)

master.mainloop ()

#retrieving the number of folders from the list
numfolds = numfoldlist[0]

#Tkinter GUI for selecting the directory where the exiftool.exe is located
#this .exe file works with the exiftool module which is the only way that I've found to extract the irradiance and vignetting data from the exif of the images
root = Tkinter.Tk()
currdir = os.getcwd() # current working directory
exiftoolloc = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select the directory where exiftool.exe is located'))

# creating a blank list for the image directories and save directories
# there will be an image and save directory for each "folder"
imgdirs = []
savedirs = []

h = 1
#counter for looping through folders
while h <= numfolds:
    #only perform an Exposure Compensation if you camera was on automatic mode (i.e. had changing shutter speed)
    #Tkinter GUI for selecting image directory/"folder"
    root = Tkinter.Tk()
    currdir = os.getcwd() # current working directory
    img_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select your image directory for folder ' + str(h) )) # generates GUI for selecting directory with images
    imgdirs.append(img_dir)
    #Tkinter GUI for selecting save directory for that folder
    root = Tkinter.Tk()
    save_dir = str(tkFileDialog.askdirectory(parent=root, initialdir=img_dir, title='Please select your save directory for folder ' + str(h) )) # generates GUI for selecting save directory
    savedirs.append(save_dir)
    
    h = h + 1

# Tkinter GUI for selecting a band images (1-5) for extracting vignette correction values from
root = Tkinter.Tk()
currdir = imgdirs[0]
band1 = str(tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a band 1 image')) # generates GUI for selecting directory with images

band2 = band1[:-6]+'_2.tif'

band3 = band1[:-6]+'_3.tif'

band4 = band1[:-6]+'_4.tif'

band5 = band1[:-6]+'_5.tif'

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

import exiftool 

#extracting the vignetting info from band images 1 - 5
os.chdir(exiftoolloc)
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

# Extracting values for calculating correction matrix for vignetting
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

#height and width of micasense rededge images in pixels
h = 960
w = 1280

#blank image for saving new corrected images in
newimage = numpy.ones((h,w))
#creating blank images for vignette correction matrices
band1vig = numpy.ones((h,w))
band2vig = numpy.ones((h,w))
band3vig = numpy.ones((h,w))
band4vig = numpy.ones((h,w))
band5vig = numpy.ones((h,w))

#generating vignette correction matrices using equations suggested by MicaSense and values from the exif of the images

#band 1

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

#band 2
    
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

#band 3

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

#band 4

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
    
#band 5 
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
    


#looping through folders
d = 0

while d < numfolds:
    
    imgpaths = filenames(imgdirs[d])
    # generating a list of filenames for folder "d"
    
    numimgs = len(imgpaths)
    #how many images to loop through
    
    # going through each image and determining the DLS value
    os.chdir(exiftoolloc)
    with exiftool.ExifTool() as et:
        DLS = et.get_tag_batch('XMP:SpectralIrradiance',imgpaths[:])
        
    a = 0
    while a < numimgs:
        filename = imgpaths[a]
        name = filename[-14:]
        # opens each image as numpyarray
        t = gdal.Open(filename)
        numpyimg = numpy.array(t.GetRasterBand(1).ReadAsArray())
    
        # reads exposure, aperture and ISO speed
        
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
            K = int(K)
    
        # saving images in the same subdirectory format in the save directory
        if exp == 'x' or K == 'x':
            #if the exif is missing exposure or ISO value, skip that image
            a = a + 1
        else:
            #perform exposure compensation
            numpyimg = numpyimg * ((1/(exp*K)))
            
            #perform DLS compensation
            DLSnum = float(DLS[a])
            numpyimg = numpyimg * (1/DLSnum)
            
            #perform vignette correction based on what band it is
       
            if name[-6:]=='_1.tif':
                newimage = numpyimg / band1vig
            elif name[-6:]=='_2.tif':
                newimage = numpyimg / band2vig
            elif name[-6:]=='_3.tif':
                newimage = numpyimg / band3vig
            elif name[-6:]=='_4.tif':
                newimage = numpyimg / band4vig
            elif name[-6:]=='_5.tif':
                newimage = numpyimg / band5vig
            
            #split filename at image directory
            subdir = filename.split(imgdirs[d]) 
            # merging save directory for folder "d" with the SET and 000 folders for the specific image file
            savedir = savedirs[d] + subdir[1][:-15]
            subdir1 = subdir[1].split('SET')
            setdir = savedirs[d] + subdir1[0]+'SET'
            #if the path doesn't exist, make it
            if not os.path.exists(setdir):
                os.mkdir(setdir)
            if not os.path.exists(savedir):
                os.mkdir(savedir)
            #changing directory to the save directory
            os.chdir(savedir)
            # saving numpy array as TIFF
            img = PIL.Image.fromarray(newimage, mode=None)
            img.save(name)
            #loop through images
            a = a + 1
    #looping through folders
    d = d + 1
