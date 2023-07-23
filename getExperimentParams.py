def getExperimentParams(experimentName):
    
    import os, datetime
    import numpy as np

    basePath = os.path.expanduser('~') + '/Desktop/'
    projectName = 'migraineContinuous/'
    dataPath = basePath + projectName + 'data/'
    today = datetime.date.today()
    todayString = today.strftime('%Y-%m-%d')

    trialParams = {
        'viewingDistance': 50, # cm
        'experimentLabel': experimentName,
        'segmentLength': 16/1000, # s
        'trialLength': 60, # s
        'preTrialSegmentLength': 2, # s
        'basePath': basePath,
        'dataPath': dataPath,
        'projectName': projectName,
        'todayString': todayString,
        'fullScreen': True
    }

    if trialParams['experimentLabel'] == 'experiment_1a':
        trialParams.update({
            'centerGaborSize': 2, # degrees
            'surroundGaborSize': 0, # degrees
            'centerAnnulusSize': 0,
            'gaborContrasts': [8], # % Michelson contrast
            'gaborSpatialFrequencies': [1,8], # cycles/degree
            'trialRepeats': 4,
            'gaussianFWHM': 3.3, # degrees
            'speed': 3.75,
            'transitionSizeFactor': 0
        })

    if trialParams['experimentLabel'] == 'experiment_1b':
        trialParams.update({
            'centerGaborSize': 2, # degrees
            'surroundGaborSize': 0, # degrees
            'centerAnnulusSize': 0,
            'gaborContrasts': [0.5, 0.7, 1, 2, 4, 8], # % Michelson contrast
            'gaborSpatialFrequencies': [1], # cycles/degree
            'trialRepeats': 4,
            'gaussianFWHM': 3.3, # degrees
            'speed': 3.75, # Hz
            'transitionSizeFactor': 0
        })

    if trialParams['experimentLabel'] == 'experiment_2':
        trialParams.update({
            'centerGaborSize': 2, # degrees
            'surroundGaborSize': 2, # degrees
            'centerAnnulusSize': 0,
            'maskShape': 'horizontalGaussian',
            'gaborContrasts': [1, 2, 4, 8, 16], # % Michelson contrast
            'gaborSpatialFrequencies': [1,8], # cycles/degree
            'trialRepeats': 3,
            'gaussianFWHM': 0.35, # degrees
            'speed': 3.75,  # Hz
            'transitionSizeFactor': 0
        })

    if trialParams['experimentLabel'] == 'experiment_2_simplified':
        trialParams.update({
            'centerGaborSize': 2, # degrees
            'surroundGaborSize': 2, # degrees
            'centerAnnulusSize': 0,
            'maskShape': 'horizontalGaussian',
            'gaborContrasts': [16], # % Michelson contrast
            'gaborSpatialFrequencies': [1], # cycles/degree
            'trialRepeats': 3,
            'gaussianFWHM': 0.35, # degrees
            'speed': 3.75, # Hz
            'transitionSizeFactor': 0

        })

    if trialParams['experimentLabel'] == 'battista':
        trialParams.update({
            'centerGaborSize': 2,  # degrees
            'surroundGaborSize': 0,  # degrees
            'centerAnnulusSize': 4,
            'maskShape': 'circle',
            'gaborContrasts': [16],  # % Michelson contrast
            'gaborSpatialFrequencies': [1],  # cycles/degree
            'trialRepeats': 3,
            'gaussianFWHM': 0.35,  # degrees
            'speed': 3.75,  # Hz
            'transitionSizeFactor': 1.1
        })

    if experimentName == 'tadin2019Continuous':
        trialParams.update({'targetRadii_degrees': np.array([0.43, 0.75, 1.33, 2.33, 4, 7])*0.5})
        trialParams.update({'dotSize_degrees': 3 / 60})
        trialParams.update({'contrasts': [7, 99]})
        trialParams.update({'randomizeTarget': False})
        trialParams.update({'background': 'gray'})
        trialParams.update({'units': 'pix'})
        trialParams.update({'trialLength_s': 20})
        trialParams.update({'trialRepeats': 3})


    return trialParams