def analyzeContinuous(subjectID, experimentName, contrast, spatialFrequency):

    import glob
    import pickle
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    from psychopy import visual
    from scipy.optimize import curve_fit


    ## Establish analysis parameters
    debugPlotting = False
    savePathRoot = '/Users/harrisonmcadams/Desktop/migraineContinuous/analysis/'


    samplingRate = 1/1000

    ## Load the relevant trials
    dataPath = '/Users/harrisonmcadams/Desktop/migraineContinuous/data/'

    # Find the trials
    relevantTrialFiles = glob.glob(dataPath + '/' + experimentName + '/' + subjectID + '/**/*SF' + str(spatialFrequency) + '_C' + str(contrast) + '_raw.pkl', recursive=True)

    nTrials = len(relevantTrialFiles)

    # Load them into memory
    trialData = []
    for tt in range(nTrials):
        with open(relevantTrialFiles[tt], 'rb') as f:
            trialData.append(pickle.load(f))

    ## Assemble data
    # Remove extra datapoints. That is, responses that came before or after the stimulus started and ended.
    timebases = []
    responses = []
    stimuli = []

    nans = []
    for tt in range(nTrials):
        stimulusStartTime = trialData[tt]['stimulusTimes'][0]
        stimulusEndTime = trialData[tt]['stimulusTimes'][-1]

        trialData[tt]['stimulusTimes'] = np.array(trialData[tt]['stimulusTimes']) - stimulusStartTime
        trialData[tt]['responseTimes'] = np.array(trialData[tt]['responseTimes']) - stimulusStartTime

        # Clean up the responses. 'Left' corresponds to 1, 'Right' corresponds to -1
        responseValues = []
        for ii in trialData[tt]['responseDirections']:
            if ii == 'left':
                responseValues.append(-1)
            elif ii == 'right':
                responseValues.append(1)

        trialTimebase = list(range(0, round(np.floor((stimulusEndTime-stimulusStartTime)*1/samplingRate))))
        timebases.append(trialTimebase)

        stimulusIndex = 0
        responseIndex = 0

        stimulusValues_resampled = []
        for timepoint in trialTimebase:
            if stimulusIndex >= len(trialData[tt]['stimulusTimes']) - 1:
                stimulusValues_resampled.append(trialData[tt]['stimulusDirections'][-1])
            else:
                if timepoint/1000 >= trialData[tt]['stimulusTimes'][stimulusIndex] and timepoint/1000 < trialData[tt]['stimulusTimes'][stimulusIndex+1]:
                    stimulusValues_resampled.append(trialData[tt]['stimulusDirections'][stimulusIndex])
                elif timepoint/1000 >= trialData[tt]['stimulusTimes'][stimulusIndex + 1]:
                    stimulusValues_resampled.append(trialData[tt]['stimulusDirections'][stimulusIndex+1])

                    stimulusIndex = stimulusIndex + 1
        #stimuli.append(stimulusValues_resampled)
        stimuli.append((np.array(stimulusValues_resampled) + 1) / 2)

        nanValues = []
        responseValues_resampled = []
        for timepoint in trialTimebase:
            if responseIndex >= len(trialData[tt]['responseTimes']) - 1:
                responseValues_resampled.append(responseValues[-1])
            else:
                if timepoint/1000 >= trialData[tt]['responseTimes'][responseIndex] and timepoint/1000 < trialData[tt]['responseTimes'][responseIndex+1]:
                    responseValues_resampled.append(responseValues[responseIndex])
                elif timepoint/1000 >= trialData[tt]['responseTimes'][responseIndex + 1]:
                    responseValues_resampled.append(responseValues[responseIndex+1])
                    responseIndex = responseIndex + 1
                else:
                    responseValues_resampled.append(np.nan)
                    nanValues.append(timepoint)


        #responses.append(responseValues_resampled)
        responses.append((np.array(responseValues_resampled)+1)/2)


        # Remove nan values, which correspond to timepoints prior to first response input
        responses[tt] = np.delete(responses[tt], nanValues)
        stimuli[tt] = np.delete(stimuli[tt], nanValues)
        timebases[tt] = np.delete(timebases[tt], nanValues)


        #for nn in reversed(nanValues):
        #    del responses[tt][nn]
        #    del stimuli[tt][nn]
        #    del timebases[tt][nn]

    if debugPlotting:


        separatePlots = False
        if separatePlots:
            f = plt.figure(1)
            plt.plot(timebases[0], responses[0])
            plt.title('Responses')
            f.show()

            g = plt.figure(2)
            plt.plot(timebases[0], stimuli[0])
            plt.title('Stimuli')
            g.show()
        else:
            plt.plot(timebases[0], responses[0], label='Responses')
            plt.plot(timebases[0], stimuli[0], label='Stimuli')
            plt.legend()
    # For each trial, resample to a common stimulus and response timebase

    ## Cross correlation
    # Cocatenate stimuli and response vectors
    responseVector = []
    stimulusVector = []
    for tt in range(nTrials):
        responseVector.extend(responses[tt])
        stimulusVector.extend(stimuli[tt])

    correlationSamplingRate = 1/1000
    slidingDistance = 3 # slide 3 seconds forward, and 3 seconds backward
    correlationIndices = list(range(round(-slidingDistance*1/samplingRate), round(slidingDistance*1/samplingRate)))

    correlations = []
    for ii in correlationIndices:


        #stimulusIndicesToDelete = (np.array(range(ii))+1)*-1
        if ii < 0:
            stimulusIndicesToDelete = np.array(range(abs(ii)))
            responseIndicesToDelete = (np.array(range(abs(ii)))+1)*-1
        elif ii>0:
            stimulusIndicesToDelete = (np.array(range(ii))+1)*-1
            responseIndicesToDelete = np.array(range(ii))
        elif ii>0:
            stimulusIndicesToDelete = []
            responseIndicesToDelete = []


        shiftedStimulus = np.delete(stimulusVector, stimulusIndicesToDelete)

        trimmedResponse = np.delete(responseVector, responseIndicesToDelete)

        corr = np.corrcoef(trimmedResponse, shiftedStimulus)
        correlations.append(corr[0,1])

    correlationTimebase = np.array(correlationIndices)*samplingRate


    maxCorrelation = max(correlations)
    maxCorrelationRounded = round(maxCorrelation, 3)
    indexOfMaxCorrelation = correlations.index(maxCorrelation)
    shift = correlationTimebase[indexOfMaxCorrelation]

    # Fit a Gaussian to cross correlogram

    def func(x, lag, width, peak):
        return visual.filters.makeGauss(x, mean=lag, sd=width, gain=peak, base=0)

    popt, pcov = curve_fit(func, correlationTimebase, correlations)

    plt.plot(correlationTimebase, correlations)
    plt.plot(correlationTimebase, func(correlationTimebase, *popt))
    plt.title('Maximum correlation: ' + str(maxCorrelationRounded) + ' at ' + str(shift) + ' s')
    # Note that positive time means shifting the stimulus forward in time relative to a stationary response time series

    savePath = savePathRoot + '/' + experimentName + '/' + subjectID + '/'
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    plt.savefig(savePath + 'SF' + str(spatialFrequency) + '_C' + str(contrast) + '_crossCorrelation.png')
    plt.close()

    corr = np.corrcoef(responses[0], stimuli[0])


    print('yay')