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
    screenSize = trialParams['screenSize']
    screenDiagonal_cm = trialParams['screenDiagonal_cm']

    mywin = visual.Window(screenSize, fullscr=fullScreen, monitor='testMonitor', screen=screen,
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
    trialLength_s = trialParams['trialLength_s']
    nFrames = int(np.ceil(frameRate*trialLength_s))
    trialParams.update({'nFrames': nFrames})
    dotSize_degrees = trialParams['dotSize_degrees']
    circleRadius_degrees = trialParams['targetRadius_degrees']
    backgroundMethod = trialParams['backgroundMethod']
    randomizeTarget = trialParams['randomizeTarget']
    randomizeBackground = trialParams['randomizeBackground']
    targetNoiseType = trialParams['targetNoiseType']
    backgroundNoiseType = trialParams['backgroundNoiseType']
    targetMask = trialParams['targetMask']
    targetMaskParams = trialParams['targetMaskParams']
    backgroundScaleFactor = trialParams['backgroundScaleFactor']
    targetMethod = trialParams['targetMethod']
    targetIterations = trialParams['targetIterations']
    proportionToPreserve = trialParams['proportionToPreserve']



    ## Prepare the random walk
    walkRefreshRate = 1/60
    walkFrames = int(np.ceil(1 / walkRefreshRate * trialLength_s))+100
    arcminsPerPixel = 2.6/2
    mean = 0
    std = 4 # gives speed of 6.6 degrees per second approximately, to match what Tadin did. Note that the original continuous paper from Johannes had this at 1
    xVelocity = np.random.normal(mean, std, size=walkFrames)
    yVelocity = np.random.normal(mean, std, size=walkFrames)
    speed_pixelsPerFrame = (xVelocity**2 + yVelocity**2)**0.5
    speed_pixelsPerSecond = speed_pixelsPerFrame*frameRate
    speed_arcminPerSecond = speed_pixelsPerSecond * arcminsPerPixel
    speed_degreePerSecond = speed_arcminPerSecond /60
    print(np.mean(speed_degreePerSecond)) 

    # We will use these xPosition vectors to actually jitter the target, as well as to save out the stimulus information
    xPosition = np.cumsum(xVelocity)
    yPosition = np.cumsum(yVelocity)
    if nFrames > walkFrames:
        x = np.arange(0, walkFrames, walkFrames/nFrames)
        xp = list(range(walkFrames))
        fp = xPosition

        xPosition = np.interp(x, xp, fp)

        fp = yPosition
        yPosition = np.interp(x, xp, fp)

    xPosition = xPosition[0:nFrames]
    yPosition = yPosition[0:nFrames]


    targetPositions = []
    for ii in range(len(xPosition)):
        targetPositions.append([xPosition[ii], yPosition[ii]])



    ## Convert distances from degrees to pixels, through centimeters
    
    screenWidth_cm = screenDiagonal_cm/(((screenSize[1]**2)/(screenSize[0]**2))+1)**0.5

    #pixelCorrectionFactor = mywin.clientSize[0]/mywin.size[0]
    #pixelsPerCM = 2560/30 * pixelCorrectionFactor
    pixelsPerCM = screenSize[0]/screenWidth_cm
    
    print('PixelsPerCM: ' + str(pixelsPerCM))

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
    if backgroundMethod == 'gray':
        background = visual.NoiseStim(mywin, noiseType=backgroundNoiseType, mask='raisedCos', opacity=0, maskParams={'fringeWidth': 0.9}, size=[[circleRadius_pixels*2,circleRadius_pixels*2]], noiseElementSize=dotSize_pixels, units=units, contrast=backgroundContrast/100)
    elif backgroundMethod == 'pixels':
        background = visual.NoiseStim(mywin, noiseType=backgroundNoiseType, opacity=1, size=[screenSize[0]*backgroundScaleFactor, screenSize[1]*backgroundScaleFactor], noiseElementSize=dotSize_pixels, units=units, contrast=backgroundContrast/100)

    # Prep for background jiggle
    randomBackgroundOrigins = []
    backgroundRandomFactor = 3
    for ii in range(nFrames):

        outerBackgroundOriginX = np.floor((backgroundScaleFactor * screenSize[0] / 2) - (screenSize[0] / 2))
        outerBackgroundOriginY = np.floor((backgroundScaleFactor * screenSize[1] / 2) - (screenSize[1] / 2))

        backgroundOriginX = random.randint(-outerBackgroundOriginX, outerBackgroundOriginX)
        backgroundOriginY = random.randint(-outerBackgroundOriginY, outerBackgroundOriginY)

        if ii % backgroundRandomFactor == 0:
            randomBackgroundOrigins.append([0,0])
        else:
            randomBackgroundOrigins.append([backgroundOriginX, backgroundOriginY])


    if targetMethod == 'NoiseStim':
        target = visual.NoiseStim(mywin, noiseType=targetNoiseType, mask=targetMask, maskParams=targetMaskParams,
                              size=[[circleRadius_pixels * 2, circleRadius_pixels * 2]],
                              noiseElementSize=dotSize_pixels, units=units, contrast=contrast / 100, opacity=opacity)
    elif targetMethod == 'ElementArrayStim':

        # Manually construct a circle made up of individual dots
        def makeCircleCoordinates(circleRadius, dotSize):

            radius_inDots = int(np.ceil(circleRadius / dotSize))

            circle_xys = []
            colors = []
            for xx in range(-radius_inDots, radius_inDots + 1):
                for yy in range(-radius_inDots, radius_inDots + 1):
                    if (xx ** 2 + yy ** 2) ** 0.5 <= radius_inDots:
                        circle_xys.append([xx * dotSize, yy * dotSize])
                        color = random.randint(0, 1) * 2 - 1
                        colors.append([color, color, color])

            colors = np.array(colors)
            circle_xys = np.array(circle_xys)
            return circle_xys, colors

        # Get the xy coordinates and their colors
        circle_xys, colors = makeCircleCoordinates(circleRadius_pixels, dotSize_pixels)

        # Make the target
        target = visual.ElementArrayStim(win=mywin, units='pixels',
                                         nElements=len(circle_xys),
                                         elementTex=None,
                                         elementMask='circle',
                                         xys=circle_xys,
                                         sizes=[dotSize_pixels*1.1, dotSize_pixels*1.1],
                                         colors=colors*contrast/100,
                                         fieldPos=[0, 0]
                                         )

        ## If we're doing element array stim, we have to do a lot more background work to get it up and running

        circleIndicesToIterate = []
        nDots = len(circle_xys)
        for ii in range(targetIterations):
            indices = (random.sample(range(nDots), round(nDots * proportionToPreserve)))
            circleIndicesToIterate.append(indices)


        # Get ready to make the shuffle on each iteration
        verticesBase = target.verticesBase
        verticesPix = target.verticesPix
        sizes = target.sizes
        oris = target.oris
        opacities = target.opacities
        sfs = target.sfs
        phases = target.phases

        randomCircleIndices = []
        for ii in range(nFrames):
            randomCircleIndices.append(random.randint(0,targetIterations-1))

        target.nElements = len(circleIndicesToIterate[0])
        target.sizes = sizes[circleIndicesToIterate[0]]
        target.oris = oris[circleIndicesToIterate[0]]
        target.opacities = opacities[circleIndicesToIterate[0]]
        target.sfs = sfs[circleIndicesToIterate[0]]
        target.phases = phases[circleIndicesToIterate[0]]

        target.verticesBase = verticesBase[circleIndicesToIterate[0]]
        target.verticesPix = verticesPix[circleIndicesToIterate[0]]
        target.xys = circle_xys[circleIndicesToIterate[0]]
        target.colors = colors[circleIndicesToIterate[0]]*contrast/100



    ## Display the trial setup
    # Make the pre-trial text
    textString = 'Press Space to begin Trial '+str(trialParams['trialNumber'])+' of '+str(trialParams['totalTrials'])
    preTrialText = visual.TextStim(win=mywin, pos=[0, 200], text=textString, color='red')

    # Show the poiniter
    pointer = visual.GratingStim(win=mywin, size=3, pos=[0,0], sf=0, color='red', units=units)


    background.draw()
    target.draw()
    preTrialText.draw()
    pointer.draw()
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

    clock.wait(3)
    #mouse = event.Mouse()
    mouse = visual.CustomMouse(mywin)
    mouse.pointer = pointer

    # Prepare for trial

    frameTimes = []
    keyPresses = []
    mousePositions = []

    ## Perform trial
    for ii in range(nFrames):

        # Draw background
        background.pos = randomBackgroundOrigins[ii]
        background.draw()

        # Adjust the target
        if targetMethod == 'NoiseStim':
            target.pos = [xPosition[ii], yPosition[ii]]
            if randomizeTarget:
                target.buildNoise()
        elif targetMethod == 'ElementArrayStim':
            randomIndex = randomCircleIndices[ii]
            target.xys = circle_xys[circleIndicesToIterate[randomIndex]]
            target.colors = colors[circleIndicesToIterate[randomIndex]] * contrast / 100
            target.fieldPos = [xPosition[ii], yPosition[ii]]  # this will make the thing vertically


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
    savePath=dataPath + trialParams['experimentName'] + '/' + trialParams['subjectID'] + '/' + today_string + '/'

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

    # Print out plot of frame performance
    frameIntervals = np.diff(frameTimes*1000)
    meanInterval = np.mean(frameIntervals)
    nDroppedFrames = sum(i > 1/frameRate*1.2*1000 for i in frameIntervals)
    droppedFramesPercentage = nDroppedFrames/len(frameIntervals)*100
    droppedFramesPercentage_rounded = round(droppedFramesPercentage, 3)
    meanInterval_rounded = round(meanInterval, 3)


    plt.plot(frameIntervals)
    plt.xlabel('Frames (n)')
    plt.ylabel('Frame Interval (ms)')
    plt.title('Mean Frame Interval: '+str(meanInterval_rounded)+', '+str(droppedFramesPercentage_rounded)+'% Dropped Frames')
    plt.savefig(savePath + startTime + '_S' + str(trialParams['targetRadius_degrees']) + '_C' + str(
            trialParams['contrast'])+'_frames.png')
    plt.close()

    # For support
    print('boom')