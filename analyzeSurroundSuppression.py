import analyzeContinuous
import matplotlib.pyplot as plt
import numpy as np

subjectID = 'harry_200ms'
experimentName = 'experiment_2_simplified'
contrasts = [92]
spatialFrequency = 1

centerPeaks = []
surroundPeaks = []
for cc in contrasts:
    centerPeak, centerLag, centerWidth, surroundPeak, surroundLag, surroundWidth = analyzeContinuous.analyzeContinuous(subjectID, experimentName, cc, spatialFrequency)
    centerPeaks.append(centerPeak)
    surroundPeaks.append(surroundPeak)
    
#contrast = 16
#analyzeContinuous.analyzeContinuous(subjectID, experimentName, contrast, spatialFrequency)

plt.plot(np.log(contrasts), centerPeaks, label='Center')
plt.plot(np.log(contrasts), surroundPeaks, label='Surround')
plt.legend()