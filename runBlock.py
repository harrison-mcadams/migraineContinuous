def runBlock(**kwargs):

    from psychopy import logging, clock, visual
    import getExperimentParams, getSubjectInfo, getWindow, getTrialList, runTrial


    if 'trialParams' in kwargs:

        trialParams = kwargs['trialParams']

    else: # No trialParams specified, so will gather everything from scratch
        trialParams = getExperimentParams.getExperimentParams('tadin2019Continuous')

        subjectID, viewingDistance_cm = getSubjectInfo.getSubjectInfo()
        trialParams.update({'subjectID': subjectID})
        trialParams.update({'viewingDistance_cm': viewingDistance_cm})

    paramsAcrossTrials = getTrialList.getTrialList(trialParams)


    mywin, screenSize, fullScreen, screenNumber, screenDiagonal_cm, units  = getWindow.getWindow(useFullScreen=False)
    trialParams.update({'screenSize': screenSize})
    trialParams.update({'fullScreen': fullScreen})
    trialParams.update({'screenNumber': screenNumber})
    trialParams.update({'screenDiagonal_cm': screenDiagonal_cm})
    trialParams.update({'units': units})

    trialCounter = 1
    for tt in paramsAcrossTrials:
        trialParams.update({
            'targetRadius_degrees': tt[1],
            'contrast': tt[0],
            'trialNumber': trialCounter,
            'totalTrials': len(paramsAcrossTrials),
            # 'backgroundContrast': tt[0]
        })

        print('Trial ' + str(trialParams['trialNumber']) + ' of ' + str(
            trialParams['totalTrials']) + '; Contrast: ' + str(trialParams['contrast']) + ', Radius: ' + str(
            trialParams['targetRadius_degrees']))

        mywin.mouseVisible = True

        runTrial.runTrial(mywin, trialParams)

        trialCounter = trialCounter + 1



    mywin.close()
    test = 'lame'

