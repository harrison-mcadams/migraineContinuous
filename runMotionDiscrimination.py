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
    mywin.recordFrameIntervals = True
    frameRate = mywin.getActualFrameRate()
    trialParams.update({'frameRate': frameRate})

    viewingDistance_cm = trialParams['viewingDistance_cm']

    dataPath = trialParams['dataPath']
    today_string = trialParams['todayString']
    startTime = datetime.datetime.now()
    startTime = startTime.strftime("%H%M%S")
    trialParams.update({'startTime': startTime})

    contrast = trialParams['contrast']
    nFrames = int(np.ceil(frameRate*20))
    trialParams.update({'nFrames': nFrames})
    dotSize_degrees = trialParams['dotSize_degrees']
    circleRadius_degrees = trialParams['targetRadius_degrees']
    background = trialParams['background']
    randomizeTarget = trialParams['randomizeTarget']


    ## Prepare the random walk
    nFrames = 60*20
    frameRate = 60
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
    xPosition = np.cumsum(xVelocity)
    yPosition = np.cumsum(yVelocity)

    targetPositions = []
    for ii in range(len(xPosition)):
        targetPositions.append([xPosition[ii], yPosition[ii]])




    pixelCorrectionFactor = mywin.clientSize[0]/mywin.size[0]
    pixelsPerCM = 2560/30 * pixelCorrectionFactor


    #stimulus = visual.DotStim(mywin, fieldSize=10, speed=0, dotLife=-1, nDots=1000, coherence=0)
    # Show 100 frames




    def convertDegreesToCM(degrees, viewingDistance_cm):
        cms = 2 * viewingDistance_cm * np.tan(np.deg2rad(degrees / 2))

        return cms

    dotSize_cm = convertDegreesToCM(dotSize_degrees, viewingDistance_cm)
    circleRadius_cm = convertDegreesToCM(circleRadius_degrees, viewingDistance_cm)

    dotSize_pixels = dotSize_cm * pixelsPerCM
    circleRadius_pixels = circleRadius_cm * pixelsPerCM

    if background == 'gray':
        target = visual.NoiseStim(mywin, noiseType='binary', mask='raisedCos', opacity=1, maskParams={'fringeWidth': 0.9}, size=[[circleRadius_pixels*2,circleRadius_pixels*2]], noiseElementSize=dotSize_pixels, units=units, contrast=contrast/100)
        background = visual.NoiseStim(mywin, noiseType='binary', mask='raisedCos', opacity=0, maskParams={'fringeWidth': 0.9}, size=[100,100], noiseElementSize=dotSize_pixels, units=units, contrast=contrast/100)
    elif background == 'pixels':
        background = visual.NoiseStim(mywin, noiseType='binary', opacity=1, size=[[2000,2000]], noiseElementSize=dotSize_pixels, units=units, contrast=contrast/100)
        target = visual.NoiseStim(mywin, noiseType='binary', size=circleRadius_pixels, noiseElementSize=dotSize_pixels, units=units, mask='circle', contrast=contrast/100)


    background.draw()
    target.draw()
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

    frameTimes = []

    mouse = event.Mouse()

    keyPresses = []
    mousePositions = []
    for ii in range(nFrames):
        background.draw()
        target.pos = [xPosition[ii], yPosition[ii]]
        if randomizeTarget:
            target.buildNoise()
        target.draw()
        mywin.flip()
        frameTimes.append(mywin.lastFrameT)
        mousePosition = mouse.getPos()
        mousePositions.append([mousePosition[0], mousePosition[1]])

        keys = event.getKeys(timeStamped=logging.defaultClock, keyList=['q', 'escape'])
        keyPresses.append(keys)
        event.clearEvents()
        for key in keys:
            if 'q' in key or 'escape' in key:
                core.quit()

    targetXVelocities = []
    targetYVelocities = []
    mouseXVelocities = []
    mouseYVelocities = []
    for ii in range(nFrames-1):
        targetXVelocities.append((xPosition[ii+1]-xPosition[ii])/(frameTimes[ii+1]-frameTimes[ii]))
        targetYVelocities.append((yPosition[ii+1]-yPosition[ii])/(frameTimes[ii+1]-frameTimes[ii]))

        mouseXVelocities.append((np.array(mousePositions)[ii+1,0] - np.array(mousePositions)[ii,0])/(frameTimes[ii+1]-frameTimes[ii]))
        mouseYVelocities.append((np.array(mousePositions)[ii+1,1]- np.array(mousePositions)[ii,1])/(frameTimes[ii+1]-frameTimes[ii]))


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






    savePath=dataPath + trialParams['experimentLabel'] + '/' + trialParams['subjectID'] + '/' + today_string + '/'

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    with open(savePath + startTime + '_S' + str(trialParams['targetSize']) + '_C' + str(trialParams['contrast']) + '_raw.pkl', 'wb') as f:
        pickle.dump(data, f)
    f.close()


    with open(savePath + startTime + '_S' + str(trialParams['targetSize']) + '_C' + str(
            trialParams['contrast']) + '.txt', 'w') as g:
        g.write('time (s),targetX,targetY,mouseX,mouseY\n')
        for ii in range(len(frameTimes)):
            g.write(str(frameTimes[ii]) + ',' + str(targetPositions[ii][0]) +',' + str(targetPositions[ii][1]) + ',' + str(mousePositions[ii][0]) + ',' + str(mousePositions[ii][1]) + '\n')
    g.close()

    print('boom')