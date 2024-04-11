from psychopy import logging, clock, visual
import getExperimentParams, getSubjectInfo, getWindow, runBlock, runDemo

trialParams = getExperimentParams.getExperimentParams('horizontalContinuous')

subjectID, viewingDistance_cm = getSubjectInfo.getSubjectInfo()
trialParams.update({'subjectID': subjectID})
trialParams.update({'viewingDistance_cm': viewingDistance_cm})

## Run demo
runDemo.runDemo(trialParams=trialParams)

## Run first block
runBlock.runBlock(trialParams=trialParams)


## Run second block
runBlock.runBlock(trialParams=trialParams)