import getExperimentParams, runContinuousTrial, random

## Basic setup params
experimentName = 'experiment_2_simplified'
subjectID = '500ms_C2'
segmentLength = 500/1000 # in seconds
viewingDistance = 50 # in cm
contrasts = [2]
trialRepeats = 4
debugSingleTrial = False # If false, will run through different contrasts, spatial frequencies, and repetitions
useMetropsis = False
useFullScreen = False

## Assemble the params
trialParams = getExperimentParams.getExperimentParams(experimentName)
trialParams.update({'segmentLength': segmentLength})
trialParams.update({'subjectID': subjectID})
trialParams.update({'viewingDistance': viewingDistance})
trialParams.update({'gaborContrasts': contrasts})
trialParams.update({'fullScreen': useFullScreen})
trialParams.update({'trialRepeats': trialRepeats})



if useMetropsis:
    trialParams.update({'screenNumber': 1})
else:
    trialParams.update({'screenNumber': 0})


if debugSingleTrial:
    trialParams['gaborContrasts'] = [8]
    trialParams['gaborSpatialFrequencies'] = [1]
    trialParams['trialRepeats'] = 1


randomizeTrialOrder = True

## Run the experiment
nContrastLevels = len(trialParams['gaborContrasts'])
nSpatialFrequencyLevels = len(trialParams['gaborSpatialFrequencies'])
nTrialRepeats = trialParams['trialRepeats']

paramsAcrossTrials = []
for cc in range(nContrastLevels):
    for sf in range(nSpatialFrequencyLevels):
        for rr in range(nTrialRepeats):
            paramsAcrossTrials.append([trialParams['gaborContrasts'][cc], trialParams['gaborSpatialFrequencies'][sf]])

if randomizeTrialOrder:
    random.shuffle(paramsAcrossTrials)

trialCounter = 1
for tt in paramsAcrossTrials:

    trialParams.update({
        'gaborSpatialFrequency': tt[1],
        'gaborContrast': tt[0],
        'trialNumber': trialCounter,
        'totalTrials': len(paramsAcrossTrials)
    })

    runContinuousTrial.runContinuousTrial((trialParams))
    trialCounter = trialCounter + 1

    print('test')
