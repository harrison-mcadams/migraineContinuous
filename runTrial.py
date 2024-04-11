def runTrial(mywin, trialParams):

    from psychopy import visual, core, event, clock, logging
    import numpy as np
    import random
    import datetime
    import pickle
    import os
    import copy
    import matplotlib.pyplot as plt

    #Grab some info about the window
    screenSize = trialParams['screenSize']
    fullScreen = trialParams['fullScreen']
    screen = trialParams['screenNumber']
    units=trialParams['units']
    logging.setDefaultClock(clock.Clock())
    screenDiagonal_cm = trialParams['screenDiagonal_cm']
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
    trialLength_s = trialParams['trialLength_s']
    nFrames = int(np.ceil(frameRate*trialLength_s))
    trialParams.update({'nFrames': nFrames})
    circleRadius_degrees = trialParams['targetRadius_degrees']
    centerRadius_degrees = trialParams['centerRadius_degrees']
    sf_cyclesPerDegree = trialParams['sf_cyclesPerDegree']
    targetSpeed_degreesPerSecond = trialParams['targetSpeed_degreesPerSecond']

    ## Convert distances from degrees to pixels, through centimeters

    screenWidth_cm = screenDiagonal_cm / (((screenSize[1] ** 2) / (screenSize[0] ** 2)) + 1) ** 0.5
    pixelsPerCM = screenSize[0] / screenWidth_cm

    def convertDegreesToCM(degrees, viewingDistance_cm):
        cms = 2 * viewingDistance_cm * np.tan(np.deg2rad(degrees / 2))

        return cms

    circleRadius_cm = convertDegreesToCM(circleRadius_degrees, viewingDistance_cm)
    centerRadius_cm = convertDegreesToCM(centerRadius_degrees, viewingDistance_cm)

    circleRadius_pixels = round(circleRadius_cm * pixelsPerCM)
    centerRadius_pixels = round(centerRadius_cm * pixelsPerCM)

    CMsPerDegree = convertDegreesToCM(1, viewingDistance_cm)
    pixelsPerDegree = pixelsPerCM * CMsPerDegree
    degreesPerPixel = 1/pixelsPerDegree
    arcminsPerPixel = degreesPerPixel*60
    sf_cyclesPerCM = sf_cyclesPerDegree / CMsPerDegree
    sf_cyclesPerPixel = sf_cyclesPerCM / pixelsPerCM

    ## Prepare the random walk
    walkRefreshRate = 1/60
    walkFrames = int(np.ceil(1 / walkRefreshRate * trialLength_s))+100
    #arcminsPerPixel = 2.6/2
    mean = 0
    std = (targetSpeed_degreesPerSecond*pixelsPerDegree*walkRefreshRate)/((2/np.pi)**0.5) #3.85 # gives speed of 4 degrees per second approximately
    xVelocity = np.random.normal(mean, std, size=walkFrames)
    speed_pixelsPerFrame = (xVelocity**2)**0.5
    speed_pixelsPerSecond = speed_pixelsPerFrame*1/walkRefreshRate
    speed_arcminPerSecond = speed_pixelsPerSecond * arcminsPerPixel
    speed_degreePerSecond = speed_arcminPerSecond /60
   # print(np.mean(speed_degreePerSecond))

    # We will use these xPosition vectors to actually jitter the target, as well as to save out the stimulus information
    xPosition = np.cumsum(xVelocity)
    if nFrames > walkFrames:
        x = np.arange(0, walkFrames, walkFrames/nFrames)
        xp = list(range(walkFrames))
        fp = xPosition
        xPosition = np.interp(x, xp, fp)

    xPosition = xPosition[0:nFrames]
    yPosition = np.zeros(len(xPosition))

    targetPositions = []
    for ii in range(len(xPosition)):
        targetPositions.append([xPosition[ii], yPosition[ii]])





    ## Make our stimulus

    # The gabor target
    target = visual.GratingStim(win=mywin, mask='gauss', units=units, size=[[circleRadius_pixels * 2, circleRadius_pixels * 2]],  contrast=contrast / 100, sf=sf_cyclesPerPixel)

    # The center hole of our target
    targetCenter = visual.Circle(mywin, radius=centerRadius_pixels, color=[0,0,0], units=units)



    ## Display the trial setup

    # Make the pre-trial text
    textString = 'Press Space to Begin Trial '+str(trialParams['trialNumber'])+' of '+str(trialParams['totalTrials'])
    preTrialText = visual.TextStim(win=mywin, pos=[0, 200], text=textString, color='red')

    # Show the pointer
    pointer = visual.GratingStim(win=mywin, size=3, pos=[0,0], sf=0, color='red', units=units)

    # Draw everythiing
    target.draw()
    targetCenter.draw()
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

    # Three second delay until trial start
    clock.wait(3)

    # Get the mouse going
    mouse = visual.CustomMouse(mywin)
    mouse.pointer = pointer

    # Prepare for trial

    frameTimes = []
    keyPresses = []
    mousePositions = []

    ## Perform trial
    for ii in range(nFrames):

        # Adjust the target
        target.pos = [xPosition[ii], yPosition[ii]]
        targetCenter.pos = [xPosition[ii], yPosition[ii]]

        target.draw()
        targetCenter.draw()


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

    # Quantify performance to provide feedback
    score = 0
    scoreSigma = pixelsPerCM
    for ii in range(nFrames):
        distance = ((mousePositions[ii][0] - xPosition[ii]) ** 2 + (mousePositions[ii][1] - yPosition[ii]) ** 2) ** 0.5
        thisScore = visual.filters.makeGauss(distance, mean=0, sd=scoreSigma, gain=1, base=0)
        score = score + thisScore * 1/nFrames

    trialParams.update({'score': score})
    trialParams.update({'scoreSigma': pixelsPerCM})

    scoreRounded = round(score*100, 2)
    textString = 'Score: '+str(scoreRounded)+'%'
    feedbackText = visual.TextStim(win=mywin, pos=[0, 0], text=textString, color='red')
    feedbackText.draw()
    mywin.flip()

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
    print('- Trial Complete')