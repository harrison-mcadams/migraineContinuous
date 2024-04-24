def makePooledResponse(loadBehavior):

    import numpy as np
    import analyzeTadin as analyzeTadin
    import getExperimentParams as getExperimentParams
    import glob
    import pickle
    import os
    import matplotlib.pyplot as plt

    import makeSubjectList.py

    basicTrialParams = getExperimentParams.getExperimentParams('horizontalContinuous')


    load = loadBehavior

    inputtedContrasts = [2, 99]
    inputtedTargetRadii = [0.75, 1.5, 3.0, 6.0]
    contrastsString = ",".join(str(x) for x in inputtedContrasts)
    sizesString = ",".join(str(x) for x in inputtedTargetRadii)

    comparison = 'targetXVelocities-mouseXVelocities'

    savePathRoot = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/analysis/'
    savePath = savePathRoot + '/' + 'horizontalContinuous' + '/meanResponses/pooled/'

    subjectIDs = glob.glob(os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/data/horizontalContinuous/SS*')
    subjectIDs = [os.path.basename(x) for x in subjectIDs]

    if load:
        with open(savePath + 'C' + contrastsString + '_S' + sizesString + '_pooledResults.pkl', 'rb') as f:
            results = pickle.load(f)

    else:



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


        plt.xticks(np.log(targetRadii*2), targetRadii*2)
        plt.xlabel('Stimulus Size (degrees)')
        plt.ylabel('Kernel Peak (r)')
        plt.legend()
        plt.ylim([-0.025, 0.25])
        plt.savefig(savePath + 'pooled_CRF_peaks.png')


        pooledPeaks = {'Contrast2': groupMean_peaks_2}
        pooledPeaks.update({'Contrast99': groupMean_peaks_99})

        pooledPeaksSEM = {'Contrast2': groupSEM_peaks_2}
        pooledPeaksSEM.update({'Contrast99': groupSEM_peaks_99})

        results = {
                    'peaks': pooledPeaks,
                    'peaksSEM': pooledPeaksSEM,
                    'contrasts': contrasts,
                    'targetRadii': targetRadii
                }


        with open(savePath + 'C' + contrastsString + '_S' + sizesString + '_pooledResults.pkl', 'wb') as f:
            pickle.dump(results, f)
        f.close()

    return results


