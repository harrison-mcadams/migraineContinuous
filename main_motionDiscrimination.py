import runMotionDiscrimination, os, datetime, getExperimentParams, random

subjectID = 'giggity'
fullScreen = True
useMetropsis = False
viewingDistance = 50
randomizeTrialOrder = True


## depending on monitor, will need to figure out screen width, pixel size, etc.

trialParams = getExperimentParams.getExperimentParams('tadin2019Continuous')

#trialParams.update({'contrasts': [7]})
#trialParams.update({'targetRadii_degrees': [0.665]})


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