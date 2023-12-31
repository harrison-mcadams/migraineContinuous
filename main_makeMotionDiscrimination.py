import makeMotionDiscrimination, os, datetime, getExperimentParams, random

subjectID = 'player'
fullScreen = False
useMetropsis = True
viewingDistance = 50
randomizeTrialOrder = True
frameRate = 120

#option = 1 # jittering background of dots with stationary, smoothed target
option = 2 # gray background, with stationary, smoothed target
#option = 3 # stationary background of uniform noise dots with stationary, smoothed target

## depending on monitor, will need to figure out screen width, pixel size, etc.

trialParams = getExperimentParams.getExperimentParams('tadin2019Continuous')

trialParams.update({'contrasts': [100]})
trialParams.update({'targetRadii_degrees': [7/2]})

trialParams.update({'trialLength_s': 1})

#trialParams.update({'targetRadii_degrees': [0.75/2, 3.5]})
trialParams.update({'trialRepeats': 2})
trialParams.update({'frameRate': frameRate})

if option == 1: # jittering background of dots with stationary, smoothed target
    trialParams.update({'contrasts': [50]})
    trialParams.update({'targetRadii_degrees': [7]})
    trialParams.update({'targetOpacity': 1})
    trialParams.update({'backgroundContrast': 50})
    trialParams.update({'background': 'pixels'})
    trialParams.update({'targetMask': 'raisedCos'})
    trialParams.update({'targetMaskParams': {'fringeWidth': 0.3}})
    trialParams.update({'randomizeBackground': True})
elif option == 2: # gray background, with stationary, smoothed target
    trialParams.update({'targetOpacity': 1})
    trialParams.update({'backgroundContrast': 0})
    trialParams.update({'background': 'gray'})
    trialParams.update({'targetMask': 'raisedCos'})
    trialParams.update({'targetMaskParams': {'fringeWidth': 0.9}})
    trialParams.update({'randomizeBackground': False})
if option == 3:  # stationary background of uniform noise dots with stationary, smoothed target
    trialParams.update({'contrasts': [50]})
    trialParams.update({'targetRadii_degrees': [7]})
    trialParams.update({'targetOpacity': 1})
    trialParams.update({'backgroundContrast': 50})
    trialParams.update({'background': 'pixels'})
    trialParams.update({'targetNoiseType': 'uniform'})
    trialParams.update({'backgroundNoiseType': 'uniform'})
    trialParams.update({'targetMask': 'raisedCos'})
    trialParams.update({'targetMaskParams': {'fringeWidth': 0.3}})
    trialParams.update({'randomizeBackground': False})





if useMetropsis:
    screenNumber = 0
    screenSize = [1920, 1080]
    screenDiagonal_cm = 31.5*2.54
    screenWidth_cm = 70
    screenWidth_pixels = 1920
    backgroundSize = screenSize
else:
    screenNumber = 0
    screenSize = [1440, 900]
    screenDiagonal_cm = 13.3*2.54
    screenWidth_cm = 13.3*30
    screenWidth_pixels = 2560
    backgroundSize = screenSize
    


trialParams.update({'subjectID': subjectID})
trialParams.update({'fullScreen': fullScreen})
trialParams.update({'screenNumber': screenNumber})
trialParams.update({'viewingDistance_cm': viewingDistance})
trialParams.update({'screenSize': screenSize})
trialParams.update({'screenWidth_cm': screenWidth_cm})
trialParams.update({'screenWidth_pixels': screenWidth_pixels})
trialParams.update({'screenDiagonal_cm': screenDiagonal_cm})
trialParams.update({'backgroundSize': backgroundSize})



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

trialCounter = 1
for tt in paramsAcrossTrials:

    trialParams.update({
        'targetRadius_degrees': tt[1],
        'contrast': tt[0],
        'trialNumber': trialCounter,
        'totalTrials': len(paramsAcrossTrials)
    })

    print('Trial '+ str(trialParams['trialNumber']) + ' of ' + str(trialParams['totalTrials']) + '; Contrast: ' + str(trialParams['contrast']) + ', Size: ' + str(trialParams['targetRadius_degrees']))

    makeMotionDiscrimination.makeMotionDiscrimination(trialParams)

    trialCounter = trialCounter + 1
    print(trialCounter)