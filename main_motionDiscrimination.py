import runMotionDiscrimination, os, datetime, getExperimentParams

subjectID = 'testTest'
fullScreen = False
useMetropsis = False
viewingDistance = 50

trialParams = getExperimentParams.getExperimentParams('tardin2019Continuous')

trialParams.update({'subjectID': subjectID})
trialParams.update({'fullScreen': False})
trialParams.update({'screenNumber': 0})
trialParams.update({'viewingDistance_cm': viewingDistance})


#trialParams.update({'experimentLabel': 'tadin2019Continuous'})
#trialParams.update({'basePath': basePath})
#trialParams.update({'projectName': projectName})
#trialParams.update({'dataPath': dataPath})
#trialParams.update({'todayString': todayString})




runMotionDiscrimination.runMotionDiscrimination(trialParams)