import analyzeContinuous_new

subjectID = 'test4'
experimentName = 'tadin2019Continuous'
trialParams = {'subjectID': 'test4'}
trialParams.update({'experimentName': 'tadin2019Continuous'})
trialParams.update({'targetSize': 5})
trialParams.update({'contrast': 100})

analyzeContinuous_new.analyzeContinuous_new(subjectID, experimentName, trialParams)
