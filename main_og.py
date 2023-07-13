from psychopy import visual, core, event, logging, clock
from psychopy.hardware import keyboard
import numpy as np
import random
import math

## Make window
logging.setDefaultClock(clock.Clock())
mywin = visual.Window([800,600], monitor='testMonitor', units='deg')
#mywin = visual.Window([800,600], monitor='testMonitor', units='deg', clock=clock.Clock())


mywin.recordFrameIntervals = True

## Experiment parameters
duration = 60 #s
desiredTrialLength = 16/1000 #s, taken from bhat 2018

frameRate = mywin.getActualFrameRate()
framesPerTrial = round(frameRate * desiredTrialLength)
actualTrialLength = 1/frameRate*framesPerTrial

totalFrames = round(duration * frameRate)

## Design the visual stimuli
# Design the main center grating

# Make Gaussian to be applied as mask
sigma = 100
lengthOfMask = 256
y = visual.filters.makeGauss(np.array(range(lengthOfMask)), mean=lengthOfMask/2, sd=sigma, gain=2.0, base=-1.0)
mask = np.tile(y, (lengthOfMask,1))



grating = visual.GratingStim(win=mywin, mask=mask, size=3, pos=[-0,0], sf=3)

# Design the fixation point
#fixation = visual.GratingStim(win=mywin, size=0.5, pos=[0,0], sf=0, rgb=-1)

## Set up to run the experiment
# Get keyboard
#kb = keyboard.Keyboard()

# Get initial figures on screen
grating.draw()
#fixation.draw()
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

keyPresses = []
frameTimes = []
stimulusDirection = []

#kb.clock.reset()
mywin.frameClock.reset()

for ii in range(totalFrames):

    if (ii/framesPerTrial).is_integer():
        # Determine if we're flipping direction if we're starting a new trial
        direction = random.randint(0,1)*2 - 1


    grating.setPhase(direction * 0.05, '+')  # advance phase by 0.05 of a cycle
    grating.draw()
    #fixation.draw()
    mywin.flip()

    frameTimes.append(mywin.lastFrameT)
    stimulusDirection.append(direction)

    keys = event.getKeys(timeStamped=logging.defaultClock)
    keyPresses.append(keys)
    event.clearEvents()



#keys = kb.getKeys()
    #keys = event.getKeys(timeStamped=mywin.frameClock)
#keyPresses.append(keys)

#keyPresses = filter(None, keyPresses)
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

print(keys)
