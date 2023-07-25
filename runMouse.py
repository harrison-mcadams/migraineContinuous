from psychopy import visual, core, event, logging, clock
import numpy as np
import random
import datetime
import pickle
import os
import matplotlib.pyplot as plt

## Trial params
fullScreen = False
screen = 0
proportionToPreserve = 0.5
viewingDistance_cm = 50



units = 'pixels'



startTime = datetime.datetime.now()

startTime = startTime.strftime("%H%M%S")




## Make window
logging.setDefaultClock(clock.Clock())

mywin = visual.Window(fullscr=fullScreen, monitor='testMonitor', screen=screen,
                      units=units)
mywin.recordFrameIntervals = True

pixelCorrectionFactor = mywin.clientSize[0]/mywin.size[0]
pixelsPerCM = 2560/30 * pixelCorrectionFactor


#stimulus = visual.DotStim(mywin, fieldSize=10, speed=0, dotLife=-1, nDots=1000, coherence=0)
# Show 100 frames

dotSize_degrees = 3/60 # in degrees
circleRadius_degrees = 5


def convertDegreesToCM(degrees, viewingDistance_cm):
    cms = 2 * viewingDistance_cm * np.tan(np.deg2rad(degrees / 2))

    return cms

dotSize_cm = convertDegreesToCM(dotSize_degrees, viewingDistance_cm)
circleRadius_cm = convertDegreesToCM(circleRadius_degrees, viewingDistance_cm)

dotSize_pixels = dotSize_cm * pixelsPerCM
circleRadius_pixels = circleRadius_cm * pixelsPerCM


def makeCircleCoordinates(circleRadius, dotSize):

    radius_inDots = int(np.ceil(circleRadius/dotSize))

    circle_xys = []
    colors = []
    for xx in range(-radius_inDots, radius_inDots+1):
        for yy in range(-radius_inDots, radius_inDots+1):
            if (xx**2 + yy**2)**0.5 <= radius_inDots:
                circle_xys.append([xx*dotSize, yy*dotSize])
                color = random.randint(0, 1) * 2 - 1
                colors.append([color, color, color])

    colors = np.array(colors)
    circle_xys = np.array(circle_xys)
    return circle_xys, colors

def makeBackgroundCoordinates(dotSize, mywin):

    fudgeFactor = 1
    xRange = range(-int(round(mywin.clientSize[0]/2 * fudgeFactor)), int((mywin.clientSize[0]/2 * fudgeFactor)))
    yRange = range(-int(round(mywin.clientSize[1]/2 * fudgeFactor)), int(mywin.clientSize[1]/2 * fudgeFactor))

    background_xys = []
    backgroundColors = []
    for xx in xRange:
        for yy in yRange:
            background_xys.append([xx*dotSize, yy*dotSize])
            color = random.randint(0, 1) * 2 - 1
            backgroundColors.append([color, color, color])

    background_xys = np.array(background_xys)
    return background_xys, backgroundColors

circle_xys, colors = makeCircleCoordinates(circleRadius_pixels, dotSize_pixels)
background_xys, backgroundColors = makeBackgroundCoordinates(dotSize_pixels, mywin)

nDots = len(circle_xys)
nBackgroundDots = len(background_xys)


circle = visual.ElementArrayStim(win=mywin, units='pixels',
                                 nElements = len(circle_xys),
                                 elementTex=None,
                                 elementMask='circle',
                                 xys=circle_xys,
                                 sizes=dotSize_pixels*1.1,
                                 colors=colors,
                                 fieldPos=[0,0]
                                 )

background = visual.ElementArrayStim(win=mywin, units='pixels',
                                 nElements = len(background_xys),
                                 elementTex=None,
                                 elementMask='circle',
                                 xys=background_xys,
                                 sizes=dotSize_pixels*1.1,
                                 colors=backgroundColors,
                                 fieldPos=[0,0]
                                 )




#for ii in circle_xys:
#    plt.plot(ii[0], ii[1], 'o')

background.draw()
circle.draw()
#mywin.flip()

nFrames = 120*20
nRandomFrames = 100




#noise = visual.NoiseStim(mywin, noiseType='binary', size=[200, 200], noiseElementSize=1, units='pix')
#noise.draw()
#mywin.flip()

background_xys = []
backgroundColors = []

circle_xys = []
colors = []
trialLength_s = 20
frameRate = 60

walkRefreshRate = 1 / 60
walkFrames = int(np.ceil(1 / walkRefreshRate * trialLength_s))
arcminsPerPixel = 2.6 / 2
mean = 0
std = 4  # gives speed of 6.6 degrees per second approximately, to match what Tadin did. Note that the original continuous paper from Johannes had this at 1
xVelocity = np.random.normal(mean, std, size=walkFrames)
yVelocity = np.random.normal(mean, std, size=walkFrames)
speed_pixelsPerFrame = (xVelocity ** 2 + yVelocity ** 2) ** 0.5
speed_pixelsPerSecond = speed_pixelsPerFrame * frameRate
speed_arcminPerSecond = speed_pixelsPerSecond * arcminsPerPixel
speed_degreePerSecond = speed_arcminPerSecond / 60
print(np.mean(speed_degreePerSecond))

# We will use these xPosition vectors to actually jitter the target, as well as to save out the stimulus information
xPosition = np.cumsum(xVelocity)
yPosition = np.cumsum(yVelocity)


frameTimes = []
for i in range(60*20):
    background.draw()
    backgroundRandomizeList = np.array([int(random.random() < 0.5)*2 - 1 for _ in range(nBackgroundDots)])
    #backgroundRandomizeList = (random.sample(range(nBackgroundDots), round(nBackgroundDots * proportionToPreserve)))
    backgroundKeepList = (random.sample(range(nBackgroundDots), round(nBackgroundDots * proportionToPreserve)))
    backgroundRandomizeList[backgroundKeepList] = 1
    backgroundRandomizeArray = np.tile(backgroundRandomizeList, [3,1])
    background.colors = background.colors * np.rot90(backgroundRandomizeArray)

    randomizeList = np.array([int(random.random() < 0.5)*2 - 1 for _ in range(nDots)])
    keepList = (random.sample(range(nDots), round(nDots * proportionToPreserve)))
    randomizeList[keepList] = 1
    randomizeArray = np.tile(randomizeList, [3,1])
    #circle.colors = circleColors[random.randint(0,nRandomFrames-1)]
    circle.colors = circle.colors * np.rot90(randomizeArray)


    circle.fieldPos = [xPosition[i], yPosition[i]] # this will make the thing vertically
    circle.draw()
    #mywin.flip()
    frameTimes.append(mywin.lastFrameT)
    mywin.getMovieFrame(buffer='back')



mywin.saveMovieFrames(os.path.expanduser('~')+'/Desktop/test.mp4', fps=60)

print('done yo')