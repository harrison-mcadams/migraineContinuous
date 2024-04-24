def makeGroupResponse(loadBehavior):

    import numpy as np
    import analyzeTadin as analyzeTadin
    import getExperimentParams as getExperimentParams
    import glob
    import pickle
    import os
    import matplotlib.pyplot as plt

    import makeSubjectList

    basicTrialParams = getExperimentParams.getExperimentParams('horizontalContinuous')


    load = loadBehavior

    inputtedContrasts = [2, 99]
    if loadBehavior:
        inputtedTargetRadii = [0.75, 1.5, 3.0, 6.0]
    else:
        inputtedTargetRadii = [0.75, 1.5, 3, 6]
        inputtedTargetRadii = [0.75, 1.5, 3.0, 6.0]
    contrastsString = ",".join(str(x) for x in inputtedContrasts)
    sizesString = ",".join(str(x) for x in inputtedTargetRadii)

    comparison = 'targetXVelocities-mouseXVelocities'

    savePathRoot = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/analysis/'
    savePath = savePathRoot + '/' + 'horizontalContinuous' + '/meanResponses/pooled/'

    subjectIDs = makeSubjectList.makeSubjectList()

    if load:
        with open(savePath + 'C' + contrastsString + '_S' + sizesString + '_pooledResults.pkl', 'rb') as f:
            results = pickle.load(f)

    else:



        peaks_2 = []
        peaks_99 = []

        groups = ['controls', 'migraine', 'ptha']
        groupsCounter = 1
        for group in groups:

            if groupsCounter == 1:
                pooledCorrelograms = {group: []}
            else:
                pooledCorrelograms.update({group: []})
            groupsCounter = groupsCounter + 1

            contrastCounter = 1
            for contrast in inputtedContrasts:
                if contrastCounter == 1:
                    pooledCorrelograms[group] = {'Contrast' + str(contrast): []}
                else:
                    pooledCorrelograms[group].update({'Contrast' + str(contrast): []})
                contrastCounter = contrastCounter + 1

                sizeCounter = 1
                for size in inputtedTargetRadii:
                    if sizeCounter == 1:
                        pooledCorrelograms[group]['Contrast'+str(contrast)] =  {'Size'+str(size): []}
                    else:
                        pooledCorrelograms[group]['Contrast'+str(contrast)].update({'Size'+str(size): []})
                    sizeCounter = sizeCounter + 1


        for subjectIDc in subjectIDs['controls']:
            group = 'controls'

            peaks, contrasts, targetRadii, correlograms = analyzeTadin.analyzeTadin(subjectIDc, inputtedContrasts, inputtedTargetRadii, comparison, False)

            peaks_2.append(peaks['Contrast2'])
            peaks_99.append(peaks['Contrast99'])

            for contrast in inputtedContrasts:
                sizeCounter = 0
                for size in inputtedTargetRadii:
                    pooledCorrelograms[group]['Contrast'+str(contrast)]['Size'+str(size)].append(correlograms['Contrast'+str(contrast)][sizeCounter])
                    sizeCounter = sizeCounter + 1
        controlMean_peaks_2 = np.mean(peaks_2, 0)
        controlMean_peaks_99 = np.mean(peaks_99, 0)

        controlSEM_peaks_2 = np.std(peaks_2, 0)/len(peaks_2)**0.5
        controlSEM_peaks_99 = np.std(peaks_99, 0)/len(peaks_99)**0.5

        plt.errorbar(np.log(np.array(inputtedTargetRadii) * 2), controlMean_peaks_2, controlSEM_peaks_2,
                    color='k', linestyle='--')
        plt.errorbar(np.log(np.array(inputtedTargetRadii) * 2), controlMean_peaks_99, controlSEM_peaks_99,
                     label='Controls', color='k', linestyle='-')

        migrainePeaks_2 = []
        migrainePeaks_99 = []


        for subjectIDm in subjectIDs['migraine']:
            group = 'migraine'

            peaks, contrasts, targetRadii, correlograms = analyzeTadin.analyzeTadin(subjectIDm, inputtedContrasts, inputtedTargetRadii, comparison, True)

            migrainePeaks_2.append(peaks['Contrast2'])
            migrainePeaks_99.append(peaks['Contrast99'])

            for contrast in inputtedContrasts:
                sizeCounter = 0
                for size in inputtedTargetRadii:
                    pooledCorrelograms[group]['Contrast'+str(contrast)]['Size'+str(size)].append(correlograms['Contrast'+str(contrast)][sizeCounter])
                    sizeCounter = sizeCounter + 1

        migraineMean_peaks_2 = np.mean(migrainePeaks_2, 0)
        migraineMean_peaks_99 = np.mean(migrainePeaks_99, 0)

        migraineSEM_peaks_2 = np.std(migrainePeaks_2, 0)/len(migrainePeaks_2)**0.5
        migraineSEM_peaks_99 = np.std(migrainePeaks_99, 0)/len(migrainePeaks_2)**0.5

        plt.errorbar(np.log(np.array(inputtedTargetRadii) * 2), migraineMean_peaks_2, migraineSEM_peaks_2,
                    color='r', linestyle='--')
        plt.errorbar(np.log(np.array(inputtedTargetRadii) * 2), migraineMean_peaks_99, migraineSEM_peaks_99,
                     label='Migraine', color='r', linestyle='-')

        pthaPeaks_2 = []
        pthaPeaks_99 = []

        for subjectIDp in subjectIDs['ptha']:

            group = 'ptha'

            peaks, contrasts, targetRadii, correlograms = analyzeTadin.analyzeTadin(subjectIDp, inputtedContrasts, inputtedTargetRadii, comparison, True)

            pthaPeaks_2.append(peaks['Contrast2'])
            pthaPeaks_99.append(peaks['Contrast99'])

            for contrast in inputtedContrasts:
                sizeCounter = 0
                for size in inputtedTargetRadii:
                    pooledCorrelograms[group]['Contrast'+str(contrast)]['Size'+str(size)].append(correlograms['Contrast'+str(contrast)][sizeCounter])
                    sizeCounter = sizeCounter + 1

        pthaMean_peaks_2 = np.mean(pthaPeaks_2, 0)
        pthaMean_peaks_99 = np.mean(pthaPeaks_99, 0)

        pthaSEM_peaks_2 = np.std(pthaPeaks_2, 0)/len(pthaPeaks_2)**0.5
        pthaSEM_peaks_99 = np.std(pthaPeaks_99, 0)/len(pthaPeaks_99)**0.5

        plt.errorbar(np.log(np.array(inputtedTargetRadii) * 2), pthaMean_peaks_2, pthaSEM_peaks_2,
                    color='b', linestyle='--')
        plt.errorbar(np.log(np.array(inputtedTargetRadii) * 2), pthaMean_peaks_99, pthaSEM_peaks_99,
                     label='PTHA', color='b', linestyle='-')


        plt.xticks(np.log(targetRadii*2), targetRadii*2)
        plt.xlabel('Stimulus Size (degrees)')
        plt.ylabel('Kernel Peak (r)')
        plt.legend()
        plt.ylim([-0.025, 0.25])
        plt.savefig(savePath + 'groups_CRF_peaks.png')


        pooledPeaks = {'Contrast2': groupMean_peaks_2}
        pooledPeaks.update({'Contrast99': groupMean_peaks_99})

        pooledPeaksSEM = {'Contrast2': groupSEM_peaks_2}
        pooledPeaksSEM.update({'Contrast99': groupSEM_peaks_99})

        results = {
                    'peaks': pooledPeaks,
                    'peaksSEM': pooledPeaksSEM,
                    'contrasts': contrasts,
                    'targetRadii': targetRadii,
                    'correlograms': pooledCorrelograms
                }


        with open(savePath + 'C' + contrastsString + '_S' + sizesString + '_pooledResults.pkl', 'wb') as f:
            pickle.dump(results, f)
        f.close()

    return results


#makeGroupResponse(False)