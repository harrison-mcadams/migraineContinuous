import analyzeContinuous
import matplotlib.pyplot as plt
import numpy as np

subjectID = '500ms_varyContrast'
experimentName = 'battista'
contrasts = [2, 50, 90]
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
plt.xlabel('Contrast (%)')
plt.ylabel('Kernel Peak (r)')
plt.xticks(np.log(contrasts), contrasts)
plt.savefig('/Users/carlynpattersongentile/Desktop/migraineContinuous/analysis/' + experimentName + '/' + subjectID + '/CRF.png')