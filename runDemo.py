def runDemo(**kwargs):

    from psychopy import logging, clock, visual
    import getExperimentParams, getSubjectInfo, getWindow, getTrialList, runTrial


    if 'trialParams' in kwargs:

        trialParams = kwargs['trialParams']

    else: # No trialParams specified, so will gather everything from scratch
        trialParams = getExperimentParams.getExperimentParams('tadin2019Continuous')

        subjectID, viewingDistance_cm = getSubjectInfo.getSubjectInfo()
        trialParams.update({'subjectID': subjectID})
        trialParams.update({'viewingDistance_cm': viewingDistance_cm})



    mywin, screenSize, fullScreen, screenNumber, screenDiagonal_cm, units  = getWindow.getWindow(useFullScreen=False)
    trialParams.update({'screenSize': screenSize})
    trialParams.update({'fullScreen': fullScreen})
    trialParams.update({'screenNumber': screenNumber})
    trialParams.update({'screenDiagonal_cm': screenDiagonal_cm})
    trialParams.update({'units': units})

    contrast = float(input('Contrast: '))
    targetRadius = float(input('Target radius: '))

    continueDemo = True
    trialCounter = 1
    while continueDemo:
        trialParams.update({
            'targetRadius_degrees': targetRadius,
            'contrast': contrast,
            'trialNumber': trialCounter,
            'totalTrials': 1,
            'subjectID': 'demo',

        })


        mywin.mouseVisible = True

        runTrial.runTrial(mywin, trialParams)

        continueDemoQuestion = input('Continue demo? (y/n): ')
        if continueDemoQuestion == 'y':
            continueDemo = True
            contrast = float(input('Contrast: '))
            targetRadius = float(input('Target radius: '))
        else:
            continueDemo = False




    mywin.close()
    test = 'lame'

