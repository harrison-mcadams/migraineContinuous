import numpy as np
import analyzeTadin as analyzeTadin
import getExperimentParams as getExperimentParams
import glob
import os
import matplotlib.pyplot as plt

basicTrialParams = getExperimentParams.getExperimentParams('horizontalContinuous')


load = True
inputtedContrasts = [2,99]
inputtedTargetRadii = [0.75,1.5,3.0,6.0]
comparison = 'targetXVelocities-mouseXVelocities'

subjectIDs = glob.glob(os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/data/horizontalContinuous/SS*')
subjectIDs = [os.path.basename(x) for x in subjectIDs]

peaks_2 = []
peaks_99 = []


for subjectID in subjectIDs:

    peaks, contrasts, targetRadii = analyzeTadin.analyzeTadin(subjectID, inputtedContrasts, inputtedTargetRadii, comparison, load)

    peaks_2.append(peaks['Contrast2'])
    peaks_99.append(peaks['Contrast99'])

groupMean_peaks_2 = np.mean(peaks_2, 0)
groupMean_peaks_99 = np.mean(peaks_99, 0)

groupSEM_peaks_2 = np.std(peaks_2, 0)/len(peaks_2)**0.5
groupSEM_peaks_99 = np.std(peaks_99, 0)/len(peaks_99)**0.5

plt.errorbar(np.log(np.array(inputtedTargetRadii) * 2), groupMean_peaks_2, groupSEM_peaks_2,
             label='Contrast: ' + str(2))
plt.errorbar(np.log(np.array(inputtedTargetRadii) * 2), groupMean_peaks_99, groupSEM_peaks_99,
             label='Contrast: ' + str(99))

savePathRoot = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/analysis/'
savePath = savePathRoot + '/' + 'horizontalContinuous' + '/pooled/'
plt.xticks(np.log(targetRadii*2), targetRadii*2)
plt.xlabel('Stimulus Size (degrees)')
plt.ylabel('Kernel Peak (r)')
plt.legend()
plt.ylim([-0.025, 0.25])
plt.savefig(savePath + 'pooled_CRF_peaks.png')

