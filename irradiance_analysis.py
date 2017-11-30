# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:35:15 2017

@author: kmason
"""
import exifread
import exiftool
import os

folders = ['T:\ProjectWorkspace\UAS\Missions\Training & Testing\Other Projects\CO_DFC_Training_Testing_Area\\20171003_Radiometric_Calibration_with_Dennis\UAV Data\Images\Manual_Full_Flight_ISO200_1ms\\000','T:\ProjectWorkspace\UAS\Missions\Training & Testing\Other Projects\CO_DFC_Training_Testing_Area\\20171003_Radiometric_Calibration_with_Dennis\UAV Data\Images\Manual_Full_Flight_ISO200_1ms\\001']
exiftoolloc = 'F:\Workspace'
name = 'irradiance_manual_flight2'
save_path = 'T:\ProjectWorkspace\UAS\Missions\Training & Testing\Other Projects\CO_DFC_Training_Testing_Area\\20171003_Radiometric_Calibration_with_Dennis\Calibration Calculations'
time1 = []
time2 = []
time3 = []
time4 = []
time5 = []
filepath1 = []
filepath2 =[]
filepath3 =[]
filepath4 = []
filepath5=[]

x = 0

while x < len(folders):
    for filename in os.listdir(folders[x]):
        if filename[-3:]=='tif':
            filepath = folders[x]+'/'+filename
            
            #get exif info
            f = open(filepath, 'rb')
            tags = exifread.process_file(f,details=False)
            #get time
            photodatetime = tags['EXIF DateTimeDigitized']
            photodatetime = str(photodatetime)
            photodatetime = photodatetime.split(':')
            day = photodatetime[2].split(' ')
            # hour must be in UTC time
            hour = int(day[1])
            
            minute = int(photodatetime[3])
            second = int(photodatetime[4])
                
            time = hour + (minute/float(60))+ (second/float(60)/float(60))-6.0
            
            if filepath[-5:]=='1.tif':
                filepath1.append(filepath)
                time1.append(time)
            elif filepath[-5:]=='2.tif':
                filepath2.append(filepath)
                time2.append(time)
            elif filepath[-5:]=='3.tif':
                filepath3.append(filepath)
                time3.append(time)
            elif filepath[-5:]=='4.tif':
                filepath4.append(filepath)
                time4.append(time)   
            elif filepath[-5:]=='5.tif':
                filepath5.append(filepath)
                time5.append(time)   
        
    x = x + 1
    
#get irradiance values
os.chdir(exiftoolloc)
with exiftool.ExifTool() as et:
    irradiance1 = et.get_tag_batch('XMP:SpectralIrradiance',filepath1[:])
    irradiance2 = et.get_tag_batch('XMP:SpectralIrradiance',filepath2[:])
    irradiance3 = et.get_tag_batch('XMP:SpectralIrradiance',filepath3[:])
    irradiance4 = et.get_tag_batch('XMP:SpectralIrradiance',filepath4[:])
    irradiance5 = et.get_tag_batch('XMP:SpectralIrradiance',filepath5[:])
    roll1 = et.get_tag_batch('XMP:IrradianceRoll',filepath1[:])
    pitch1 = et.get_tag_batch('XMP:IrradiancePitch',filepath1[:])
    yaw1 = et.get_tag_batch('XMP:IrradianceYaw',filepath1[:])
    roll2 = et.get_tag_batch('XMP:IrradianceRoll',filepath2[:])
    pitch2 = et.get_tag_batch('XMP:IrradiancePitch',filepath2[:])
    yaw2 = et.get_tag_batch('XMP:IrradianceYaw',filepath2[:])
    roll3 = et.get_tag_batch('XMP:IrradianceRoll',filepath3[:])
    pitch3 = et.get_tag_batch('XMP:IrradiancePitch',filepath3[:])
    yaw3 = et.get_tag_batch('XMP:IrradianceYaw',filepath3[:])
    roll4 = et.get_tag_batch('XMP:IrradianceRoll',filepath4[:])
    pitch4 = et.get_tag_batch('XMP:IrradiancePitch',filepath4[:])
    yaw4 = et.get_tag_batch('XMP:IrradianceYaw',filepath4[:])
    roll5 = et.get_tag_batch('XMP:IrradianceRoll',filepath5[:])
    pitch5 = et.get_tag_batch('XMP:IrradiancePitch',filepath5[:])
    yaw5 = et.get_tag_batch('XMP:IrradianceYaw',filepath5[:])

text = 'File Path, Time, Irradiance, Roll, Pitch, Yaw \n'

j = 0

while j < len(filepath1):
    text = text + str(filepath1[j])+','+str(time1[j])+','+str(irradiance1[j])+','+str(roll1[j])+','+str(pitch1[j])+','+str(yaw1[j])+'\n'
    j = j + 1
    
j = 0

text = text + '\n \n'

while j < len(filepath2):
    text = text + str(filepath2[j])+','+str(time2[j])+','+str(irradiance2[j])+','+str(roll2[j])+','+str(pitch2[j])+','+str(yaw2[j])+'\n'
    j = j + 1

text = text + '\n \n'

j = 0

while j < len(filepath3):
    text = text + str(filepath3[j])+','+str(time3[j])+','+str(irradiance3[j])+','+str(roll3[j])+','+str(pitch3[j])+','+str(yaw3[j])+'\n'
    j = j + 1

text = text + '\n \n'

j = 0

while j < len(filepath4):
    text = text + str(filepath4[j])+','+str(time4[j])+','+str(irradiance4[j])+','+str(roll4[j])+','+str(pitch4[j])+','+str(yaw4[j])+'\n'
    j = j + 1

text = text + '\n \n'

j = 0

while j < len(filepath5):
    text = text + str(filepath5[j])+','+str(time5[j])+','+str(irradiance5[j])+','+str(roll5[j])+','+str(pitch5[j])+','+str(yaw5[j])+'\n'
    j = j + 1
#save as .txt file

new_file = open(save_path + '/' + name + '.txt', 'w')
new_file.write(text)
new_file.close()
