def runMotionDiscrimination(trialParams):

    from psychopy import visual, core, event, logging, clock
    import numpy as np
    import random
    import datetime
    import pickle
    import os
    import matplotlib.pyplot as plt

    ## Make window
    fullScreen = trialParams['fullScreen']
    screen = trialParams['screenNumber']
    units=trialParams['units']
    logging.setDefaultClock(clock.Clock())

    mywin = visual.Window([1440, 900], fullscr=fullScreen, monitor='testMonitor', screen=screen,
                          units=units)

    #Grab some info about that window
    mywin.recordFrameIntervals = True
    frameRate = mywin.getActualFrameRate()
    trialParams.update({'frameRate': frameRate})

    ## Set up the trial parameters
    viewingDistance_cm = trialParams['viewingDistance_cm']

    # Save stuff
    dataPath = trialParams['dataPath']
    today_string = trialParams['todayString']
    startTime = datetime.datetime.now()
    startTime = startTime.strftime("%H%M%S")
    trialParams.update({'startTime': startTime})

    # Visual params
    contrast = trialParams['contrast']
    if 'backgroundContrast' in trialParams:
        backgroundContrast = trialParams['backgroundContrast']
    else:
        backgroundContrast = contrast
    opacity = trialParams['targetOpacity']
    nFrames = int(np.ceil(frameRate*20))
    trialParams.update({'nFrames': nFrames})
    dotSize_degrees = trialParams['dotSize_degrees']
    circleRadius_degrees = trialParams['targetRadius_degrees']
    background = trialParams['background']
    randomizeTarget = trialParams['randomizeTarget']
    randomizeBackground = trialParams['randomizeBackground']
    targetNoiseType = trialParams['targetNoiseType']
    backgroundNoiseType = trialParams['backgroundNoiseType']
    targetMask = trialParams['targetMask']
    targetMaskParams = trialParams['targetMaskParams']


    ## Prepare the random walk
    arcminsPerPixel = 2.6/2
    mean = 0
    std = 4 # gives speed of 6.6 degrees per second approximately, to match what Tadin did. Note that the original continuous paper from Johannes had this at 1
    xVelocity = np.random.normal(mean, std, size=nFrames)
    yVelocity = np.random.normal(mean, std, size=nFrames)
    speed_pixelsPerFrame = (xVelocity**2 + yVelocity**2)**0.5
    speed_pixelsPerSecond = speed_pixelsPerFrame*frameRate
    speed_arcminPerSecond = speed_pixelsPerSecond * arcminsPerPixel
    speed_degreePerSecond = speed_arcminPerSecond /60
    print(np.mean(speed_degreePerSecond))

    # We will use these xPosition vectors to actually jitter the target, as well as to save out the stimulus information
    xPosition = np.cumsum(xVelocity)
    yPosition = np.cumsum(yVelocity)

    targetPositions = []
    for ii in range(len(xPosition)):
        targetPositions.append([xPosition[ii], yPosition[ii]])



    ## Convert distances from degrees to pixels, through centimeters

    pixelCorrectionFactor = mywin.clientSize[0]/mywin.size[0]
    pixelsPerCM = 2560/30 * pixelCorrectionFactor

    def convertDegreesToCM(degrees, viewingDistance_cm):
        cms = 2 * viewingDistance_cm * np.tan(np.deg2rad(degrees / 2))

        return cms

    dotSize_cm = convertDegreesToCM(dotSize_degrees, viewingDistance_cm)
    circleRadius_cm = convertDegreesToCM(circleRadius_degrees, viewingDistance_cm)

    dotSize_pixels = round(dotSize_cm * pixelsPerCM)
    circleRadius_pixels = round(circleRadius_cm * pixelsPerCM)

    circleRadius_pixels = np.ceil(circleRadius_pixels/dotSize_pixels)*dotSize_pixels
    if circleRadius_pixels/dotSize_pixels % 2 != 0:
        circleRadius_pixels = circleRadius_pixels + 2



    ## Make our stimulus and background
    if background == 'gray':
        target = visual.NoiseStim(mywin, noiseType=targetNoiseType, mask=targetMask, maskParams=targetMaskParams, size=[[circleRadius_pixels*2,circleRadius_pixels*2]], noiseElementSize=dotSize_pixels, units=units, contrast=contrast/100, opacity=opacity)
        background = visual.NoiseStim(mywin, noiseType=backgroundNoiseType, mask='raisedCos', opacity=0, maskParams={'fringeWidth': 0.9}, size=[100,100], noiseElementSize=dotSize_pixels, units=units, contrast=backgroundContrast/100)
    elif background == 'pixels':
        target = visual.NoiseStim(mywin, noiseType=targetNoiseType, size=circleRadius_pixels, noiseElementSize=dotSize_pixels, units=units, mask=targetMask, maskParams=targetMaskParams, contrast=contrast/100, opacity=opacity)
        background = visual.NoiseStim(mywin, noiseType=backgroundNoiseType, opacity=1, size=[1440, 900], noiseElementSize=dotSize_pixels, units=units, contrast=backgroundContrast/100)

    ## Display the trial setup
    # Make the pre-trial text
    textString = 'Press Space to begin Trial '+str(trialParams['trialNumber'])+' of '+str(trialParams['totalTrials'])
    preTrialText = visual.TextStim(win=mywin, pos=[0, 4], text=textString)

    background.draw()
    target.draw()
    preTrialText.draw()
    mywin.flip()

    ## Await space bar to start
    thisResp = None
    while thisResp == None:
        allKeys = event.waitKeys()
        for thisKey in allKeys:
            if thisKey == 'space':
                thisResp = 1
            elif thisKey in ['q', 'escape']:
                core.quit()  # abort experiment
        event.clearEvents()  # clear other (eg mouse) events - they clog the buffer

    # Prepare for trial
    #mouse = event.Mouse()
    mouse = visual.CustomMouse(mywin)
    pointer = visual.GratingStim(win=mywin, size=3, pos=[0,0], sf=0, color='red', units=units)
    mouse.pointer = pointer

    frameTimes = []
    keyPresses = []
    mousePositions = []

    ## Perform trial
    for ii in range(nFrames):

        # Draw background
        if randomizeBackground:
            background.buildNoise()
        background.draw()

        # Adjust the target
        target.pos = [xPosition[ii], yPosition[ii]]
        if randomizeTarget:
            target.buildNoise()
        target.draw()

        # Update the mouse pointer
        mouse.draw()

        # Update the frame
        mywin.flip()

        # Save out timing and mouse position
        frameTimes.append(mywin.lastFrameT)
        mousePosition = mouse.getPos()
        mousePositions.append([mousePosition[0], mousePosition[1]])

        # Listen for quit
        keys = event.getKeys(timeStamped=logging.defaultClock, keyList=['q', 'escape'])
        keyPresses.append(keys)
        event.clearEvents()
        for key in keys:
            if 'q' in key or 'escape' in key:
                core.quit()

    ## Package up the data to save out
    # Set the timebase relative to trial start
    frameTimes = np.array(frameTimes) - frameTimes[0]

    # Get velocities
    targetXVelocities = []
    targetYVelocities = []
    mouseXVelocities = []
    mouseYVelocities = []
    for ii in range(nFrames-1):
        targetXVelocities.append((xPosition[ii+1]-xPosition[ii])/(frameTimes[ii+1]-frameTimes[ii]))
        targetYVelocities.append((yPosition[ii+1]-yPosition[ii])/(frameTimes[ii+1]-frameTimes[ii]))

        mouseXVelocities.append((np.array(mousePositions)[ii+1,0] - np.array(mousePositions)[ii,0])/(frameTimes[ii+1]-frameTimes[ii]))
        mouseYVelocities.append((np.array(mousePositions)[ii+1,1]- np.array(mousePositions)[ii,1])/(frameTimes[ii+1]-frameTimes[ii]))


    # Package up the main output variable
    data = {
        'mouseXs': np.array(mousePositions)[:,0],
        'mouseXVelocities': mouseXVelocities,
        'mouseYs':np.array(mousePositions)[:,1],
        'mouseYVelocities': mouseYVelocities,
        'targetXs': xPosition,
        'targetXVelocities': targetXVelocities,
        'targetYs': yPosition,
        'targetYVelocities': targetYVelocities,
        'frameTimes': frameTimes,
        'trialParams': trialParams
    }

    # Define path
    savePath=dataPath + trialParams['experimentLabel'] + '/' + trialParams['subjectID'] + '/' + today_string + '/'

    # Make the output folder
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    # Save variable
    with open(savePath + startTime + '_S' + str(trialParams['targetRadius_degrees']) + '_C' + str(trialParams['contrast']) + '_raw.pkl', 'wb') as f:
        pickle.dump(data, f)
    f.close()

    # Write out text file of the results
    with open(savePath + startTime + '_S' + str(trialParams['targetRadius_degrees']) + '_C' + str(
            trialParams['contrast']) + '.txt', 'w') as g:
        g.write('time (s),targetX,targetY,mouseX,mouseY\n')
        for ii in range(len(frameTimes)):
            g.write(str(frameTimes[ii]) + ',' + str(targetPositions[ii][0]) +',' + str(targetPositions[ii][1]) + ',' + str(mousePositions[ii][0]) + ',' + str(mousePositions[ii][1]) + '\n')
    g.close()

    # For support
    print('boom')