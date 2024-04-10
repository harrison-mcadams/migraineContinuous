def runDemo(**kwargs):

    from psychopy import logging, clock, visual
    import getExperimentParams, getSubjectInfo, getWindow, getTrialList, runTrial
    import pyautogui


    if 'trialParams' in kwargs:

        trialParams = kwargs['trialParams']

    else: # No trialParams specified, so will gather everything from scratch
        trialParams = getExperimentParams.getExperimentParams('tadin2019Continuous')

        subjectID, viewingDistance_cm = getSubjectInfo.getSubjectInfo()
        trialParams.update({'subjectID': subjectID})
        trialParams.update({'viewingDistance_cm': viewingDistance_cm})


    # Working on mouse behavior
    # Get the screen size
    screen_width, screen_height = pyautogui.size()

    # Calculate the center coordinates
    center_x = screen_width // 2
    center_y = screen_height // 2



    mywin, screenSize, fullScreen, screenNumber, screenDiagonal_cm, units  = getWindow.getWindow()
    trialParams.update({'screenSize': screenSize})
    trialParams.update({'fullScreen': fullScreen})
    trialParams.update({'screenNumber': screenNumber})
    trialParams.update({'screenDiagonal_cm': screenDiagonal_cm})
    trialParams.update({'units': units})

    subjectID = trialParams['subjectID']

    contrast = 99
    targetRadius = 6

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

        pyautogui.moveTo(center_x, center_y)



        continueDemoQuestion = input('Continue demo? (y/n): ')


        if continueDemoQuestion == 'y':
            continueDemo = True
            contrast = float(input('Contrast (' + str(trialParams['contrasts']) + '): '))
            targetRadius = float(input('Radius (' + str(trialParams['targetRadii_degrees']) + '): '))
        else:
            continueDemo = False




    mywin.close()
    trialParams.update({'subjectID': subjectID})

