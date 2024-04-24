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

        # Big nested for loop structure to set up our results variables
        for group in groups:

            if groupsCounter == 1:
                pooledCorrelograms = {group: []}
                pooledPeaks = {group: []}
                meanCorrelograms = {group: []}
                meanPeaks = {group: []}
                SEMCorrelograms = {group: []}
                SEMPeaks = {group: []}
            else:
                pooledCorrelograms.update({group: []})
                pooledPeaks.update({group: []})
                meanCorrelograms.update({group: []})
                meanPeaks.update({group: []})
                SEMCorrelograms.update({group: []})
                SEMPeaks.update({group: []})
            groupsCounter = groupsCounter + 1

            contrastCounter = 1
            for contrast in inputtedContrasts:
                if contrastCounter == 1:
                    pooledCorrelograms[group] = {'Contrast' + str(contrast): []}
                    pooledPeaks[group] = {'Contrast' + str(contrast): []}
                    meanCorrelograms[group] = {'Contrast' + str(contrast): []}
                    meanPeaks[group] = {'Contrast' + str(contrast): []}
                    SEMCorrelograms[group] = {'Contrast' + str(contrast): []}
                    SEMPeaks[group] = {'Contrast' + str(contrast): []}
                else:
                    pooledCorrelograms[group].update({'Contrast' + str(contrast): []})
                    pooledPeaks[group].update({'Contrast' + str(contrast): []})
                    meanCorrelograms[group].update({'Contrast' + str(contrast): []})
                    meanPeaks[group].update({'Contrast' + str(contrast): []})
                    SEMCorrelograms[group].update({'Contrast' + str(contrast): []})
                    SEMPeaks[group].update({'Contrast' + str(contrast): []})
                contrastCounter = contrastCounter + 1

                radiusCounter = 1
                for radius in inputtedTargetRadii:
                    if radiusCounter == 1:
                        pooledCorrelograms[group]['Contrast'+str(contrast)] =  {'Radius'+str(radius): []}
                        pooledPeaks[group]['Contrast'+str(contrast)] =  {'Radius'+str(radius): []}
                        meanCorrelograms[group]['Contrast'+str(contrast)] =  {'Radius'+str(radius): []}
                        meanPeaks[group]['Contrast'+str(contrast)] =  {'Radius'+str(radius): []}
                        SEMCorrelograms[group]['Contrast'+str(contrast)] =  {'Radius'+str(radius): []}
                        SEMPeaks[group]['Contrast'+str(contrast)] =  {'Radius'+str(radius): []}


                    else:
                        pooledCorrelograms[group]['Contrast'+str(contrast)].update({'Radius'+str(radius): []})
                        pooledPeaks[group]['Contrast'+str(contrast)].update({'Radius'+str(radius): []})
                        meanCorrelograms[group]['Contrast'+str(contrast)].update({'Radius'+str(radius): []})
                        meanPeaks[group]['Contrast'+str(contrast)].update({'Radius'+str(radius): []})
                        SEMCorrelograms[group]['Contrast'+str(contrast)].update({'Radius'+str(radius): []})
                        SEMPeaks[group]['Contrast'+str(contrast)].update({'Radius'+str(radius): []})

                    radiusCounter = radiusCounter + 1

        ## Do the pooling
        for group in groups:


            for subjectID in subjectIDs[group]:

                peaks, contrasts, targetRadii, correlograms = analyzeTadin.analyzeTadin(subjectID, inputtedContrasts, inputtedTargetRadii, comparison, True)

                peaks_2.append(peaks['Contrast2'])
                peaks_99.append(peaks['Contrast99'])

                for contrast in inputtedContrasts:
                    radiusCounter = 0
                    for radius in inputtedTargetRadii:
                        pooledCorrelograms[group]['Contrast'+str(contrast)]['Radius'+str(radius)].append(correlograms['Contrast'+str(contrast)][radiusCounter])
                        pooledPeaks[group]['Contrast'+str(contrast)]['Radius'+str(radius)].append(peaks['Contrast'+str(contrast)][radiusCounter])

                        radiusCounter = radiusCounter + 1

        ## Collapse pooling into mean and SEM
        for group in groups:
            for contrast in inputtedContrasts:
                radiusCounter = 0
                for radius in inputtedTargetRadii:
                    meanPeaks[group]['Contrast'+str(contrast)]['Radius'+str(radius)] = np.mean(pooledPeaks[group]['Contrast'+str(contrast)]['Radius'+str(radius)])
                    SEMPeaks[group]['Contrast'+str(contrast)]['Radius'+str(radius)] = np.std(pooledPeaks[group]['Contrast'+str(contrast)]['Radius'+str(radius)])/(len(pooledPeaks[group]['Contrast'+str(contrast)]['Radius'+str(radius)])**0.5)

                    meanCorrelograms[group]['Contrast'+str(contrast)]['Radius'+str(radius)] = np.mean(pooledCorrelograms[group]['Contrast'+str(contrast)]['Radius'+str(radius)],0)
                    SEMCorrelograms[group]['Contrast'+str(contrast)]['Radius'+str(radius)] = np.std(pooledCorrelograms[group]['Contrast'+str(contrast)]['Radius'+str(radius)],0)/(np.size(pooledPeaks[group]['Contrast'+str(contrast)]['Radius'+str(radius)],0)**0.5)


                radiusCounter = radiusCounter + 1

        ## Do some plotting

        groupColors = {'controls': 'black',
                       'migraine': 'red',
                       'ptha': 'blue'}

        contrastLineStyles = {'2': '--',
                              '99': '-'}

        # Plot peaks by size
        groupCounter = 0
        for group in groups:
            for contrast in contrasts:
                if contrast == 99:
                    plt.errorbar(
                        np.log(np.array(inputtedTargetRadii) * 2),
                        [meanPeaks[group]['Contrast'+str(contrast)]['Radius'+str(inputtedTargetRadii[0])], meanPeaks[group]['Contrast'+str(contrast)]['Radius'+str(inputtedTargetRadii[1])], meanPeaks[group]['Contrast'+str(contrast)]['Radius'+str(inputtedTargetRadii[2])], meanPeaks[group]['Contrast'+str(contrast)]['Radius'+str(inputtedTargetRadii[3])]],
                        [SEMPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[0])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[1])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[2])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[3])]],

                        color=groupColors[group],
                        label=groups[groupCounter],
                        linestyle=contrastLineStyles[str(contrast)]
                    )
                else:
                    plt.errorbar(
                        np.log(np.array(inputtedTargetRadii) * 2),
                        [meanPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[0])],
                         meanPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[1])],
                         meanPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[2])],
                         meanPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[3])]],
                        [SEMPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[0])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[1])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[2])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Radius' + str(inputtedTargetRadii[3])]],

                        color=groupColors[group],
                        linestyle=contrastLineStyles[str(contrast)]
                    )

            groupCounter = groupCounter + 1




        plt.xticks(np.log(targetRadii*2), targetRadii*2)
        plt.xlabel('Stimulus Size (degrees)')
        plt.ylabel('Kernel Peak (r)')
        plt.legend()
        plt.ylim([-0.025, 0.25])
        plt.savefig(savePath + 'groups_CRF_peaks.png')
        plt.close()


        # Plot correlograms by stimulus condition
        firstTimepoint = -1
        lastTimepoint = 2
        samplingRate = 1/1000

        correlationIndices = list(
            range(round(firstTimepoint * 1 / samplingRate), round(lastTimepoint * 1 / samplingRate)))
        correlationTimebase = np.array(correlationIndices) * samplingRate

        groupCounter = 0

        for contrast in contrasts:
            for radius in inputtedTargetRadii:
                for group in groups:
                    plt.plot(correlationTimebase, meanCorrelograms[group]['Contrast'+str(contrast)]['Radius'+str(radius)],
                             color=groupColors[group],
                             label=group,
                             )

                plt.xlabel('Time (s)')
                plt.ylabel('Cross Correlation')
                plt.legend()
                plt.ylim([-0.025, 0.25])
                plt.savefig(savePath + 'C'+str(contrast)+'_S'+str(2*radius)+'_crossCorrelogram.png')
                plt.close()

                groupCounter = groupCounter + 1


        results = {
                    'pooledPeaks': pooledPeaks,
                    'meanPeaks': meanPeaks,
                    'SEMPeaks': SEMPeaks,

                    'pooledCorrelograms': pooledCorrelograms,
                    'meanCorrelograms': meanCorrelograms,
                    'SEMCorrelograms': SEMCorrelograms

                }


        with open(savePath + 'C' + contrastsString + '_S' + sizesString + '_pooledResults.pkl', 'wb') as f:
            pickle.dump(results, f)
        f.close()

    return results


#makeGroupResponse(False)