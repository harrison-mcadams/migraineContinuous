import runMotionDiscrimination, os, datetime

basePath = os.path.expanduser('~') + '/Desktop/'
projectName = 'migraineContinuous/'
dataPath = basePath+projectName+'data/'
today = datetime.date.today()
todayString = today.strftime('%Y-%m-%d')

trialParams = {'subjectID': 'test5'}
trialParams.update({'fullScreen': False})
trialParams.update({'screenNumber': 0})
trialParams.update({'viewingDistance_cm': 50})


trialParams.update({'experimentLabel': 'tadin2019Continuous'})
trialParams.update({'basePath': basePath})
trialParams.update({'projectName': projectName})
trialParams.update({'dataPath': dataPath})
trialParams.update({'todayString': todayString})


trialParams.update({'targetRadius_degrees': 5})
trialParams.update({'dotSize_degrees': 3/60})
trialParams.update({'contrast': 100})
trialParams.update({'randomizeTarget': False})
trialParams.update({'background': 'gray'})
trialParams.update({'units': 'pix'})
trialParams.update({'trialLength_s': 20})

runMotionDiscrimination.runMotionDiscrimination(trialParams)