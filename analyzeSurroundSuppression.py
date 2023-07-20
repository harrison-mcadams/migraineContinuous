import analyzeContinuous
import matplotlib.pyplot as plt
import numpy as np
import os

subjectID = '100ms_repeats'
experimentName = 'experiment_2_simplified'
contrasts = [2]
spatialFrequency = 1
nTrials = 5

centerPeaks = []
surroundPeaks = []
for cc in contrasts:
    for tt in range(nTrials):
        analyzeContinuous.analyzeContinuous(subjectID, experimentName, cc, spatialFrequency, [tt+1], '_trial'+str(tt+1))


    centerPeak, centerLag, centerWidth, surroundPeak, surroundLag, surroundWidth = analyzeContinuous.analyzeContinuous(subjectID, experimentName, cc, spatialFrequency, 'all', '')
    centerPeaks.append(centerPeak)
    surroundPeaks.append(surroundPeak)


plt.plot(np.log(contrasts), centerPeaks, label='Center')
plt.plot(np.log(contrasts), surroundPeaks, label='Surround')
plt.legend()
plt.xlabel('Contrast (%)')
plt.ylabel('Kernel Peak (r)')
plt.savefig(os.path.expanduser('~') + '/Desktop/migraineContinuous/analysis/' + experimentName + '/' + subjectID + '/CRF.png')
plt.xticks(np.log(contrasts), contrasts)
