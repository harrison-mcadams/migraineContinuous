#import numpy as np

#subjectID = 'SS_1412'
#inputtedContrasts = [2, 99]

#inputtedTargetRadii = np.array([1.33, 2.33, 4, 7, 12])*0.5
#load = False
#inputtedContrasts = []
#inputtedTargetRadii = []
#comparison = 'targetXVelocities-mouseXVelocities'
#def analyzeTadin(subjectID, inputtedContrasts, inputtedTargetRadii, comparison, load):


def analyzeTadin(subjectID, **kwargs):

    import analyzeContinuous_new, getExperimentParams, glob, pickle
    import os
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sb
    import makeStruct

    experimentName = 'tadin2019Continuous'
    experimentName = 'horizontalContinuous'

    if 'inputtedContrast' in kwargs:

        inputtedContrasts = kwargs['inputtedContrast']
        inputtedTargetRadii = kwargs['inputtedTargetRadii']

    else:

        inputtedContrasts = []
        inputtedTargetRadii = []

    if 'load' in kwargs:
        load = kwargs['load']
    else:
        load = True

    if 'comparison' in kwargs:
        comparison = kwargs['comparison']
    else:
        comparison = 'targetXVelocities-mouseXVelocities'

    if inputtedContrasts == [] and inputtedTargetRadii == []:
        flexiblyDiscoverTrials = True
    else:
        flexiblyDiscoverTrials = False

    basicTrialParams = getExperimentParams.getExperimentParams(experimentName)

    # Load up an example trialParams from the session
    relevantTrialFiles = glob.glob(basicTrialParams['dataPath'] + '/' + basicTrialParams['experimentName'] + '/' + subjectID + '/**/*_raw.pkl', recursive=True)

    if flexiblyDiscoverTrials:
        contrasts = []
        targetRadii = []
        for tt in range(len(relevantTrialFiles)):
            with open(relevantTrialFiles[tt], 'rb') as f:
                trialData = pickle.load(f)
                contrasts.append(trialData['trialParams']['contrast'])
                targetRadii.append(trialData['trialParams']['targetRadius_degrees'])
    else:
        contrasts = inputtedContrasts
        targetRadii = inputtedTargetRadii
        for tt in range(len(relevantTrialFiles)):
            with open(relevantTrialFiles[tt], 'rb') as f:
                trialData = pickle.load(f)

    contrasts = list(set(contrasts))
    targetRadii = list(set(targetRadii))

    contrasts = (sorted(contrasts))
    targetRadii = (sorted(targetRadii))

    targetRadii_forSaving = targetRadii
    targetRadii_forOperating = np.array(targetRadii)
    #targetRadii = np.array(targetRadii)

    targetSizes = []
    for ss in targetRadii:
        size = ss*2
        if float(size) == int(size):
            size = int(size)

        targetSizes.append(size)

    trialParams = trialData['trialParams']
    trialParams.update({'experimentName': experimentName})
    trialParams.update({'targetSizes_degrees': targetSizes})


    savePath = basicTrialParams['analysisPath']+trialParams['experimentName']+'/meanResponses/'+subjectID+'/'

    correlationYLims = [-0.05, 0.3]

    #contrasts = [2, 99]
    #targetRadii = np.array([0.75, 1.33, 2.33, 4, 7])*0.5

    if not load:

        peaks = {'Contrast'+str(contrasts[0]): ''}
        peaksTrials = {'Contrast'+str(contrasts[0]): ''}

        lags = {'Contrast'+str(contrasts[0]): ''}
        lagsTrials = {'Contrast'+str(contrasts[0]): ''}

        widths = {'Contrast'+str(contrasts[0]): ''}
        widthsTrials = {'Contrast'+str(contrasts[0]): ''}



        correlograms = {'Contrast'+str(contrasts[0]): ''}
        correlogramTrials = {'Contrast'+str(contrasts[0]): ''}


        for cc in contrasts:



            peakPooler = []
            peaksTrialPooler = []
            lagPooler = []
            lagsTrialPooler = []
            widthPooler = []
            widthsTrialPooler = []
            correlogramPooler = []
            correlogramTrialsPooler = []


            for rr in targetRadii:

                trialParams.update({'targetRadius_degrees': rr})
                trialParams.update({'contrast': cc})

                meanCorrelations, correlationsPooled, gaussStats, gaussStatsPooled, correlationsTimebase = analyzeContinuous_new.analyzeContinuous_new(subjectID, experimentName, trialParams)
                peak = gaussStats[comparison]['peak']
                peakPooler.append(peak)
                lag = gaussStats[comparison]['lag']
                lagPooler.append(lag)
                width = gaussStats[comparison]['width']
                widthPooler.append(width)
                correlogramPooler.append(meanCorrelations[comparison])
                correlogramTrialsPooler.append(correlationsPooled)

                peaksPerTrial = []
                widthsPerTrial = []
                lagsPerTrial = []
                nTrials = len(gaussStatsPooled[comparison])
                for tt in range(nTrials):
                    peaksPerTrial.append(gaussStatsPooled[comparison][tt]['peak'])
                    widthsPerTrial.append(gaussStatsPooled[comparison][tt]['width'])
                    lagsPerTrial.append(gaussStatsPooled[comparison][tt]['lag'])


                peaksTrialPooler.append(peaksPerTrial)
                lagsTrialPooler.append(lagsPerTrial)
                widthsTrialPooler.append(widthsPerTrial)


            peaks.update({'Contrast'+str(cc): peakPooler})
            peaksTrials.update({'Contrast'+str(cc): peaksTrialPooler})
            widths.update({'Contrast'+str(cc): widthPooler})
            widthsTrials.update({'Contrast'+str(cc): widthsTrialPooler})
            lags.update({'Contrast'+str(cc): lagPooler})
            lagsTrials.update({'Contrast'+str(cc): lagsTrialPooler})


            correlograms.update({'Contrast'+str(cc): correlogramPooler})
            correlogramTrials.update({'Contrast'+str(cc): correlogramTrialsPooler})

        # Make the error bars
        peakErrors = {'Contrast'+str(contrasts[0]): ''}
        lagErrors = {'Contrast'+str(contrasts[0]): ''}
        widthErrors = {'Contrast'+str(contrasts[0]): ''}

        # Save out the timebase
        correlograms.update({'timebase': correlationsTimebase})

        for cc in range(len(contrasts)):
            SEMPooledPeaks = []
            SEMPooledLags = []
            SEMPooledWidths = []

            for rr in range(len(targetRadii)):
                nTrials = len(peaksTrials['Contrast'+str(contrasts[cc])][rr][:])
                SEMPeaks = np.std(peaksTrials['Contrast'+str(contrasts[cc])][rr][:])/(nTrials**0.5)
                SEMPooledPeaks.append(SEMPeaks)

                SEMLags = np.std(lagsTrials['Contrast'+str(contrasts[cc])][rr][:])/(nTrials**0.5)
                SEMPooledLags.append(SEMLags)

                SEMWidths = np.std(widthsTrials['Contrast'+str(contrasts[cc])][rr][:])/(nTrials**0.5)
                SEMPooledWidths.append(SEMWidths)

            peakErrors.update({'Contrast'+str(contrasts[cc]): SEMPooledPeaks})
            widthErrors.update({'Contrast'+str(contrasts[cc]): SEMPooledWidths})
            lagErrors.update({'Contrast'+str(contrasts[cc]): SEMPooledLags})

        #targetRadii = np.array(targetRadii)
        for cc in contrasts:
            plt.errorbar(np.log(np.array(targetRadii_forOperating)*2), peaks['Contrast'+str(cc)], peakErrors['Contrast'+str(cc)], label='Contrast: '+str(cc))
        #plt.errorbar(np.log(targetRadii*2), peaks['Contrast'+str(contrasts[1])], peakErrors['Contrast'+str(contrasts[1])], label='Contrast: '+str(contrasts[1]))
        plt.xticks(np.log(targetRadii_forOperating*2), targetRadii_forOperating*2)
        plt.xlabel('Stimulus Size (degrees)')
        plt.ylabel('Kernel Peak (r)')
        plt.legend()
        plt.ylim([-0.025, 0.25])
        plt.savefig(savePath + 'CRF_peaks.png')


        if not os.path.exists(basicTrialParams['analysisPath'] + '/horizontalContinuous/pooled/'):
            os.makedirs(basicTrialParams['analysisPath'] + '/horizontalContinuous/pooled/')
        plt.savefig(basicTrialParams['analysisPath'] + '/horizontalContinuous/pooled/' + subjectID + '_CRF_peaks.png')
        plt.close()

        for cc in contrasts:
            plt.errorbar(np.log(targetRadii_forOperating*2), lags['Contrast'+str(cc)], lagErrors['Contrast'+str(cc)], label='Contrast: '+str(cc))

            #plt.plot(np.log(targetRadii*2), lags['Contrast'+str(cc)], label='Contrast: '+str(cc))
            #plt.plot(np.log(targetRadii*2), lags['Contrast'+str(contrasts[1])], label='Contrast: '+str(contrasts[1]))
        plt.xticks(np.log(targetRadii_forOperating*2), targetRadii_forOperating*2)
        plt.xlabel('Stimulus Size (degrees)')
        plt.ylabel('Kernel Lag (s)')
        plt.legend()
        plt.savefig(savePath + 'CRF_lags.png')
        plt.close()

        for cc in contrasts:
            plt.errorbar(np.log(targetRadii_forOperating*2), widths['Contrast'+str(cc)], widthErrors['Contrast'+str(cc)], label='Contrast: '+str(cc))

            #plt.plot(np.log(targetRadii*2), widths['Contrast'+str(cc)], label='Contrast: '+str(cc))
        #plt.plot(np.log(targetRadii*2), widths['Contrast'+str(contrasts[1])], label='Contrast: '+str(contrasts[1]))
        plt.xticks(np.log(targetRadii_forOperating*2), targetRadii_forOperating*2)
        plt.xlabel('Stimulus Size (degrees)')
        plt.ylabel('Kernel Width (FWHM, s)')
        plt.legend()
        plt.savefig(savePath + 'CRF_widths.png')
        plt.close()


        for cc in contrasts:
            correlationPlot = plt.figure()
            for rr in range(len(targetRadii)):

                plt.plot(correlationsTimebase, correlograms['Contrast'+str(cc)][rr], label=targetSizes[rr], color='black', alpha=(rr+1)/(len(targetRadii)+1))

            plt.title('Contrast '+str(cc))
            plt.legend()
            plt.xlabel('Time (s)')
            plt.ylabel('Correlogram (r)')
            plt.savefig(savePath + 'C' + str(cc) + '_combinedCorrelograms.png')
            plt.close()


        xTicks = [0, 500, 1000, 1500, 2000, 2500, 2999]
        if comparison == 'targetVelocities-mouseVelocities':
            for cc in contrasts:

                #correlationPlot = plt.figure()
                correlationsXMatrix = []
                correlationsYMatrix = []
                correlationsCombinedMatrix = []

                for rr in range(len(targetRadii)):
                    nTrials = len(correlogramTrials['Contrast'+str(cc)][rr]['targetXVelocities-mouseXVelocities'])
                    for tt in range(nTrials):
                        correlationsXMatrix.append(np.array(correlogramTrials['Contrast'+str(cc)][rr]['targetXVelocities-mouseXVelocities'][tt]))
                        correlationsYMatrix.append(np.array(correlogramTrials['Contrast'+str(cc)][rr]['targetYVelocities-mouseYVelocities'][tt]))
                        correlationsCombinedMatrix.append((np.array(correlogramTrials['Contrast'+str(cc)][rr]['targetXVelocities-mouseXVelocities'][tt]) + np.array(
                    correlogramTrials['Contrast'+str(cc)][rr]['targetYVelocities-mouseYVelocities'][tt])) / 2)

                fig, (ax1, ax2, ax3) = plt.subplots(1, 3,
                                               sharey='row', figsize = (15,5))
                heatmapx = sb.heatmap(ax=ax1, data=correlationsXMatrix, vmin=correlationYLims[0], vmax=correlationYLims[1])
                heatmapx.set_xticks(xTicks, list(correlationsTimebase[xTicks[0:-1]])+ [2.0])
                heatmapx.set_title('X')
                yTicks = []
                for ii in range(len(targetRadii)):
                    nTrials = len(correlogramTrials['Contrast'+str(cc)][rr]['targetXVelocities-mouseXVelocities'])

                    yValue = (ii+1)*nTrials
                    ax1.plot(np.array(range(len(correlationsTimebase))), np.ones(len(correlationsTimebase))*yValue, color='black')
                    yTicks.append((ii*nTrials)+nTrials/2)
                heatmapx.set_ylabel('Target Size (degrees)')
                heatmapx.set_xlabel('Time (s)')

                heatmapy = sb.heatmap(ax=ax2, data=correlationsYMatrix, vmin=correlationYLims[0], vmax=correlationYLims[1])
                heatmapy.set_xticks(xTicks, list(correlationsTimebase[xTicks[0:-1]])+ [2.0])
                heatmapy.set_title('Y')
                for ii in range(len(targetRadii)):
                    nTrials = len(correlogramTrials['Contrast'+str(cc)][rr]['targetXVelocities-mouseXVelocities'])

                    yValue = (ii+1)*nTrials
                    ax2.plot(np.array(range(len(correlationsTimebase))), np.ones(len(correlationsTimebase))*yValue, color='black')


                heatmap = sb.heatmap(ax=ax3, data=correlationsCombinedMatrix, vmin=correlationYLims[0], vmax=correlationYLims[1])
                heatmap.set_xticks(xTicks, list(correlationsTimebase[xTicks[0:-1]])+ [2.0])
                heatmap.set_title('Combined')

                for ii in range(len(targetRadii)):
                    nTrials = len(correlogramTrials['Contrast'+str(cc)][rr]['targetXVelocities-mouseXVelocities'])

                    yValue = (ii+1)*nTrials
                    ax3.plot(np.array(range(len(correlationsTimebase))), np.ones(len(correlationsTimebase))*yValue, color='black')

                heatmapx.set_yticks(yTicks, np.array(targetRadii)*2.0)
                fig.suptitle('Contrast ' + str(cc) + '%')
                fig.savefig(savePath + 'C' + str(cc) + '_trialCorrelograms.png')
                plt.close()
        else:
            for cc in contrasts:

                # correlationPlot = plt.figure()
                correlationsMatrix = []


                for rr in range(len(targetRadii)):
                    nTrials = len(correlogramTrials['Contrast' + str(cc)][rr][comparison])
                    for tt in range(nTrials):
                        correlationsMatrix.append(
                            np.array(correlogramTrials['Contrast' + str(cc)][rr][comparison][tt]))

                ax1 = plt.axes()
                heatmapx = sb.heatmap(ax=ax1, data=correlationsMatrix, vmin=correlationYLims[0],
                                      vmax=correlationYLims[1])
                heatmapx.set_xticks(xTicks, list(correlationsTimebase[xTicks[0:-1]]) + [2.0])
                heatmapx.set_title('X')
                yTicks = []
                for ii in range(len(targetRadii)):
                    nTrials = len(correlogramTrials['Contrast' + str(cc)][rr][comparison])

                    yValue = (ii + 1) * nTrials
                    ax1.plot(np.array(range(len(correlationsTimebase))),
                             np.ones(len(correlationsTimebase)) * yValue,
                             color='black')
                    yTicks.append((ii * nTrials) + nTrials / 2)
                heatmapx.set_ylabel('Target Size (degrees)')
                heatmapx.set_xlabel('Time (s)')

                heatmapx.set_yticks(yTicks, np.array(targetRadii) * 2.0)
                plt.savefig(savePath + 'C' + str(cc) + '_trialCorrelograms.png')
                plt.close()

        # Clean up results for outputting
        contrastString_forFieldNames = []
        for contrast in contrasts:
            contrastString_forFieldNames.append('Contrast'+str(contrast))

        sizeString_forFieldNames = []
        for size in targetSizes:
            sizeString_forFieldNames.append('Size'+str(size))

        statsFieldNames = ['peak', 'peakSEM', 'width', 'widthSEM', 'lag', 'lagSEM']

        fieldsList_stats = [statsFieldNames, contrastString_forFieldNames, sizeString_forFieldNames]
        fieldsList_correlograms = [contrastString_forFieldNames, sizeString_forFieldNames]


        stats = makeStruct.makeStruct(fieldsList_stats)

        correlogramsForSaving = makeStruct.makeStruct(fieldsList_correlograms)


        for contrast in contrasts:
            sizeCounter = 0
            for size in targetSizes:
                stats['peak']['Contrast'+str(contrast)]['Size'+str(size)] = peaks['Contrast'+str(contrast)][sizeCounter]
                stats['peakSEM']['Contrast'+str(contrast)]['Size'+str(size)] = peakErrors['Contrast'+str(contrast)][sizeCounter]

                stats['lag']['Contrast'+str(contrast)]['Size'+str(size)] = lags['Contrast'+str(contrast)][sizeCounter]
                stats['lagSEM']['Contrast'+str(contrast)]['Size'+str(size)] = lagErrors['Contrast'+str(contrast)][sizeCounter]

                stats['width']['Contrast'+str(contrast)]['Size'+str(size)] = widths['Contrast'+str(contrast)][sizeCounter]
                stats['widthSEM']['Contrast'+str(contrast)]['Size'+str(size)] = widthErrors['Contrast'+str(contrast)][sizeCounter]

                correlogramsForSaving['Contrast'+str(contrast)]['Size'+str(size)] = correlograms['Contrast'+str(contrast)][sizeCounter]

                sizeCounter = sizeCounter + 1


        correlograms = correlogramsForSaving
        correlograms.update({'timebase': correlationsTimebase})


        results = {
            'stats': stats,
            'correlograms': correlograms
        }

        contrastsString = ",".join(str(x) for x in contrasts)
        sizesString = ",".join(str(x) for x in targetSizes)
        with open(savePath + 'C' + contrastsString + '_S' + sizesString + '_results.pkl', 'wb') as f:
            pickle.dump(results, f)
        f.close()


    else:



        contrastsString = ",".join(str(x) for x in contrasts)
        sizesString = ",".join(str(x) for x in targetSizes)
        with open(savePath + 'C' + contrastsString + '_S' + sizesString + '_results.pkl', 'rb') as f:
            results = pickle.load(f)

        stats = results['stats']
        correlograms = results['correlograms']


    print('oogie')

    return stats, correlograms

#analyzeTadin(subjectID, inputtedContrasts, inputtedTargetRadii, comparison, load)