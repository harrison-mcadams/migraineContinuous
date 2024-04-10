import runMotionDiscrimination, os, datetime, getExperimentParams, random
import numpy as np
from psychopy import logging, clock, visual

subjectID = 'carlyn_1'
fullScreen = True
useMetropsis = True
viewingDistance = 50
randomizeTrialOrder = True
targetRadii_degrees = [0.75, 1.5, 3, 6]

#option = 1 # jittering background of dots with stationary, smoothed target
#option = 2 # gray background, with stationary, smoothed target
#option = 3 # stationary background of uniform noise dots with stationary, smoothed target
#option = 4 # elementArrayMethod. random background with coherent but random target
#option = 5 # gabor over graybackground
option = 6 # horizontal motion

## depending on monitor, will need to figure out screen width, pixel size, etc.

trialParams = getExperimentParams.getExperimentParams('tadin2019Continuous')

# main params
trialParams.update({'contrasts': [2, 99]})
trialParams.update({'backgroundContrast': 50})
#trialParams.update({'targetRadii_degrees': np.array([1.33, 2.33, 4, 7, 12])*0.5}) # Tadin + 12degrees
#trialParams.update({'targetRadii_degrees': [1,2,4,8,16]}) # Tadin + 12degrees
#trialParams.update({'targetRadii_degrees': [0.75, 1.5, 3, 6, 12]}) # Tadin + 12degrees
#trialParams.update({'targetRadii_degrees': [0.625, 1.25, 2.5, 5.0, 10.0]})
#trialParams.update({'targetRadii_degrees': [6]})
trialParams.update({'targetRadii_degrees': targetRadii_degrees})







#trialParams.update({'contrasts': [99]})
#trialParams.update({'backgroundContrast': 50})
#trialParams.update({'targetRadii_degrees': np.array([12])*0.5})


#trialParams.update({'targetRadii_degrees': np.array([1, 2, 4, 8, 16])*0.5})
#trialParams.update({'targetRadii_degrees': np.array([0.75, 1.5, 3, 6, 12])*0.5})
#trialParams.update({'targetRadii_degrees': np.array([16])*0.5})
#trialParams.update({'targetRadii_degrees': np.array([0.75, 1.33, 2.33, 4, 7])*0.5}) # directly replicating Tadi
#trialParams.update({'targetRadii_degrees': [np.array(0.43)*0.5]}) # directly replicating Tadi
#trialParams.update({'targetRadii_degrees': np.array([1.33, 7])*0.5})




#trialParams.update({'targetRadii_degrees': np.array([12])*0.5})

# 1.5, 3, 6, 12 degrees diameter

if option == 1: # jittering background of dots with stationary, smoothed target
    trialParams.update({'contrasts': [50]})
    trialParams.update({'targetRadii_degrees': [7]})
    trialParams.update({'targetOpacity': 1})
    trialParams.update({'backgroundContrast': 50})
    trialParams.update({'backgroundMethod': 'pixels'})
    trialParams.update({'targetMask': 'raisedCos'})
    trialParams.update({'targetMaskParams': {'fringeWidth': 0.3}})
    trialParams.update({'randomizeBackground': True})
elif option == 2: # gray background, with stationary, smoothed target
    trialParams.update({'targetOpacity': 1})
    trialParams.update({'backgroundContrast': 0})
    trialParams.update({'backgroundMethod': 'gray'})
    trialParams.update({'targetMask': 'raisedCos'})
    trialParams.update({'targetMaskParams': {'fringeWidth': 0.9}})
    trialParams.update({'randomizeBackground': False})
if option == 3:  # stationary background of uniform noise dots with stationary, smoothed target
    trialParams.update({'targetOpacity': 1})
    trialParams.update({'backgroundContrast': 100})
    trialParams.update({'backgroundMethod': 'pixels'})
    trialParams.update({'targetNoiseType': 'uniform'})
    trialParams.update({'backgroundNoiseType': 'uniform'})
    trialParams.update({'targetMask': 'raisedCos'})
    trialParams.update({'targetMaskParams': {'fringeWidth': 0.3}})
    trialParams.update({'randomizeBackground': False})
if option == 4: # elementArrayMethod. background of random pixels, with target with variable coherence
    trialParams.update({'backgroundScaleFactor': 1.5})
    trialParams.update({'targetMethod': 'ElementArrayStim'})
    trialParams.update({'proportionToPreserve': 0.5})
    trialParams.update({'targetIterations': 5})
    trialParams.update({'backgroundMethod': 'pixels'})
    trialParams.update({'backgroundRandomFactor': 99999})
    trialParams.update({'circleFWHM_degrees': 7 / 2})
    trialParams.update({'fringeWidth': 0.9})
if option == 5:  # Gabor target, gray background
    trialParams.update({'backgroundContrast': 0})
    #trialParams.update({'targetMethod': 'GratingStim'})
    trialParams.update({'targetMethod': 'RadialStim'})
    #trialParams.update({'centerRadius_degrees': 0.1})
    trialParams.update({'centerRadius_degrees': 0})
if option == 6:  # gabor target, greybackground, horizontal motion
    trialParams.update({'backgroundContrast': 0})
    trialParams.update({'targetMethod': 'GratingStim'})
    #trialParams.update({'targetMethod': 'RadialStim'})
    trialParams.update({'centerRadius_degrees': 0.1})
    #trialParams.update({'centerRadius_degrees': 0})
    trialParams.update({'1DMotion': True})


if useMetropsis:
    screenNumber = 1
    screenSize = [1920, 1080]
    screenDiagonal_cm = 31.5*2.54
else:
    screenNumber = 0
    screenSize = [1440, 900]
    screenDiagonal_cm = 13.3*2.54
    


trialParams.update({'subjectID': subjectID})
trialParams.update({'fullScreen': fullScreen})
trialParams.update({'screenNumber': screenNumber})
trialParams.update({'viewingDistance_cm': viewingDistance})
trialParams.update({'screenSize': screenSize})
trialParams.update({'screenDiagonal_cm': screenDiagonal_cm})



nContrastLevels = len(trialParams['contrasts'])
nTargetSizes = len(trialParams['targetRadii_degrees'])
nTrialRepeats = trialParams['trialRepeats']

paramsAcrossTrials = []
for cc in range(nContrastLevels):
    for ss in range(nTargetSizes):
        for rr in range(nTrialRepeats):
            paramsAcrossTrials.append([trialParams['contrasts'][cc], trialParams['targetRadii_degrees'][ss]])

if randomizeTrialOrder:
    random.shuffle(paramsAcrossTrials)

    ## Make window
screenSize = trialParams['screenSize']
fullScreen = trialParams['fullScreen']
screen = trialParams['screenNumber']
units=trialParams['units']
logging.setDefaultClock(clock.Clock())
screenDiagonal_cm = trialParams['screenDiagonal_cm']

mywin = visual.Window(screenSize, fullscr=fullScreen, monitor='testMonitor', screen=screen,
                          units=units)

trialCounter = 1
for tt in paramsAcrossTrials:

    trialParams.update({
        'targetRadius_degrees': tt[1],
        'contrast': tt[0],
        'trialNumber': trialCounter,
        'totalTrials': len(paramsAcrossTrials),
        #'backgroundContrast': tt[0]
    })

    print('Trial '+ str(trialParams['trialNumber']) + ' of ' + str(trialParams['totalTrials']) + '; Contrast: ' + str(trialParams['contrast']) + ', Size: ' + str(trialParams['targetRadius_degrees']))

    mywin.mouseVisible = True

    runMotionDiscrimination.runMotionDiscrimination(mywin, trialParams)

    trialCounter = trialCounter + 1
    print(trialCounter)