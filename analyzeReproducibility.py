import analyzeContinuous
import matplotlib.pyplot as plt
import numpy as np
import random

subjectID = '100ms_repeats'
experimentName = 'experiment_2_simplified'
contrast = 2
spatialFrequency = 1

nBootstraps = 100
trialSizesToAnalyze = [1, 2, 3, 4, 5]

centerMeans = []
centerSEMs = []
surroundMeans = []
surroundSEMs = []

for tt in trialSizesToAnalyze:

    nTrials = tt
    centerPeaks = []
    surroundPeaks = []
    for ii in range(nBootstraps):

        trialList = random.choices((np.array(range(len(trialSizesToAnalyze)))+1), k=nTrials)
        centerPeak, centerLag, centerWidth, surroundPeak, surroundLag, surroundWidth = analyzeContinuous.analyzeContinuous(subjectID, experimentName, contrast, spatialFrequency, trialList)
        centerPeaks.append(centerPeak)
        surroundPeaks.append(surroundPeak)

    meanCenterPeaks = np.mean(centerPeaks)
    centerMeans.append(meanCenterPeaks)
    meanSurroundPeaks = np.mean(surroundPeaks)
    surroundMeans.append(meanSurroundPeaks)

    semCenterPeaks = np.std(centerPeaks)
    centerSEMs.append(semCenterPeaks)
    semSurroundPeaks = np.std(surroundPeaks)
    surroundSEMs.append(semSurroundPeaks)

plt.errorbar(trialSizesToAnalyze, centerMeans, yerr=centerSEMs, label='Center')
plt.errorbar(trialSizesToAnalyze, surroundMeans, yerr=surroundSEMs, label='Surround')
plt.legend()
plt.xlabel('Number of Trials')
plt.ylabel('Kernel Peak (+/- SEM)')
plt.savefig(os.path.expanduser('~') + '/Desktop/migraineContinuous/analysis/' + experimentName + '/' + subjectID + '/' + 'SF' + str(spatialFrequency) + '_C' + str(contrast) + '_errorAnalysis.png')

print('yay')

# Standard deviation of the bootstrap sample estimates the standard error of the mean of the initial sample
