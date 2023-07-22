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
contrast = 100
nFrames = 60*20


units = 'pix'



startTime = datetime.datetime.now()

startTime = startTime.strftime("%H%M%S")

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
#plt.plot(xPosition)


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

background = visual.NoiseStim(mywin, noiseType='binary', size=mywin.clientSize, noiseElementSize=dotSize_pixels, units=units, contrast=contrast/100)
target = visual.NoiseStim(mywin, noiseType='binary', size=circleRadius_pixels, noiseElementSize=dotSize_pixels, units=units, mask='circle', contrast=contrast/100)
background.draw()
target.draw()
mywin.flip()

frameTimes = []

mouse = event.Mouse()

mousePositions = []
for ii in range(nFrames):
    background.draw()
    target.pos = [xPosition[ii], yPosition[ii]]
    target.buildNoise()
    target.draw()
    mywin.flip()
    frameTimes.append(mywin.lastFrameT)
    mousePosition = mouse.getPos()
    mousePositions.append([mousePosition[0], mousePosition[1]])




print('boom')