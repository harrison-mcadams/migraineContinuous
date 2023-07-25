def makeMotionDiscrimination(trialParams):

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
    frameRate = trialParams['frameRate']

    ## Set up the trial parameters
    viewingDistance_cm = trialParams['viewingDistance_cm']

    # Save stuff
    dataPath = trialParams['dataPath']
    today_string = trialParams['todayString']
    startTime = datetime.datetime.now()
    startTime = startTime.strftime("%H%M%S")
    trialParams.update({'startTime': startTime})

    # Visual params
    proportionToPreserve = 0.5
    trialParams.update({'proportionToPreserve': proportionToPreserve})
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
    background = trialParams['background']
    randomizeTarget = trialParams['randomizeTarget']
    randomizeBackground = trialParams['randomizeBackground']
    targetNoiseType = trialParams['targetNoiseType']
    backgroundNoiseType = trialParams['backgroundNoiseType']
    targetMask = trialParams['targetMask']
    targetMaskParams = trialParams['targetMaskParams']


    ## Prepare the random walk
    walkRefreshRate = 1/60
    walkFrames = int(np.ceil(1 / walkRefreshRate * trialLength_s))
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

    def makeBackgroundCoordinates(dotSize, mywin):

        fudgeFactor = 1
        xRange = range(-int(round(mywin.clientSize[0] / 2 * fudgeFactor)), int((mywin.clientSize[0] / 2 * fudgeFactor)))
        yRange = range(-int(round(mywin.clientSize[1] / 2 * fudgeFactor)), int(mywin.clientSize[1] / 2 * fudgeFactor))

        background_xys = []
        backgroundColors = []
        for xx in xRange:
            for yy in yRange:
                background_xys.append([xx * dotSize, yy * dotSize])
                color = random.randint(0, 1) * 2 - 1
                backgroundColors.append([color, color, color])

        background_xys = np.array(background_xys)
        return background_xys, backgroundColors

    circle_xys, colors = makeCircleCoordinates(circleRadius_pixels, dotSize_pixels)
    background_xys, backgroundColors = makeBackgroundCoordinates(dotSize_pixels, mywin)

    nDots = len(circle_xys)
    nBackgroundDots = len(background_xys)

    circle = visual.ElementArrayStim(win=mywin, units='pixels',
                                     nElements=len(circle_xys),
                                     elementTex=None,
                                     elementMask='circle',
                                     xys=circle_xys,
                                     sizes=dotSize_pixels * 1.1,
                                     colors=colors,
                                     fieldPos=[0, 0]
                                     )

    background = visual.ElementArrayStim(win=mywin, units='pixels',
                                         nElements=len(background_xys),
                                         elementTex=None,
                                         elementMask='circle',
                                         xys=background_xys,
                                         sizes=dotSize_pixels * 1.1,
                                         colors=backgroundColors,
                                         fieldPos=[0, 0]
                                         )

    frameTimes = []
    for i in range(nFrames):
        background.draw()
        backgroundRandomizeList = np.array([int(random.random() < 0.5) * 2 - 1 for _ in range(nBackgroundDots)])
        # backgroundRandomizeList = (random.sample(range(nBackgroundDots), round(nBackgroundDots * proportionToPreserve)))
        backgroundKeepList = (random.sample(range(nBackgroundDots), round(nBackgroundDots * proportionToPreserve)))
        backgroundRandomizeList[backgroundKeepList] = 1
        backgroundRandomizeArray = np.tile(backgroundRandomizeList, [3, 1])
        background.colors = background.colors * np.rot90(backgroundRandomizeArray)

        randomizeList = np.array([int(random.random() < 0.5) * 2 - 1 for _ in range(nDots)])
        keepList = (random.sample(range(nDots), round(nDots * proportionToPreserve)))
        randomizeList[keepList] = 1
        randomizeArray = np.tile(randomizeList, [3, 1])
        # circle.colors = circleColors[random.randint(0,nRandomFrames-1)]
        circle.colors = circle.colors * np.rot90(randomizeArray)

        circle.fieldPos = [xPosition[i], yPosition[i]]  # this will make the thing vertically
        circle.draw()
        # mywin.flip()
        frameTimes.append(mywin.lastFrameT)
        mywin.getMovieFrame(buffer='back')

    # Define path
    savePath=dataPath + trialParams['experimentName'] + '/' + trialParams['subjectID'] + '/' + today_string + '/'


    # Make the output folder
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    mywin.saveMovieFrames(savePath + startTime + '_S' + str(trialParams['targetRadius_degrees']) + '_C' + str(trialParams['contrast']) + '.mp4', fps=60)

    ## Package up the data to save out
    # Set the timebase relative to trial start
    frameTimes = np.array(frameTimes) - frameTimes[0]

    # Get velocities
    targetXVelocities = []
    targetYVelocities = []
#    mouseXVelocities = []
#    mouseYVelocities = []
    for ii in range(nFrames-1):
        targetXVelocities.append((xPosition[ii+1]-xPosition[ii])/(frameTimes[ii+1]-frameTimes[ii]))
        targetYVelocities.append((yPosition[ii+1]-yPosition[ii])/(frameTimes[ii+1]-frameTimes[ii]))

#        mouseXVelocities.append((np.array(mousePositions)[ii+1,0] - np.array(mousePositions)[ii,0])/(frameTimes[ii+1]-frameTimes[ii]))
#        mouseYVelocities.append((np.array(mousePositions)[ii+1,1]- np.array(mousePositions)[ii,1])/(frameTimes[ii+1]-frameTimes[ii]))

    # Package up the main output variable
    data = {
        'targetXs': xPosition,
        'targetXVelocities': targetXVelocities,
        'targetYs': yPosition,
        'targetYVelocities': targetYVelocities,
        'frameTimes': frameTimes,
        'trialParams': trialParams
    }




    # Save variable
    with open(savePath + startTime + '_S' + str(trialParams['targetRadius_degrees']) + '_C' + str(trialParams['contrast']) + '_raw.pkl', 'wb') as f:
        pickle.dump(data, f)
    f.close()

    # Write out text file of the results
    with open(savePath + startTime + '_S' + str(trialParams['targetRadius_degrees']) + '_C' + str(
            trialParams['contrast']) + '.txt', 'w') as g:
        g.write('time (s),targetX,targetY\n')
        for ii in range(len(frameTimes)):
            g.write(str(frameTimes[ii]) + ',' + str(targetPositions[ii][0]) +',' + str(targetPositions[ii][1]) + '\n')
    g.close()

    # For support
    print('boom')