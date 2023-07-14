def runContinuousTrial(trialParams):

    from psychopy import visual, core, event, logging, clock
    import numpy as np
    import random
    import datetime
    import pickle
    import os

    ### PREPARE THE TRIAL
    startTime = datetime.datetime.now()

    startTime = startTime.strftime("%H%M%S")

    ## Make window
    logging.setDefaultClock(clock.Clock())
    units = 'cm'
    #mywin = visual.Window(fullscr=trialParams['fullScreen'], monitor='testMonitor', units=units)
    mywin = visual.Window(fullscr=trialParams['fullScreen'], monitor='testMonitor', screen=trialParams['screenNumber'], units=units)

    #mywin = visual.Window([800,600], monitor='testMonitor', units=units)
    trialParams.update({'units': units})

    if 'screenWidth' in trialParams:
        screenWidth_cm = trialParams['screenWidth']
    else:
        screenWidth_cm = mywin.scrWidthCM
        trialParams['screenWidth'] = screenWidth_cm

    mywin.recordFrameIntervals = True

    ## Experiment parameters
    duration = trialParams['trialLength']
    desiredSegmentLength = trialParams['segmentLength']

    frameRate = mywin.getActualFrameRate()
    trialParams.update({'frameRate': frameRate})
    framesPerSegment = round(frameRate * desiredSegmentLength)
    actualSegmentLength = 1 / frameRate * framesPerSegment

    preTrialFrames = round(trialParams['preTrialSegmentLength']*frameRate)
    totalFrames = round(duration * frameRate)

    ## Design the visual stimuli
    # Design the main center grating

    # Make Gaussian to be applied as mask
    lengthOfMask = 1024
    gaussianFWHM_cm = (2*trialParams['viewingDistance']*np.tan(np.deg2rad(trialParams['gaussianFWHM'])))
    gaussianSigma_cm = gaussianFWHM_cm/((8*np.log(2))**0.5)
    gaussianSigma = gaussianSigma_cm*lengthOfMask/screenWidth_cm

    y = visual.filters.makeGauss(np.array(range(lengthOfMask)), mean=lengthOfMask/2, sd=gaussianSigma, gain=2.0, base=-1.0)
    mask = np.tile(y, (lengthOfMask,1))

    # Make the center grating
    stimulusHeight_cm = 2 * trialParams['viewingDistance'] * np.tan(np.deg2rad(trialParams['centerGaborSize']/2))
    stimulusFrequency_cyclesPerCM =  2 * trialParams['viewingDistance'] * np.tan(np.deg2rad(trialParams['gaborSpatialFrequency']/2))
    centerPosition = [0,0]
    grating = visual.GratingStim(win=mywin, mask=mask, units=units, size=(screenWidth_cm, stimulusHeight_cm), pos=centerPosition, sf=stimulusFrequency_cyclesPerCM, contrast=trialParams['gaborContrast']/100)
    trialParams.update({
        'stimulusHeight_cm': stimulusHeight_cm,
        'stimulsuFrequency_cyclesPerCM': stimulusFrequency_cyclesPerCM,
        'lengthOfMask': lengthOfMask,
        'centerPosition': centerPosition})

    # Make the surround gratings
    surroundHeight_cm = 2 * trialParams['viewingDistance'] * np.tan(np.deg2rad(trialParams['surroundGaborSize']/2))
    upperSurroundGrating = visual.GratingStim(win=mywin, mask=mask, units=units, size=(screenWidth_cm, surroundHeight_cm), pos=[0,surroundHeight_cm], sf=stimulusFrequency_cyclesPerCM, contrast=trialParams['gaborContrast']/100)
    lowerSurroundGrating = visual.GratingStim(win=mywin, mask=mask, units=units, size=(screenWidth_cm, surroundHeight_cm), pos=[0,-surroundHeight_cm], sf=stimulusFrequency_cyclesPerCM, contrast=trialParams['gaborContrast']/100)


    # Make the fixation point
    fixation = visual.GratingStim(win=mywin, size=0.1, pos=[0,0], sf=0, rgb=1)

    # Make the pre-trial text
    textString = 'Press Space to begin Trial '+str(trialParams['trialNumber'])+' of '+str(trialParams['totalTrials'])
    preTrialText = visual.TextStim(win=mywin, pos=[0, 2], text=textString)

    ### START THE TRIAL
    ## Pre-trial activity
    # Get initial figures on screen
    grating.draw()
    upperSurroundGrating.draw()
    lowerSurroundGrating.draw()
    fixation.draw()
    preTrialText.draw()
    mywin.update()

    ## Await space bar to start
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
                    if thisKey=='space':
                        thisResp = 1
                    elif thisKey in ['q', 'escape']:
                        core.quit()  # abort experiment
        event.clearEvents()  # clear other (eg mouse) events - they clog the buffer

    direction = 1
    flankerDirection = -1
    for ii in range(preTrialFrames):


        grating.setPhase(direction * trialParams['speed'] / frameRate, '+')  # advance phase by 0.05 of a cycle
        grating.draw()

        upperSurroundGrating.setPhase(flankerDirection * trialParams['speed'] / frameRate, '+')
        lowerSurroundGrating.setPhase(flankerDirection * trialParams['speed'] / frameRate, '+')

        upperSurroundGrating.draw()
        lowerSurroundGrating.draw()

        fixation.draw()
        mywin.flip()

    direction = -1
    flankerDirection = 1
    for ii in range(preTrialFrames):
        grating.setPhase(direction * trialParams['speed'] / frameRate, '+')  # advance phase by 0.05 of a cycle
        grating.draw()


        upperSurroundGrating.setPhase(flankerDirection * trialParams['speed'] / frameRate, '+')
        lowerSurroundGrating.setPhase(flankerDirection * trialParams['speed'] / frameRate, '+')

        upperSurroundGrating.draw()
        lowerSurroundGrating.draw()

        fixation.draw()

        mywin.flip()

    for ii in range(preTrialFrames):
        upperSurroundGrating.draw()
        lowerSurroundGrating.draw()
        grating.draw()
        fixation.draw()
        mywin.flip()

    ## Run the trial
    direction = 1
    flankerDirection = -1

    keyPresses = []
    frameTimes = []
    stimulusDirections = []
    flankerDirections = []

    #kb.clock.reset()
    mywin.frameClock.reset()

    #grating = visual.GratingStim(win=mywin, mask=mask, units=units, size=(screenWidth_cm, stimulusHeight_cm), pos=centerPosition, sf=stimulusFrequency_cyclesPerCM, contrast=trialParams['gaborContrast']/100)

    for ii in range(totalFrames):

        if (ii / framesPerSegment).is_integer():
            # Determine if we're flipping direction if we're starting a new trial
            direction = random.randint(0,1)*2 - 1
            flankerDirection  = random.randint(0,1)*2 - 1


        grating.setPhase(direction * trialParams['speed']/frameRate, '+')  # advance phase by 0.05 of a cycle
        #grating.phase = grating.phase + direction * trialParams['speed']/frameRate
        #grating.phase = direction

        upperSurroundGrating.setPhase(flankerDirection * trialParams['speed']/frameRate, '+')
        lowerSurroundGrating.setPhase(flankerDirection * trialParams['speed']/frameRate, '+')

        grating.draw(mywin)
        upperSurroundGrating.draw(mywin)
        lowerSurroundGrating.draw(mywin)

        fixation.draw(mywin)

        #preTrialText = visual.TextStim(win=mywin, pos=[0, 2], text=str(direction))
        #preTrialText.draw()

        mywin.flip()

        frameTimes.append(mywin.lastFrameT)
        stimulusDirections.append(direction)
        flankerDirections.append(flankerDirection)

        keys = event.getKeys(timeStamped=logging.defaultClock, keyList=['q', 'escape', 'left', 'right'])
        keyPresses.append(keys)
        event.clearEvents()
        for key in keys:
            if 'q' in key or 'escape' in key:
                core.quit()



    #keys = kb.getKeys()
        #keys = event.getKeys(timeStamped=mywin.frameClock)
    #keyPresses.append(keys)

    #keyPresses = filter(None, keyPresses)

    ### SAVE OUT THE DATA
    # Package up the response data
    #stimulusDirections = list(reversed(stimulusDirections))

    responseTimes = []
    responseDirections = []
    for key in keyPresses:
        if len(key) != 0:
            responseTimes.append(key[0][1])
            responseDirections.append(key[0][0])
        #if isinstance(key[0], object):
        #    print(key[0].name, key[0].rt, key[0].duration, key[0].tDown)
        #    responseTimes.append(key[0].rt)
        #    responseDirections.append(key[0].name)

    # Get directory information
    today = datetime.date.today()
    # Get today's date as a string
    today_string = today.strftime('%Y-%m-%d')

    savePath = trialParams['savePath'] + '/' + trialParams['saveFolder'] +'/data/' + trialParams['experimentLabel'] + '/' + trialParams['subjectID'] + '/' + today_string + '/'

    # Save the data variables


    data = {
        'responseTimes': responseTimes,
        'responseDirections': responseDirections,
        'stimulusTimes': frameTimes,
        'stimulusDirections': stimulusDirections,
        'surroundDirections': flankerDirections,
        'trialParams': trialParams
    }



    if not os.path.exists(savePath):
        os.makedirs(savePath)

    with open(savePath + startTime + '_SF' + str(trialParams['gaborSpatialFrequency']) + '_C' + str(trialParams['gaborContrast']) + '_raw.pkl', 'wb') as f:
        pickle.dump(data, f)
    f.close()

    # Write data to a textfile
    with open(savePath + startTime + '_SF' + str(trialParams['gaborSpatialFrequency']) + '_C' + str(trialParams['gaborContrast']) + '_responses.txt', 'w') as g:
        g.write('time (s),responseDirection\n')
        for ii in range(len(responseTimes)):
            g.write(str(responseTimes[ii]) + ',' + responseDirections[ii] + '\n')
    g.close()

    with open(savePath + startTime + '_SF' + str(trialParams['gaborSpatialFrequency']) + '_C' + str(trialParams['gaborContrast']) + '_stimuli.txt', 'w') as h:
        h.write('frameTime (s),stimulusDirection, surroundDirection\n')
        for ii in range(len(frameTimes)):
            h.write(str(frameTimes[ii]) + ',' + str(stimulusDirections[ii]) + str(flankerDirections[ii]) + '\n')
    h.close()


    print(keys)
