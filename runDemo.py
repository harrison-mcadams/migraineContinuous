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

        continueDemoQuestion = ''
        while continueDemoQuestion != 'y' and continueDemoQuestion != 'n':

            continueDemoQuestion = input('Continue demo? (y/n): ')
            if continueDemoQuestion != 'y' and continueDemoQuestion != 'n':
                print('Please enter y or n')


        if continueDemoQuestion == 'y':
            continueDemo = True

            contrast = 0
            while contrast not in trialParams['contrasts']:

                contrast = input('Contrast (' + str(trialParams['contrasts']) + '): ')
                try:
                    if float(contrast) not in trialParams['contrasts']:
                        print('Please enter a valid contrast from available options')
                    contrast = float(contrast)
                except:
                    print('Please enter a valid contrast from available options')



            targetRadius = 0
            while targetRadius not in trialParams['targetRadii_degrees']:

                targetRadius = input('Radius (' + str(trialParams['targetRadii_degrees']) + '): ')

                try:

                    if float(targetRadius) not in trialParams['targetRadii_degrees']:
                        print('Please enter a valid target radius from available options')
                    targetRadius = float(targetRadius)

                except:
                    print('Please enter a valid target radius from available options')
        else:
            continueDemo = False




    mywin.close()
    trialParams.update({'subjectID': subjectID})

