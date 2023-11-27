from psychopy import logging, clock, visual
import getExperimentParams, getSubjectInfo, getWindow, runBlock, runDemo

trialParams = getExperimentParams.getExperimentParams('tadin2019Continuous')

subjectID, viewingDistance_cm = getSubjectInfo.getSubjectInfo()
trialParams.update({'subjectID': subjectID})
trialParams.update({'viewingDistance_cm': viewingDistance_cm})

## Run demo
runDemo.runDemo(trialParams=trialParams)

## Run first block
runBlock.runBlock(trialParams=trialParams)

## Pause between blocks
input('Press Enter when ready to begin second block:')

## Run second block
runBlock.runBlock(trialParams=trialParams)