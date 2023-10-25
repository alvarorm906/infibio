###SCRIPT FOR 96 WELL-PLATE MANAGING ON THE MICROSCOPE####
##
##
## activate IO library

from System.IO import File, Directory, FileInfo, Path
import os
import datetime
import time
from System import ApplicationException
from System import TimeoutException

## set variables

userPath = ('D:\Xisca\Experiments')
wgPath = ('D:\Xisca\Experiments')
XX = 'trial' # Needs to be changed at the start of a new experiment
path = r'D:\Xisca\Experiments\{}'.format(XX) 
os.mkdir(path)
userPath = (r'D:\Xisca\Experiments\{}'.format(XX))
objpos = 4 # 63x objective		############## MODIFIED
intensities = {2:60, 3:80, 4:95}
refpos = 2 # DIC_TL
listx = [i*9000+posX for i in range(0,12)] # List with positions of x
listy = [i*9000+posY for i in range(0,9)] # List with positions of y

## set functions




def runSWAF(DetailScan_reloaded,
            delay=1,
            searchStrategy='Full',
            sampling=ZenSoftwareAutofocusSampling.Fine,
            relativeRangeIsAutomatic=False,
            relativeRangeSize=80,
            timeout=0):

    # get current z-Position
    zSWAF = Zen.Devices.Focus.ActualPosition
    print('Z-Position before special SWAF :', zSWAF)

    # set SWAF parameters
    SWAF_exp.SetAutofocusParameters(searchStrategy=searchStrategy,
                                    sampling=sampling,
                                    relativeRangeIsAutomatic=relativeRangeIsAutomatic,
                                    relativeRangeSize=relativeRangeSize)
    try:
        print('Running special SWAF ...')
        zSWAF = Zen.Acquisition.FindAutofocus(SWAF_exp, timeoutSeconds=timeout)
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
    except TimeoutException as e:
        print(e.Message)

    print('Z-Position after initial SWAF : ', zSWAF)

    return zSWAF

SWAF_exp = Zen.Acquisition.Experiments.ActiveExperiment

run_findsurface = True
store_for_recall = True
hwdelay = 1
if run_findsurface:
    try:
        # initial focussing via FindSurface to assure a good starting position
        Zen.Acquisition.FindSurface()
        print('Z-Position after FindSurface: ', Zen.Devices.Focus.ActualPosition)
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
        print('FindSurface (Definite Focus) failed.')
zSWAF = runSWAF(DetailScan_reloaded,
                delay=hwdelay,
                searchStrategy='Full',
                sampling=ZenSoftwareAutofocusSampling.Coarse,
                relativeRangeIsAutomatic=False,
                relativeRangeSize=500,
                timeout=0)
if store_for_recall:
    try:
        # store current focus position inside DF to use it with RecallFocus
        Zen.Acquisition.StoreFocus()
        print('Stored Offset inside Definte Focus.')
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
        print('StoreFocus (Definite Focus) failed.')

def take_pic(): # Let's do a helper function to save code
    ## Show live image
    Zen.Acquisition.StartLive()

    ## Double autofocus
    zSWAF
    zSWAF
    ## Snap image
    image = Zen.Acquisition.AcquireImage()
    Zen.Application.Documents.Add(image)
    ## Close live image
    Zen.Acquisition.StopLive()
    ##
    ## Save the image  (in this case, "Snap-##.czi")
    Zen.Application.Save(image,r'D:\Xisca\Experiments\{}\{}_{}.czi'.format(XX, extract_labels(i,j),datetime.datetime.now()))
    
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
camerasetting1.SetParameter('Frame', '0, 0, 1920, 1216')	########### MODIFIED
## Set exposure time to 10 ms
camerasetting1.SetParameter('ExposureTime', '3.0')		########### MODIFIED
## Set binning mode to 2x2
# camerasetting1.SetParameter('BinningList', "1")
## Set gain to 4x (opt)
camerasetting1.SetParameter('AnalogGainModeList', '2')		########### MODIFIED
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
Zen.Devices.Lamp.TargetIntensity = intensities[objpos]		### Objectives: 20x, 40x and 63x -> Lamp intensity: 60, 80, 95, respectively
Zen.Devices.Lamp.Apply()
lampint = Zen.Devices.Lamp.ActualIntensity
# lampinfo = 'New Lamp intensity: ' + str(lampint) 
# Zen.Windows.Show(lampinfo)
##
#######################################################
# Get and set objective position
#######################################################
##
## Get current objective information
## Show objective information
# objname = Zen.Devices.ObjectiveChanger.ActualPositionName
# objpos = Zen.Devices.ObjectiveChanger.ActualPosition
# objmag = Zen.Devices.ObjectiveChanger.GetMagnificationByPosition(objpos)
# objinfo = 'Current name: ' + objname + '\nCurrent position: ' + str(objpos) + '\nCurrent magnification: ' + str(objmag)
# Zen.Windows.Show(objinfo)
##
##
## Set objective changer to next objective position
## Show name of current objective

Zen.Devices.ObjectiveChanger.TargetPosition = objpos
Zen.Devices.ObjectiveChanger.Apply()
objpos = Zen.Devices.ObjectiveChanger.ActualPosition
objname = Zen.Devices.ObjectiveChanger.ActualPositionName
objmag = Zen.Devices.ObjectiveChanger.GetMagnificationByPosition(objpos)
objinfo = 'New name: ' + objname + '\nNew position: ' + str(objpos) + '\nNew magnification: ' + str(objmag)
# Zen.Windows.Show(objinfo)
##
#######################################################
# Get and set reflector position
#######################################################
##
## Get current reflector information
## Show reflector information
# refname = Zen.Devices.Reflector.ActualPositionName
# refpos = Zen.Devices.Reflector.ActualPosition
# refinfo = 'Current name: ' + refname + '\nCurrent position: ' + str(refpos) 
# Zen.Windows.Show(refinfo)
##
##
## Set reflector turret to next reflector position
## Show name of current reflector

Zen.Devices.Reflector.TargetPosition = refpos
Zen.Devices.Reflector.Apply()
refname = Zen.Devices.Reflector.ActualPositionName
refpos = Zen.Devices.Reflector.ActualPosition
refinfo = 'New name: ' + refname + '\nNew position: ' + str(refpos) 
# Zen.Windows.Show(refinfo)
##
#######################################################
# Get and set stage position
#######################################################
##
## Get current stage position
## Show stage position 

posX = Zen.Devices.Stage.ActualPositionX
posY = Zen.Devices.Stage.ActualPositionY
stageinfo = 'Stage Pos X: ' + str(posX) + '\nStagePos Y: ' + str(posY) 
##Zen.Windows.Show(stageinfo)
##
##
## Set stage position
## Show new stage position 
Zen.Devices.Stage.MoveTo(15000,11720)
## an alternative to set the position
#Zen.Devices.Stage.TargetPositionX = 15000
#Zen.Devices.Stage.TargetPositionY = 11720
#Zen.Devices.Stage.Apply()
# stageinfo = 'New Stage Pos X: ' + str(Zen.Devices.Stage.ActualPositionX) + '\nNew Stage Pos Y: ' + str(Zen.Devices.Stage.ActualPositionY) 
# Zen.Windows.Show(stageinfo)
##
#######################################################
# Get and set focus position
##
## Get current focus position
## Show focus position 
focPos = Zen.Devices.Focus.ActualPosition
focusinfo = r'Focus Pos: {}'.format(focPos) 
#Zen.Windows.Show(focusinfo)
##
##
## Set focus position
## Show new focus position 
newfocPos = 5984
Zen.Devices.Focus.MoveTo(newfocPos)
## an alternative to set the position
#Zen.Devices.Focus.TargetPosition = newfocPos
#Zen.Devices.Focus.Apply()
# focusinfo = 'New Focus Pos: ' + str(Zen.Devices.Focus.ActualPosition) 
# Zen.Windows.Show(focusinfo)
##
#######################################################
## Image acquisition (v1)
# Acquire an image and save it
# Do autofocus in live image
# Loop to go through the entire plate
#######################################################
##

#for row in range(1, 9):  # Rows are numbered 1 to 8
#    for col in range(0, 12):  # Columns are numbered 1 to 12
#        well = extract_labels(row,col)  # Convert row number to letter (A-H)
#        print(r'Processing well {}'.format(well))

## Show live image
# Zen.Acquisition.StartLive()
# Zen.Acquisition.AutoExposure()
# Zen.Application.Pause("Search field of interest and focus image!")
## Do autofocus
# Zen.Acquisition.FindAutofocus()
## Snap image
# image = Zen.Acquisition.AcquireImage()
# Zen.Application.Documents.Add(image)
## Close live image
# Zen.Acquisition.StopLive()
##
## Save the image automatically with its assigned file name (in this case, "Snap-##.czi")
# Zen.Application.Save(image)
##
#######################################################
## Image acquisition (v3)
# Acquire an image and save it
# Do autofocus in live image
# Moving step by step through the entire plate
#######################################################
##

## set focus parameters

    




posX = Zen.Devices.Stage.ActualPositionX
posY = Zen.Devices.Stage.ActualPositionY
posZ = Zen.Devices.Focus.ActualPosition



Zen.Acquisition.StartLive()
Zen.Application.Pause("Search field of interest and focus image!") # Set acquisition at the beginning, before the loop

def photo_loop(minutos, fcol, frow, lcol, lrow):
    # With this loop we can set an amount of minutes for the loop to continue. 
    # Its parameters are: Minutos -> amount of minutes for the loop to continue
    # fcol -> first column with sample
    # lcol -> last column with sample
    # frow -> first row with sample
    # lrow -> las row with sample
    t_end = time.time() + 60 * minutos
    lista_x = []
    lista_y = []
    while time.time() < t_end:
        for i in range(fcol-1,lcol-1):
            for j in range(frow-1,lrow-1):
                if i or j not in lista_x or lista_y:
                    Zen.Application.Pause("Search field of interest and focus image!")
                    lista_x.append(Zen.Devices.Stage.ActualPositionX)
                    lista_y.append(Zen.Devices.Stage.ActualPositionY)
                    Zen.Devices.Stage.MoveTo(listx[i] , listy[j])
                    take_pic()



# Zen.Application.Pause("Search field of interest and focus image!")
posX = Zen.Devices.Stage.ActualPositionX
posY = Zen.Devices.Stage.ActualPositionY




stageinfo = 'Stage Pos X: ' + str(posX) + '\nStagePos Y: ' + str(posY) 



###############################################################
