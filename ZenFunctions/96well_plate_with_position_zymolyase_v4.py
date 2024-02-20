###SCRIPT FOR 96 WELL-PLATE MANAGING ON THE MICROSCOPE####
##

# Focus all the capture points, change the range of autofocus to 30 um (minimum)

from System.IO import File, Directory, FileInfo, Path
import os
import datetime
import time
import sys
from System import ApplicationException
from System import TimeoutException
import string
import random

## set variables to be changed:
XX = 'Exp_Zymolyase_C100_50_T35_ConA03-20240219' # Needs to be changed at the start of a new experiment
refpos = 2 # DIC_TL
objpos = 4 # 63x objective  
pocillos = 7 # number of pocillos with sample (change at the start of a new experiment)
minutos = 120 # number of minutes to run the experiment (change at the start of a new experiment)
wells = ['F6','F7','F8','F9','F10','F11','F12'] #wells filled with sample
zymo = '100-50' # Set the concentration of zymolyase in ug/mL
temp = '35' # Set the temperature of the experiment in ºC
temp_str = str(temp)
zymo_str = str(zymo)

## fixed variables: 
userPath = ('D:\Xisca\Experiments')
wgPath = ('D:\Xisca\Experiments')
path = r'D:\Xisca\Experiments\{}'.format(XX) 
os.mkdir(path)
intensities = {2:60, 3:80, 4:95}

#######################################################
# Get and set stage position (initial pos)
#######################################################
Zen.Devices.Focus.MoveTo(8750.000)
Zen.Devices.Stage.MoveTo(15639.000,11570.000) # (position of A1)
well_names = [r'{}{}'.format(chr(65 + i // 12),i % 12 + 1) for i in range(96)]
posX = Zen.Devices.Stage.ActualPositionX
posY = Zen.Devices.Stage.ActualPositionY
listx = [i*9000+posX for i in range(0,12)]  # List with positions of x
listy = [i*9000+posY for i in range(0,8)]   # List with positions of y
well_positions = {well_name: [listx[i % 12], listy[i // 12]] for i, well_name in enumerate(well_names)} # Dictionary with well positions and the xy positions
zpos = []


def photo_loop_pos(minutos, well_name):
    t_end = time.time() + 60 * minutos
    start_time = time.time()
    pos = 0
    listax = {}
    listay = {}
    listaz = {}

    def photo():
        try:
            Zen.Acquisition.FindAutofocus()
            zpos.append(Zen.Devices.Focus.ActualPosition)
            image = Zen.Acquisition.AcquireImage()
            Zen.Application.Documents.Add(image)
            current_time = int(time.time() - start_time)
            current_time_str = str(current_time).zfill(4)
            well_image_count = image_counts[well_name_entry]  # Get the image count for the well
            image_name = "{}.{}_{}_{}_{}".format(well_name_entry, well_image_count, zymo_str, temp_str, current_time_str)
            image_counts[well_name_entry] += 1  # Increment the image count
            Zen.Application.Save(image, r'{}\{}\{}.czi'.format(userPath, XX, image_name))
            Zen.Application.Documents.RemoveAll()
        except Exception as e:
            print(r"Error in taking a photo: {}".format(str(e)))

    while time.time() < t_end or pos < pocillos:
        image_counts = {well_name_entry: 0 for well_name_entry in well_name}
        
        for well, well_name_entry in enumerate(wells):  # Iterate with index and value
            try:
                Zen.Devices.Stage.MoveTo(listax[well_name_entry+str(.0)], listay[well_name_entry+str(.0)])
                Zen.Devices.Focus.MoveTo(listaz[well_name_entry+str(.0)])
                photo()
                Zen.Devices.Stage.MoveTo(listax[well_name_entry+str(.1)], listay[well_name_entry+str(.1)])
                Zen.Devices.Focus.MoveTo(listaz[well_name_entry+str(.1)])
                photo()
                Zen.Devices.Stage.MoveTo(listax[well_name_entry+str(.2)], listay[well_name_entry+str(.2)])
                Zen.Devices.Focus.MoveTo(listaz[well_name_entry+str(.2)])
                photo()
                Zen.Devices.Stage.MoveTo(listax[well_name_entry+str(.3)], listay[well_name_entry+str(.3)])
                Zen.Devices.Focus.MoveTo(listaz[well_name_entry+str(.3)])
                photo()
            except:
                Zen.Devices.Stage.MoveTo(well_positions[well_name_entry][0], well_positions[well_name_entry][1])
                Zen.Application.Pause("Adjust focus")
                listax[well_name_entry+str(.0)] = Zen.Devices.Stage.ActualPositionX 
                listay[well_name_entry+str(.0)] = Zen.Devices.Stage.ActualPositionY
                listaz[well_name_entry+str(.0)] = Zen.Devices.Focus.ActualPosition
                photo()
                # Moved to a specific position
                Zen.Devices.Stage.MoveTo(well_positions[well_name_entry][0] + random.randint(-100, 100), well_positions[well_name_entry][1] + random.randint(-100, 100))
                Zen.Application.Pause("Adjust focus")
                listax[well_name_entry+str(.1)] = Zen.Devices.Stage.ActualPositionX 
                listay[well_name_entry+str(.1)] = Zen.Devices.Stage.ActualPositionY
                listaz[well_name_entry+str(.1)] = Zen.Devices.Focus.ActualPosition
                photo()
                Zen.Devices.Stage.MoveTo(well_positions[well_name_entry][0]+ random.randint(-100, 100), well_positions[well_name_entry][1] + random.randint(-100, 100))
                Zen.Application.Pause("Adjust focus")
                listax[well_name_entry+str(.2)] = Zen.Devices.Stage.ActualPositionX 
                listay[well_name_entry+str(.2)] = Zen.Devices.Stage.ActualPositionY
                listaz[well_name_entry+str(.2)] = Zen.Devices.Focus.ActualPosition
                photo()
                Zen.Devices.Stage.MoveTo(well_positions[well_name_entry][0] + random.randint(-100, 100), well_positions[well_name_entry][1] + random.randint(-100, 100))
                Zen.Application.Pause("Adjust focus")
                listax[well_name_entry+str(.3)] = Zen.Devices.Stage.ActualPositionX 
                listay[well_name_entry+str(.3)] = Zen.Devices.Stage.ActualPositionY
                listaz[well_name_entry+str(.3)] = Zen.Devices.Focus.ActualPosition
                photo()
                pos = well + 1


#######################################################
## Create a camera setting
#######################################################
##
## Remove all open images
## Define experiment
exp = Zen.Acquisition.Experiments.GetByName('Xisca_setup.czexp')
img = Zen.Acquisition.Execute(exp)
#fullPath = path + '\\' + immg.Name
#image.Save(fullPath)
## Set camera parameters to default
#Zen.Acquisition.ActiveCamera.SetDefaultSetting()
## Apply camera setting
#Zen.Acquisition.ActiveCamera.ApplyCameraSetting(camerasetting1)

#######################################################
## Microscope settings
# Get and set lamp intensity
#######################################################
## Get current lamp intensity and lamp mode
## Show current lamp intensity 
lampint = Zen.Devices.Lamp.ActualIntensity
lampmode = Zen.Devices.Lamp.ActualMode
Zen.Devices.Lamp.TargetMode = ZenLampMode.Set3200K
Zen.Devices.Lamp.Apply()

## Set new lamp intensity
## Show new current lamp intensity 
Zen.Devices.Lamp.TargetIntensity = intensities[objpos] #Objectives: 20x, 40x and 63x -> Lamp intensity: 60, 80, 95, respectively
Zen.Devices.Lamp.Apply()
lampint = Zen.Devices.Lamp.ActualIntensity

#######################################################
# Get and set objective position
#######################################################

Zen.Devices.ObjectiveChanger.TargetPosition = objpos
Zen.Devices.ObjectiveChanger.Apply()

#######################################################
# Get and set reflector position
#######################################################

Zen.Devices.Reflector.TargetPosition = refpos
Zen.Devices.Reflector.Apply()


#######################################################
# Introduce parameters and start the loop
#######################################################
Zen.Application.Pause("Check camera, auto-save, autofocus and stage settings!")
Zen.Application.Pause("Software Autofocus: Mode - Auto, Quality - Low Signal, Search - Smart, Sampling - Fine, Relative Range - Range of 20 microns")
Zen.Application.Pause("Stage: Speed - 20%, Acceleration - 5%")
Zen.Application.Pause("Camera: Exposure time - 30 ms, Acquisition ROI - 1920 x 1216, Gain - 4x")
Zen.Application.Pause("Acquisition - Auto Save - Close CZI Image After Acquisition")
Zen.Acquisition.StartLive()

# Run the photo_loop_pos function
photo_loop_pos(minutos, wells)

# Run the photo_loop_pos function
photo_loop_pos(minutos, wells)
print(zpos)
import csv
with open(path+'\z_pos.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(zpos)