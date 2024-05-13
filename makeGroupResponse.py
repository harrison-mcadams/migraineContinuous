def makeGroupResponse(**kwargs):

    import numpy as np
    import analyzeTadin as analyzeTadin
    import getExperimentParams as getExperimentParams
    import glob
    import pickle
    import os
    import matplotlib.pyplot as plt

    import makeSubjectList
    import makeStruct

    basicTrialParams = getExperimentParams.getExperimentParams('horizontalContinuous')


    if 'loadBehavior' in kwargs:
        loadBehavior = kwargs['loadBehavior']
    else:
        loadBehavior = False
    load = loadBehavior

    sizes = [1.5, 3, 6, 12]
    contrasts = [2, 99]

    contrastFieldNames = []
    for contrast in contrasts:
        contrastFieldNames.append('Contrast'+str(contrast))

    sizeFieldNames = []
    for size in sizes:
        sizeFieldNames.append('Size'+str(size))

    contrastsString = ",".join(str(x) for x in contrasts)
    sizesString = ",".join(str(x) for x in sizes)

    comparison = 'targetXVelocities-mouseXVelocities'

    savePathRoot = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/analysis/'
    savePath = savePathRoot + '/' + 'horizontalContinuous' + '/correlograms/pooled/'

    subjectIDs = makeSubjectList.makeSubjectList(makePooled=True)

    if load:
        with open(savePath + 'C' + contrastsString + '_S' + sizesString + '_pooledResults.pkl', 'rb') as f:
            results = pickle.load(f)

        summaryResults = results['summaryResults']
        pooledResults = results['pooledResults']
    else:





        groupsToPool = ['controls', 'migraine', 'ptha', 'pooled']
        groups = ['controls', 'migraine', 'ptha']


        measures = ['peaks', 'widths', 'lags', 'correlograms']
        measuresForSummary = ['peaks', 'widths', 'lags', 'correlograms', 'peaksSEM', 'widthsSEM', 'lagsSEM']
        groupsCounter = 1




        pooledResults = makeStruct.makeStruct([measures, groupsToPool, contrastFieldNames, sizeFieldNames])
        summaryResults = makeStruct.makeStruct([measuresForSummary, groupsToPool, contrastFieldNames, sizeFieldNames])



        ## Do the pooling
        for group in groupsToPool:


            for subjectID in subjectIDs[group]:

                stats, correlograms = analyzeTadin.analyzeTadin(subjectID, load=True)

                for measure in measures:
                    for contrast in contrasts:
                        for size in sizes:
                            if measure == 'correlograms':
                                pooledResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)].append(correlograms['Contrast'+str(contrast)]['Size'+str(size)])
                            else:
                                pooledResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)].append(stats[measure[:-1]]['Contrast'+str(contrast)]['Size'+str(size)])


        ## Do some plotting

        groupColors = {'controls': 'black',
                       'migraine': 'red',
                       'ptha': 'blue',
                       'pooled': 'green'}

        contrastLineStyles = {'2': '--',
                              '99': '-'}

        yLims = {'peaks': [-0.025, 0.25],
                 'correlograms': [-0.025, 0.25],
                 'widths': [0, 500],
                 'lags': [250, 400]}

        measuresYLabel = {'peaks': 'Kernel Peak (r)',
                          'lags': 'Lag (ms)',
                          'widths': 'Width (ms)'}




        # Plot peaks by size

        for measure in measures:
            if measure == 'correlograms':
                test = 'yuck'
                for contrast in contrasts:
                    for size in sizes:
                        for group in groupsToPool:
                            meanCorrelogram = np.mean(pooledResults['correlograms'][group]['Contrast'+str(contrast)]['Size'+str(size)], 0)
                            if group == 'pooled':
                                test ='doNothing'
                            else:
                                plt.plot(correlograms['timebase'], meanCorrelogram, label=group, color=groupColors[group])

                            summaryResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)] = meanCorrelogram


                        plt.xlabel('Time (s)')
                        plt.ylabel('Cross Correlation')
                        plt.legend()
                        plt.ylim(yLims[measure])
                        plt.savefig(savePath + 'C'+str(contrast)+'_S'+str(size)+'_correlograms.png')
                        plt.close()
            else:
                for group in groupsToPool:
                    for contrast in contrasts:
                        meanVector = []
                        SEMVector = []
                        for size in sizes:

                            meanValue = np.mean((pooledResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)]))
                            SEMValue = np.std((pooledResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)]))/((len(pooledResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)])**0.5))

                            if size == 1.5 and contrast == 2:
                                meanVector.append(np.nan)
                                SEMVector.append(np.nan)
                            else:
                                meanVector.append(meanValue)
                                SEMVector.append(SEMValue)

                            summaryResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)] = meanValue
                            summaryResults[measure+'SEM'][group]['Contrast'+str(contrast)]['Size'+str(size)] = SEMValue


                        if group == 'pooled':
                            test='doNothing'
                        else:
                            if contrast == 99:
                                plt.errorbar(np.log(sizes), meanVector, SEMVector,
                                        color=groupColors[group],
                                        label=group,
                                        linestyle=contrastLineStyles[str(contrast)]
                                             )
                            else:
                                plt.errorbar(np.log(sizes), meanVector, SEMVector,
                                        color=groupColors[group],
                                        linestyle=contrastLineStyles[str(contrast)]
                                             )

                plt.xticks(np.log(sizes), sizes)
                plt.xlabel('Stimulus Size (degrees)')
                plt.ylabel(measuresYLabel[measure])
                plt.legend()
                plt.ylim(yLims[measure])
                plt.savefig(savePath + 'groups_CRF_'+measure+'.png')
                plt.close()

        for measure in measures:
            if measure == 'correlograms':
                test = 'yuck'
                for contrast in contrasts:
                    for size in sizes:
                        for group in groupsToPool:
                            meanCorrelogram = np.mean(pooledResults['correlograms'][group]['Contrast'+str(contrast)]['Size'+str(size)], 0)
                            if group == 'pooled':
                                test ='doNothing'
                            else:
                                plt.plot(correlograms['timebase'], meanCorrelogram, label=group, color=groupColors[group])

                            summaryResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)] = meanCorrelogram


                        plt.xlabel('Time (s)')
                        plt.ylabel('Cross Correlation')
                        plt.legend()
                        plt.ylim(yLims[measure])
                        plt.savefig(savePath + 'C'+str(contrast)+'_S'+str(size)+'_correlograms.png')
                        plt.close()
            else:
                for group in groupsToPool:
                    for contrast in contrasts:
                        meanVector = []
                        SEMVector = []
                        for size in sizes:

                            meanValue = np.mean((pooledResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)]))
                            SEMValue = np.std((pooledResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)]))/((len(pooledResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)])**0.5))

                            if size == 1.5 and contrast == 2:
                                meanVector.append(np.nan)
                                SEMVector.append(np.nan)
                            else:
                                meanVector.append(meanValue)
                                SEMVector.append(SEMValue)

                            summaryResults[measure][group]['Contrast'+str(contrast)]['Size'+str(size)] = meanValue
                            summaryResults[measure+'SEM'][group]['Contrast'+str(contrast)]['Size'+str(size)] = SEMValue



                        if contrast == 99:
                            plt.errorbar(np.log(sizes), meanVector, SEMVector,
                                    color=groupColors[group],
                                    label=group,
                                    linestyle=contrastLineStyles[str(contrast)]
                                         )
                        else:
                            plt.errorbar(np.log(sizes), meanVector, SEMVector,
                                    color=groupColors[group],
                                    linestyle=contrastLineStyles[str(contrast)]
                                         )

                    plt.xticks(np.log(sizes), sizes)
                    plt.xlabel('Stimulus Size (degrees)')
                    plt.ylabel(measuresYLabel[measure])
                    plt.legend()
                    plt.ylim(yLims[measure])
                    plt.savefig(savePath + group + '_SRFs_'+measure+'.png')
                    plt.close()


        for group in groupsToPool:
            fig, axes = plt.subplots(1, len(contrasts))

            contrastCounter = 0
            for contrast in contrasts:

                sizeCounter = 0
                for size in sizes:
                    axes[contrastCounter].plot(correlograms['timebase'], summaryResults['correlograms'][group]['Contrast'+str(contrast)]['Size'+str(size)], label=str(size), color=groupColors[group], alpha=(sizeCounter+1)/(len(sizes)+1))
                    sizeCounter = sizeCounter + 1

                axes[contrastCounter].set_ylim(yLims['correlograms'])
                axes[contrastCounter].set_xlabel('Time (s)')
                axes[contrastCounter].set_ylabel('Correlation')
                axes[contrastCounter].set_title('Contrast '+ str(contrast))
                axes[contrastCounter].legend()





                contrastCounter = contrastCounter+1

            fig.savefig(savePath + group + '_combinedCorrelograms.png')
            plt.close()

        results = {
                    'pooledResults': pooledResults,
                    'summaryResults': summaryResults,

                }


        with open(savePath + 'C' + contrastsString + '_S' + sizesString + '_pooledResults.pkl', 'wb') as f:
            pickle.dump(results, f)
        f.close()

    return summaryResults, pooledResults


#makeGroupResponse(False)