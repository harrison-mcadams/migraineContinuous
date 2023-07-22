from psychopy import visual, core, event, logging, clock
import numpy as np
import random
import datetime
import pickle
import os
import matplotlib.pyplot as plt

## Trial params
fullScreen = True
screen = 0
proportionToPreserve = 0.5
viewingDistance_cm = 50
contrast = 100
nFrames = 60*20
basePath = os.path.expanduser('~') + '/Desktop/'
projectName = 'migraineContinuous/'
dataPath = basePath+projectName+'data/'
# Get directory information
today = datetime.date.today()
# Get today's date as a string
today_string = today.strftime('%Y-%m-%d')
dotSize_degrees = 3/60 # in degrees
circleRadius_degrees = 5

units = 'pix'

trialParams = {'subjectID': 'test4'}
trialParams.update({'experimentLabel': 'tadin2019Continuous'})
trialParams.update({'targetSize': circleRadius_degrees})
trialParams.update({'contrast': contrast})



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

targetPositions = []
for ii in range(len(xPosition)):
    targetPositions.append([xPosition[ii], yPosition[ii]])


## Make window
logging.setDefaultClock(clock.Clock())

mywin = visual.Window([1440, 900], fullscr=fullScreen, monitor='testMonitor', screen=screen,
                      units=units)
mywin.recordFrameIntervals = True

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

background = visual.NoiseStim(mywin, noiseType='binary', size=[[2000,2000]], noiseElementSize=dotSize_pixels, units=units, contrast=contrast/100)
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