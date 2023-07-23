import analyzeContinuous_new

subjectID = 'giggity'
experimentName = 'tadin2019Continuous'
trialParams = {'subjectID': 'test4'}
trialParams.update({'experimentName': 'tadin2019Continuous'})
trialParams.update({'targetRadius_degrees': 3.5})
trialParams.update({'contrast': 99})

analyzeContinuous_new.analyzeContinuous_new(subjectID, experimentName, trialParams)
