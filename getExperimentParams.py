def getExperimentParams(experimentName):
    
    import os, datetime
    import numpy as np

    basePath = os.path.expanduser('~') + '/Desktop/'
    projectName = 'surroundSuppressionPTHA/'
    dataPath = basePath + projectName + 'data/'
    analysisPath = basePath + projectName + 'analysis/'

    today = datetime.date.today()
    todayString = today.strftime('%Y-%m-%d')

    trialParams = {
        'experimentName': experimentName,
        'basePath': basePath,
        'dataPath': dataPath,
        'analysisPath': analysisPath,
        'projectName': projectName,
        'todayString': todayString,
    }

    if experimentName == 'horizontalContinuous':

        trialParams.update({'units': 'pix'})
        trialParams.update({'trialLength_s': 20})
        trialParams.update({'trialRepeats': 3})
        trialParams.update({'centerRadius_degrees': 0.1})
        trialParams.update({'targetRadii_degrees': [0.75, 1.5, 3, 6]})
        trialParams.update({'contrasts': [2, 99]})
        trialParams.update({'sf_cyclesPerDegree': 1})
        trialParams.update({'targetSpeed_degreesPerSecond': 8})


    return trialParams