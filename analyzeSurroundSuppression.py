import analyzeContinuous
import matplotlib.pyplot as plt
import numpy as np
import os

subjectID = '100ms_64'
experimentName = 'experiment_2_simplified'
contrasts = [64]
spatialFrequency = 1

centerPeaks = []
surroundPeaks = []
for cc in contrasts:
    centerPeak, centerLag, centerWidth, surroundPeak, surroundLag, surroundWidth = analyzeContinuous.analyzeContinuous(subjectID, experimentName, cc, spatialFrequency, 'all')
    centerPeaks.append(centerPeak)
    surroundPeaks.append(surroundPeak)


plt.plot(np.log(contrasts), centerPeaks, label='Center')
plt.plot(np.log(contrasts), surroundPeaks, label='Surround')
plt.legend()
plt.xlabel('Contrast (%)')
plt.ylabel('Kernel Peak (r)')
plt.savefig(os.path.expanduser('~') + '/Desktop/migraineContinuous/analysis/' + experimentName + '/' + subjectID + '/CRF.png')
plt.xticks(np.log(contrasts), contrasts)
