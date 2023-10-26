###SCRIPT FOR 96 WELL-PLATE MANAGING ON THE MICROSCOPE####
##
##
## activate IO library

from System.IO import File, Directory, FileInfo, Path
import os
import datetime
import time
import sys
from System import ApplicationException
from System import TimeoutException

## set variables to be changed:
XX = 'trial2' # Needs to be changed at the start of a new experiment
refpos = 2 # DIC_TL
objpos = 4 # 63x objective  
pocillos = 0 # number of pocillos with sample
minutos = 0 # number of minutes to run the experiment
well_name = ['01','02','03'] #wells filled with sample

## fixed variables: 
userPath = ('D:\Xisca\Experiments')
wgPath = ('D:\Xisca\Experiments')
path = r'D:\Xisca\Experiments\{}'.format(XX) 
os.mkdir(path)
intensities = {2:60, 3:80, 4:95}
#listx = [i*9000+posX for i in range(0,12)] # List with positions of x
#listy = [i*9000+posY for i in range(0,8)] # List with positions of y

## set functions

##### Generar un pop up en loop que nos permita introducir las posiciones manualmente
#a={'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8}   # Introducir letra correspondiente a la fila [A-H]
#b={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}   # Introducir numero de columna
#welln = [a*9000,b*9000]
###############################################################################################################

#def runSWAF(SWAF_exp,
#            delay=1,
 #           searchStrategy='Full',
 #           sampling=ZenSoftwareAutofocusSampling.Fine,
#            relativeRangeIsAutomatic=False,
 #           relativeRangeSize=80,
 #           timeout=0):
#
 #   # get current z-Position
 #   zSWAF = Zen.Devices.Focus.ActualPosition
 #   print('Z-Position before special SWAF :', zSWAF)

 #   # set SWAF parameters
 #   SWAF_exp.SetAutofocusParameters(searchStrategy=searchStrategy,
 #                                   sampling=sampling,
 #                                   relativeRangeIsAutomatic=relativeRangeIsAutomatic,
 #                                   relativeRangeSize=relativeRangeSize)
 #   try:
 #       print('Running special SWAF ...')
 #       zSWAF = Zen.Acquisition.FindAutofocus(SWAF_exp, timeoutSeconds=timeout)
 #   except ApplicationException as e:
 #       print('Application Exception : ', e.Message)
 #   except TimeoutException as e:
 #       print(e.Message)

  #  print('Z-Position after initial SWAF : ', zSWAF)

  #  return zSWAF

#SWAF_exp = Zen.Acquisition.Experiments.ActiveExperiment

run_findsurface = True
store_for_recall = True
hwdelay = 1
#if run_findsurface:
 #   try:
 #       # initial focussing via FindSurface to assure a good starting position
 #       Zen.Acquisition.FindSurface()
 #       print('Z-Position after FindSurface: ', Zen.Devices.Focus.ActualPosition)
 #   except ApplicationException as e:
 #       print('Application Exception : ', e.Message)
 #       print('FindSurface (Definite Focus) failed.')
#zSWAF = runSWAF(SWAF_exp,
 #               delay=hwdelay,
 #               searchStrategy='Full',
 #               sampling=ZenSoftwareAutofocusSampling.Coarse,
 #               relativeRangeIsAutomatic=False,
 #               relativeRangeSize=80,
 #               timeout=0)
#if store_for_recall:
 #   try:
 #       # store current focus position inside DF to use it with RecallFocus
 #       Zen.Acquisition.StoreFocus()
 #       print('Stored Offset inside Definte Focus.')
 #   except ApplicationException as e:
 #       print('Application Exception : ', e.Message)
 #       print('StoreFocus (Definite Focus) failed.')

def take_pic(): # Let's do a helper function to save code
    ## Snap image
    image = Zen.Acquisition.AcquireImage()
    Zen.Application.Documents.Add(image)
    ## Save the image  (in this case, "Snap-##.czi")
    # PositionInfo = '{:02d,:02d}'.format(lista_x[i], lista_y[i])
    # TimeInfo = '{:04d}'.format(time.time())
    # MyImage = PositionInfo + '_' + TimeInfo
    #Zen.Application.Save(image,r'D:\Xisca\Experiments\{}\{}.czi'.format(XX,datetime.datetime.now()))
    
def extract_labels(nr, nc):    
    """
    Define helper function to be able to extract the well labels depending
    on the actual wellplate type. Currently supports 96, 384 and 1536 well plates.

    :param nr: number of rows of the wellplate, e.g. 8 (A-H) for a 96 wellplate
    :param nc: number of columns of the wellplate, e.g. 12 (1-12) for a 96 wellplate
    :return: lx, ly are list containing the actual row and columns IDs
    """

    # labeling schemes
    labelX = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
              '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
              '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36',
              '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', ]

    labelY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
              'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF']

    lx = labelX[nc]
    ly = labelY[nr]

    return str(lx, ly)


def photo_loop(minutos, pocillos):
    # With this loop we can set an amount of minutes for the loop to continue. 
    # Its parameters are: Minutos -> amount of minutes for the loop to continue
    # pocillos -> number of pocillos with sample
    t_end = time.time() + 60 * minutos
    start_time=time.time()
    pos = 0
    lista_x = []
    lista_y = []
    lista_z = []
    while time.time() < t_end or pos < pocillos:
        for i in range(pocillos):
            try:
                Zen.Devices.Stage.MoveTo(lista_x[i] , lista_y[i])
                Zen.Devices.Focus.MoveTo(lista_z[i])
                pos = i+1
                Zen.Acquisition.FindAutofocus()
                Zen.Acquisition.FindAutofocus()
                image = Zen.Acquisition.AcquireImage()
                Zen.Application.Documents.Add(image)
                current_time = int(time.time() - start_time)
                current_time_str = str(current_time).zfill(4)
                image_name = "{}_{}.czi".format(well_name[i], current_time_str)
                Zen.Application.Save(image, r'{}\{}\{}.czi'.format(userPath, XX, image_name))
                
            except:
                Zen.Application.Pause("Search field of interest and focus image!")
                lista_x.append(Zen.Devices.Stage.ActualPositionX)
                lista_y.append(Zen.Devices.Stage.ActualPositionY)
                lista_z.append(Zen.Devices.Focus.ActualPosition)
                image = Zen.Acquisition.AcquireImage()
                Zen.Application.Documents.Add(image)
                current_time = int(time.time() - start_time)
                current_time_str = str(current_time).zfill(4)
                image_name = "{}_{}.czi".format(well_name[i], current_time_str)
                Zen.Application.Save(image, r'{}\{}\{}.czi'.format(userPath, XX, image_name))



## 
#######################################################
# Create a camera setting
#######################################################
##
## Remove all open images

Zen.Application.Documents.RemoveAll()
##
## Create new camera settings
camerasetting1 = ZenCameraSetting()
## Set camera frame to 1920 x 1216 and center
camerasetting1.SetParameter('Frame', '0, 0, 1920, 1216')
## Set exposure time to 3 ms
camerasetting1.SetParameter('ExposureTime', '3.0')
## Set binning mode to 2x2
# camerasetting1.SetParameter('BinningList', "1")
## Set gain to 4x (opt)
camerasetting1.SetParameter('AnalogGainModeList', '2')
## Save the setting
camerasetting1.SaveAs("MyCameraSetting.czcs", ZenSettingDirectory.Workgroup)


## Set camera parameters to default
Zen.Acquisition.ActiveCamera.SetDefaultSetting()
## Apply camera setting
Zen.Acquisition.ActiveCamera.ApplyCameraSetting(camerasetting1)
## Snap image
# image = Zen.Acquisition.AcquireImage()
# Zen.Application.Documents.Add(image)
## Set camera parameters back to default
Zen.Acquisition.ActiveCamera.SetDefaultSetting()
##
#######################################################
## Microscope settings
# Get and set lamp intensity
#######################################################
##
## Get current lamp intensity and lamp mode
## Show current lamp intensity 
lampint = Zen.Devices.Lamp.ActualIntensity
lampmode = Zen.Devices.Lamp.ActualMode
# lampinfo = 'Lamp intensity: ' + str(lampint) + '\rLamp mode: ' + str(lampmode)
# Zen.Windows.Show(lampinfo)
##
## Set new lamp mode
## Show new lamp mode
Zen.Devices.Lamp.TargetMode = ZenLampMode.Set3200K
Zen.Devices.Lamp.Apply()
# lampmode = Zen.Devices.Lamp.ActualMode
# Zen.Windows.Show(lampmode)
##
## Set new lamp intensity
## Show new current lamp intensity 
Zen.Devices.Lamp.TargetIntensity = intensities[objpos]      ### Objectives: 20x, 40x and 63x -> Lamp intensity: 60, 80, 95, respectively
Zen.Devices.Lamp.Apply()
lampint = Zen.Devices.Lamp.ActualIntensity
# lampinfo = 'New Lamp intensity: ' + str(lampint) 
# Zen.Windows.Show(lampinfo)
##
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
# Get and set stage position (initial pos)
#######################################################
Zen.Devices.Stage.MoveTo(15000,11720) # (e.g. 1st well)
# Focus the image z-position (manually)

#######################################################
## Change speed and acceleration of stage
#######################################################
#hwset = ZenHardwareSetting()
#hwset.Load('MyStage',ZenSettingDirectory.Workgroup)
# Enter the value in percentage (min 1, max 100).
# Stage control is updated, after hardware setting is applied.
# hwset.SetParameter('MTBStageAxisX','ContinualSpeed',50) # Number in percentage
# hwset.SetParameter('MTBStageAxisY','ContinualSpeed',50) # Number in percentage
# hwset.SetParameter('MTBStageAxisX','Acceleration',10) ## NO IDEA IF IT IS CORRECT
# hwset.SetParameter('MTBStageAxisY','Acceleration',10) ## NO IDEA IF IT IS CORRECT
#Zen.Devices.ApplyHardwareSetting(hwset)
##

#######################################################
# Define photo function and start the loop
#######################################################
Zen.Application.Pause("hallo!")
Zen.Acquisition.StartLive()





photo_loop(minutos, pocillos)
