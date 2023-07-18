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
    savePathRoot = os.path.expanduser('~') + '/Desktop/migraineContinuous/analysis/'
    savePath = savePathRoot + '/' + experimentName + '/' + subjectID + '/'

    samplingRate = 1/100

    ## Load the relevant trials
    dataPath = os.path.expanduser('~') + '/Desktop/migraineContinuous/data/'

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
    surrounds = []

    nans = []
    for tt in range(nTrials):
        stimulusStartTime = trialData[tt]['stimulusTimes'][0]
        stimulusEndTime = trialData[tt]['stimulusTimes'][-1]

        trialData[tt]['stimulusTimes'] = np.array(trialData[tt]['stimulusTimes']) - stimulusStartTime
        trialData[tt]['responseTimes'] = np.array(trialData[tt]['responseTimes']) - stimulusStartTime

        # Clean up the responses. 'Left' corresponds to 1, 'Right' corresponds to -1
        responseValues = []
        for ii in trialData[tt]['responseDirections']:
            if ii == 'left' or ii == 'a':
                responseValues.append(-1)
            elif ii == 'right' or ii == 'd':
                responseValues.append(1)

        trialTimebase = list(range(0, round(np.floor((stimulusEndTime-stimulusStartTime)*1/samplingRate))))
        timebases.append(trialTimebase)

        stimulusValues_resampled = []
        surroundValues_resampled = []
        responseValues_resampled = []

        nanValues = []


        for timepoint in trialTimebase:
            indexInQuestion = np.argmin(np.abs(trialData[tt]['stimulusTimes'] - timepoint*samplingRate))
            if timepoint*samplingRate < trialData[tt]['stimulusTimes'][indexInQuestion]:
                stimulusValues_resampled.append(trialData[tt]['stimulusDirections'][indexInQuestion-1])
            else:
                stimulusValues_resampled.append(trialData[tt]['stimulusDirections'][indexInQuestion])

            indexInQuestion = np.argmin(np.abs(trialData[tt]['stimulusTimes'] - timepoint*samplingRate))
            if timepoint*samplingRate < trialData[tt]['stimulusTimes'][indexInQuestion]:
                surroundValues_resampled.append(trialData[tt]['surroundDirections'][indexInQuestion-1])
            else:
                surroundValues_resampled.append(trialData[tt]['surroundDirections'][indexInQuestion])

            if timepoint*samplingRate < trialData[tt]['responseTimes'][0]:
                responseValues_resampled.append(np.nan)
                nanValues.append(timepoint)
            else:
                indexInQuestion = np.argmin(np.abs(trialData[tt]['responseTimes'] - timepoint * samplingRate))
                if timepoint * samplingRate < trialData[tt]['responseTimes'][indexInQuestion]:
                    responseValues_resampled.append(responseValues[indexInQuestion - 1])
                else:
                    responseValues_resampled.append(responseValues[indexInQuestion])

        stimuli.append((np.array(stimulusValues_resampled) + 1) / 2)
        surrounds.append((np.array(surroundValues_resampled) + 1) / 2)
        responses.append((np.array(responseValues_resampled)+1)/2)


        # Remove nan values, which correspond to timepoints prior to first response input
        responses[tt] = np.delete(responses[tt], nanValues)
        stimuli[tt] = np.delete(stimuli[tt], nanValues)
        surrounds[tt] = np.delete(surrounds[tt], nanValues)
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
            plt.plot(timebases[0][range(round(1/samplingRate))], responses[0][range(round(1/samplingRate))], label='Responses')
            plt.plot(timebases[0][range(round(1/samplingRate))], stimuli[0][range(round(1/samplingRate))], label='Stimuli')
            plt.legend()
            if not os.path.exists(savePath):
                os.makedirs(savePath)
            plt.savefig(savePath + 'SF' + str(spatialFrequency) + '_C' + str(
                contrast) + '_timeseries.png')
            plt.close()
    # For each trial, resample to a common stimulus and response timebase

    ## Cross correlation
    # Concatenate center stimuli and response vectors

    for ss in range(2):
        responseVector = []
        stimulusVector = []
        for tt in range(nTrials):
            responseVector.extend(responses[tt])
            if ss == 0:
                stimulusVector.extend(stimuli[tt])
                stimulusType = 'center'
            if ss == 1:
                stimulusVector.extend(surrounds[tt])
                stimulusType = 'surround'

        correlationSamplingRate = samplingRate
        firstTimepoint = -1
        lastTimepoint = 2 # slide 3 seconds forward, and 3 seconds backward
        correlationIndices = list(range(round(firstTimepoint*1/samplingRate), round(lastTimepoint*1/samplingRate)))

        correlations = []
        for ii in correlationIndices:


            #stimulusIndicesToDelete = (np.array(range(ii))+1)*-1
            if ii < 0:
                stimulusIndicesToDelete = np.array(range(abs(ii)))
                responseIndicesToDelete = (np.array(range(abs(ii)))+1)*-1
            elif ii>0:
                stimulusIndicesToDelete = (np.array(range(ii))+1)*-1
                responseIndicesToDelete = np.array(range(ii))
            elif ii==0:
                stimulusIndicesToDelete = []
                responseIndicesToDelete = []


            shiftedStimulus = np.delete(stimulusVector, stimulusIndicesToDelete)

            trimmedResponse = np.delete(responseVector, responseIndicesToDelete)

            corr = np.corrcoef(trimmedResponse, shiftedStimulus)
            correlations.append(corr[0,1])

        correlationTimebase = np.array(correlationIndices)*samplingRate

        time0 = np.argmin(np.abs(np.array(correlationTimebase) - 0))
        maxCorrelation = max(correlations[time0:-1], key=abs)
        maxCorrelationRounded = round(maxCorrelation, 3)
        indexOfMaxCorrelation = correlations.index(maxCorrelation)
        shift = correlationTimebase[indexOfMaxCorrelation]

        # Fit a Gaussian to cross correlogram

        def func(x, lag, width, peak):
            return visual.filters.makeGauss(x, mean=lag, sd=width, gain=peak, base=0)

        # Do the fit
        popt, pcov = curve_fit(func, correlationTimebase, correlations, p0=[shift, 0.4, maxCorrelation], bounds=([0, 0, -1], [2, 0.5, 1]))
        lag = popt[0]
        width_sigma = popt[1]
        width_fwhm = width_sigma * ((8*np.log(2))**0.5)
        peak = popt[2]
        peak_rounded = round(peak,3)
        width_fwhm_rounded = round(width_fwhm, 3)
        lag_rounded = round(lag, 3)

        y_pred = func(correlationTimebase, *popt)


        SSres = sum((np.array(correlations)-np.array(y_pred))**2)
        SStot = sum((np.array(correlations)-np.mean(correlations))**2)
        r2 = 1-SSres/SStot
        r2_rounded = round(r2, 3)


        plt.plot(correlationTimebase, correlations, label='CCG')
        plt.plot(correlationTimebase, func(correlationTimebase, *popt), label='Fit')
        plt.legend()
        plt.title('Peak: ' + str(peak_rounded) + ', Lag: ' + str(lag_rounded) + ', Width: ' + str(width_fwhm_rounded) + ', R2 = ' + str(r2_rounded))
        # Note that positive time means shifting the stimulus forward in time relative to a stationary response time series

        if not os.path.exists(savePath):
            os.makedirs(savePath)
        plt.savefig(savePath + 'SF' + str(spatialFrequency) + '_C' + str(contrast) + '_crossCorrelation_' + stimulusType + '.png')
        plt.close()
        
        if ss == 0:
            centerPeak = peak
            centerLag = lag
            centerWidth = width_fwhm
        
        elif ss == 1:
            surroundPeak = peak
            surroundLag = lag
            surroundWidth = width_fwhm


    return centerPeak, centerLag, centerWidth, surroundPeak, surroundLag, surroundWidth
    