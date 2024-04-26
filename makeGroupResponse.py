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

    sizes = [1.5, 3, 6, 12]
    contrasts = [2, 99]

    contrastsString = ",".join(str(x) for x in contrasts)
    sizesString = ",".join(str(x) for x in sizes)

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
            for contrast in contrasts:
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

                sizeCounter = 1
                for size in sizes:
                    if sizeCounter == 1:
                        pooledCorrelograms[group]['Contrast'+str(contrast)] =  {'Size'+str(size): []}
                        pooledPeaks[group]['Contrast'+str(contrast)] =  {'Size'+str(size): []}
                        meanCorrelograms[group]['Contrast'+str(contrast)] =  {'Size'+str(size): []}
                        meanPeaks[group]['Contrast'+str(contrast)] =  {'Size'+str(size): []}
                        SEMCorrelograms[group]['Contrast'+str(contrast)] =  {'Size'+str(size): []}
                        SEMPeaks[group]['Contrast'+str(contrast)] =  {'Size'+str(size): []}


                    else:
                        pooledCorrelograms[group]['Contrast'+str(contrast)].update({'Size'+str(size): []})
                        pooledPeaks[group]['Contrast'+str(contrast)].update({'Size'+str(size): []})
                        meanCorrelograms[group]['Contrast'+str(contrast)].update({'Size'+str(size): []})
                        meanPeaks[group]['Contrast'+str(contrast)].update({'Size'+str(size): []})
                        SEMCorrelograms[group]['Contrast'+str(contrast)].update({'Size'+str(size): []})
                        SEMPeaks[group]['Contrast'+str(contrast)].update({'Size'+str(size): []})

                    sizeCounter = sizeCounter + 1

        ## Do the pooling
        for group in groups:


            for subjectID in subjectIDs[group]:

                stats, correlograms = analyzeTadin.analyzeTadin(subjectID, load=load)



                for contrast in contrasts:
                    sizeCounter = 0
                    for size in sizes:
                        pooledCorrelograms[group]['Contrast'+str(contrast)]['Size'+str(size)].append(correlograms['Contrast'+str(contrast)]['Size'+str(size)])
                        pooledPeaks[group]['Contrast'+str(contrast)]['Size'+str(size)].append(stats['peak']['Contrast'+str(contrast)]['Size'+str(size)])

                        sizeCounter = sizeCounter + 1

        ## Collapse pooling into mean and SEM
        for group in groups:
            for contrast in contrasts:
                sizeCounter = 0
                for size in sizes:
                    meanPeaks[group]['Contrast'+str(contrast)]['Size'+str(size)] = np.mean(pooledPeaks[group]['Contrast'+str(contrast)]['Size'+str(size)])
                    SEMPeaks[group]['Contrast'+str(contrast)]['Size'+str(size)] = np.std(pooledPeaks[group]['Contrast'+str(contrast)]['Size'+str(size)])/(len(pooledPeaks[group]['Contrast'+str(contrast)]['Size'+str(size)])**0.5)

                    meanCorrelograms[group]['Contrast'+str(contrast)]['Size'+str(size)] = np.mean(pooledCorrelograms[group]['Contrast'+str(contrast)]['Size'+str(size)],0)
                    SEMCorrelograms[group]['Contrast'+str(contrast)]['Size'+str(size)] = np.std(pooledCorrelograms[group]['Contrast'+str(contrast)]['Size'+str(size)],0)/(np.size(pooledPeaks[group]['Contrast'+str(contrast)]['Size'+str(size)],0)**0.5)


                sizeCounter = sizeCounter + 1

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
                        np.log(sizes),
                        [meanPeaks[group]['Contrast'+str(contrast)]['Size'+str(sizes[0])], meanPeaks[group]['Contrast'+str(contrast)]['Size'+str(sizes[1])], meanPeaks[group]['Contrast'+str(contrast)]['Size'+str(sizes[2])], meanPeaks[group]['Contrast'+str(contrast)]['Size'+str(sizes[3])]],
                        [SEMPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[0])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[1])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[2])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[3])]],

                        color=groupColors[group],
                        label=groups[groupCounter],
                        linestyle=contrastLineStyles[str(contrast)]
                    )
                else:
                    plt.errorbar(
                        np.log(sizes),
                        [meanPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[0])],
                         meanPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[1])],
                         meanPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[2])],
                         meanPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[3])]],
                        [SEMPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[0])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[1])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[2])],
                         SEMPeaks[group]['Contrast' + str(contrast)]['Size' + str(sizes[3])]],

                        color=groupColors[group],
                        linestyle=contrastLineStyles[str(contrast)]
                    )

            groupCounter = groupCounter + 1




        plt.xticks(np.log(sizes), sizes)
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
            for size in sizes:
                for group in groups:
                    plt.plot(correlationTimebase, meanCorrelograms[group]['Contrast'+str(contrast)]['Size'+str(size)],
                             color=groupColors[group],
                             label=group,
                             )

                plt.xlabel('Time (s)')
                plt.ylabel('Cross Correlation')
                plt.legend()
                plt.ylim([-0.025, 0.25])
                plt.savefig(savePath + 'C'+str(contrast)+'_S'+str(size)+'_crossCorrelogram.png')
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


makeGroupResponse(False)