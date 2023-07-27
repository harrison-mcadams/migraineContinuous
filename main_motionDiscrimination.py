import runMotionDiscrimination, os, datetime, getExperimentParams, random

subjectID = 'debug'
fullScreen = False
useMetropsis = False
viewingDistance = 50
randomizeTrialOrder = True

#option = 1 # jittering background of dots with stationary, smoothed target
#option = 2 # gray background, with stationary, smoothed target
#option = 3 # stationary background of uniform noise dots with stationary, smoothed target
option = 4 # elementArrayMethod. random background with coherent but random target

## depending on monitor, will need to figure out screen width, pixel size, etc.

trialParams = getExperimentParams.getExperimentParams('tadin2019Continuous')

trialParams.update({'contrasts': [99]})
trialParams.update({'targetRadii_degrees': [7/2]})

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
    trialParams.update({'backgroundContrast': 50})
    trialParams.update({'backgroundMethod': 'pixels'})
    trialParams.update({'targetNoiseType': 'uniform'})
    trialParams.update({'backgroundNoiseType': 'uniform'})
    trialParams.update({'targetMask': 'raisedCos'})
    trialParams.update({'targetMaskParams': {'fringeWidth': 0.3}})
    trialParams.update({'randomizeBackground': False})
if option == 4: # elementArrayMethod. background of random pixels, with target with variable coherence
    trialParams.update({'backgroundScaleFactor': 1.25})
    trialParams.update({'targetMethod': 'ElementArrayStim'})
    trialParams.update({'proportionToPreserve': 0.5})
    trialParams.update({'targetIterations': 10})
    trialParams.update({'backgroundMethod': 'pixels'})
    trialParams.update({'backgroundRandomFactor': 99999})
    trialParams.update({'backgroundContrast': 2})
    trialParams.update({'circleFWHM_degrees': 7 / 2})
    trialParams.update({'fringeWidth': 0.9})


if useMetropsis:
    screenNumber = 1
    screenSize = [1920, 1080]
    screenDiagonal_cm = 31.5*2.54
    screenWidth_pixels = 1920
else:
    screenNumber = 0
    screenSize = [1440, 900]
    screenDiagonal_cm = 13.3*2.54
    screenWidth_pixels = 2560
    


trialParams.update({'subjectID': subjectID})
trialParams.update({'fullScreen': fullScreen})
trialParams.update({'screenNumber': screenNumber})
trialParams.update({'viewingDistance_cm': viewingDistance})
trialParams.update({'screenSize': screenSize})
trialParams.update({'screenWidth_pixels': screenWidth_pixels})
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

    runMotionDiscrimination.runMotionDiscrimination(trialParams)

    trialCounter = trialCounter + 1
    print(trialCounter)