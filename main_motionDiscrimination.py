import runMotionDiscrimination, os, datetime, getExperimentParams, random

subjectID = 'harry3'
fullScreen = True
useMetropsis = False
viewingDistance = 50
randomizeTrialOrder = True

#option = 1 # jittering background of dots with stationary, smoothed target
option = 2 # gray background, with stationary, smoothed target
#option = 3 # stationary background of uniform noise dots with stationary, smoothed target

## depending on monitor, will need to figure out screen width, pixel size, etc.

trialParams = getExperimentParams.getExperimentParams('tadin2019Continuous')

trialParams.update({'contrasts': [99]})
trialParams.update({'targetRadii_degrees': [0.75/2, 3.5]})

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





trialParams.update({'subjectID': subjectID})
trialParams.update({'fullScreen': fullScreen})
trialParams.update({'screenNumber': 0})
trialParams.update({'viewingDistance_cm': viewingDistance})

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

    runMotionDiscrimination.runMotionDiscrimination(trialParams)

    trialCounter = trialCounter + 1
    print(trialCounter)