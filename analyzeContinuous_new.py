def analyzeContinuous_new(subjectID, experimentName, trialParams):

    ## Find the data
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

    trials = 'all'

    samplingRate = 1/1000

    dataPath = os.path.expanduser('~') + '/Desktop/migraineContinuous/data/'

    # Find the trials

    if experimentName == 'tadin2019Continuous':
        relevantTrialFiles = glob.glob(dataPath + '/' + experimentName + '/' + subjectID + '/**/*S' + str(trialParams['targetRadius_degrees']) + '_C' + str(trialParams['contrast']) + '_raw.pkl', recursive=True)
        eventNames = ['mouseYVelocities', 'targetXVelocities', 'targetYVelocities', 'mouseXs', 'mouseYs', 'targetXs', 'targetYs', 'mouseXVelocities']
        eventTimeNames = ['frameTimes', 'frameTimes', 'frameTimes', 'frameTimes', 'frameTimes', 'frameTimes', 'frameTimes', 'frameTimes']
        trialParamsOfInterest = ['targetRadius_degrees', 'contrast']
        trialDescriptor = 'S'+str(trialParams['targetRadius_degrees'])+'_C'+str(trialParams['contrast'])
    else:
        relevantTrialFiles = glob.glob(dataPath + '/' + experimentName + '/' + subjectID + '/**/*SF' + str(trialParams['spatialFrequency']) + '_C' + str(trialParams['gaborContrast']) + '_raw.pkl', recursive=True)
        eventNames = ['responseDirections', 'surroundDirections', 'stimulusDirections']
        eventTimeNames = ['responseTimes', 'stimulusTimes', 'stimulusTimes']


    if trials == 'all':
        nTrials = len(relevantTrialFiles)
        trialListForLoops = range(nTrials)
    else:
        trialListForLoops = np.array(trials) - 1
        nTrials = len(trials)

    # Load them into memory
    trialData = []
    for tt in trialListForLoops:
        with open(relevantTrialFiles[tt], 'rb') as f:
            trialData.append(pickle.load(f))

    def resampleData(eventTimes, eventValues, samplingRate):


        stimulusStartTime = eventTimes[0]
        stimulusEndTime = eventTimes[-1]

        trialTimebase = list(range(0, int(np.floor((stimulusEndTime)*1/samplingRate))))

        resampledValues = []
        for timepoint in trialTimebase:

            if timepoint*samplingRate < eventTimes[0]:
                resampledValues.append(np.nan)
            else:

                indexInQuestion = np.argmin(np.abs(np.array(eventTimes) - timepoint*samplingRate))
                if timepoint*samplingRate < eventTimes[indexInQuestion]:
                    resampledValues.append(eventValues[indexInQuestion-1])
                else:
                    resampledValues.append(eventValues[indexInQuestion])

        resampledTimebase = np.array(trialTimebase)*samplingRate

        return resampledValues, resampledTimebase




    resampledTrialData = []
    for tt in range(nTrials):
        resampledTrialData.append({eventNames[0]: ''})
        for ee in range(len(eventNames)):

            eventTimes = trialData[tt][eventTimeNames[ee]]
            eventValues = trialData[tt][eventNames[ee]]

            eventResponses, eventTimebase = resampleData(eventTimes, eventValues, samplingRate)

            # trim nans
            nans = np.where(np.isnan(eventResponses))
            nans = nans[0]

            eventResponses = np.delete(eventResponses, nans)
            eventTimebase = np.delete(eventTimebase, nans)

            resampledTrialData[tt].update({eventNames[ee]: eventResponses})
            resampledTrialData[tt].update({'timebase': eventTimebase})


    ## Perform the cross correlation
    if trialParams['experimentName'] == 'tadin2019Continuous':
        stimulusNames = ['targetXVelocities', 'targetYVelocities']
        responseNames = ['mouseXVelocities', 'mouseYVelocities']
    else:
        stimulusNames = ['stimulusDirections', 'surroundDirections']
        responseNames = ['responseDirections', 'responseDirections']

    def performCrossCorrelation(stimulusVector, responseVector, timebase):
        firstTimepoint = -1
        lastTimepoint = 2

        useNumpy = True

        if useNumpy:
            a = responseVector
            b = stimulusVector
            a = (a - np.mean(a)) / (np.std(a) * len(a))
            b = (b - np.mean(b)) / (np.std(b))
            correlations = np.correlate(a, b, 'full')

            middleIndex = int(np.floor(len(correlations) / 2))

            correlations = correlations[
                           int(middleIndex + firstTimepoint / samplingRate):int(middleIndex + lastTimepoint / samplingRate)]
            correlations = list(correlations)

            correlationIndices = list(range(round(firstTimepoint * 1 / samplingRate), round(lastTimepoint * 1 / samplingRate)))
            correlationTimebase = np.array(correlationIndices)*samplingRate
        else:
            correlationIndices = list(range(round(firstTimepoint * 1 / samplingRate), round(lastTimepoint * 1 / samplingRate)))
            correlationTimebase = np.array(correlationIndices)*samplingRate
            correlations = []
            for ii in correlationIndices:

                # stimulusIndicesToDelete = (np.array(range(ii))+1)*-1
                if ii < 0:
                    stimulusIndicesToDelete = np.array(range(abs(ii)))
                    responseIndicesToDelete = (np.array(range(abs(ii))) + 1) * -1
                elif ii > 0:
                    stimulusIndicesToDelete = (np.array(range(ii)) + 1) * -1
                    responseIndicesToDelete = np.array(range(ii))
                elif ii == 0:
                    stimulusIndicesToDelete = []
                    responseIndicesToDelete = []

                shiftedStimulus = np.delete(stimulusVector, stimulusIndicesToDelete)

                trimmedResponse = np.delete(responseVector, responseIndicesToDelete)

                corr = np.corrcoef(trimmedResponse, shiftedStimulus)
                correlations.append(corr[0, 1])

        return correlations, correlationTimebase

    performTrialwise = True

    if performTrialwise:

        correlationsPooled = {stimulusNames[1]+'-'+responseNames[1]: ''}
        meanCorrelations = {stimulusNames[1]+'-'+responseNames[1]: ''}
        for cc in range(len(stimulusNames)):
            correlationsByTrial = []


            for tt in range(nTrials):

                stimulusVector = resampledTrialData[tt][stimulusNames[cc]]
                responseVector = resampledTrialData[tt][responseNames[cc]]
                timebase = resampledTrialData[tt]['timebase']

                #stimulusVector = np.diff(trialData[tt][stimulusNames[cc]])
                #responseVector = np.diff(trialData[tt][responseNames[cc]])

                #stimulusVector = np.diff(resampledTrialData[tt][stimulusNames[cc]])
                #responseVector = np.diff(resampledTrialData[tt][responseNames[cc]])

                correlations, correlationTimebase = performCrossCorrelation(stimulusVector, responseVector, timebase)
                correlationsByTrial.append(correlations)
            correlationsPooled.update({stimulusNames[cc]+'-'+responseNames[cc]: correlationsByTrial})

            # Average across trials


            #summedResponse = np.zeros(len(correlationsPooled[stimulusNames[cc] + '-' + responseNames[cc]][tt]))
            combinedResponse = []
            for tt in range(nTrials):
                #summedResponse = correlationsPooled[stimulusNames[cc] + '-' + responseNames[cc]][tt] + summedResponse
                combinedResponse.append(np.array(correlationsPooled[stimulusNames[cc] + '-' + responseNames[cc]][tt]))
            #meanResponse = np.array(summedResponse)/nTrials
            meanResponse = np.nanmean(np.array(combinedResponse), 0)
            meanCorrelations.update({stimulusNames[cc] + '-' + responseNames[cc]: meanResponse})
        if trialParams['experimentName'] == 'tadin2019Continuous':
            meanCorrelations.update({'targetVelocities-mouseVelocities': (meanCorrelations['targetXVelocities-mouseXVelocities'] + meanCorrelations['targetYVelocities-mouseYVelocities'])/2})

    ## Fit the cross correlation
    def fitGaussian(correlogram, correlationTimebase, stimulusName, responseName, saveSuffix):
        correlogram = list(correlogram)
        time0 = np.argmin(np.abs(np.array(correlationTimebase) - 0))
        maxCorrelation = max(correlogram[time0:-1], key=abs)
        maxCorrelationRounded = round(maxCorrelation, 3)
        indexOfMaxCorrelation = correlogram.index(maxCorrelation)
        shift = correlationTimebase[indexOfMaxCorrelation]

        # Fit a Gaussian to cross correlogram

        def func(x, lag, width, peak):
            return visual.filters.makeGauss(x, mean=lag, sd=width, gain=peak, base=0)

        # Do the fit
        popt, pcov = curve_fit(func, correlationTimebase, correlogram, p0=[shift, 0.4, maxCorrelation],
                               bounds=([0, 0, -1], [2, 0.5, 1]))
        lag = popt[0]
        width_sigma = popt[1]
        width_fwhm = width_sigma * ((8 * np.log(2)) ** 0.5)
        peak = popt[2]
        peak_rounded = round(peak, 3)
        width_fwhm_rounded = round(width_fwhm, 3)
        lag_rounded = round(lag, 3)

        y_pred = func(correlationTimebase, *popt)

        SSres = sum((np.array(correlogram) - np.array(y_pred)) ** 2)
        SStot = sum((np.array(correlogram) - np.mean(correlogram)) ** 2)
        r2 = 1 - SSres / SStot
        r2_rounded = round(r2, 3)

        fitStats= {'peak': peak}
        fitStats.update({'lag': lag})
        fitStats.update({'width': width_fwhm})
        fitStats.update({'R2': r2})

        plt.plot(correlationTimebase, correlogram, label='CCG')
        plt.plot(correlationTimebase, func(correlationTimebase, *popt), label='Fit')
        plt.legend()
        plt.title('Peak: ' + str(peak_rounded) + ', Lag: ' + str(lag_rounded) + ', Width: ' + str(
            width_fwhm_rounded) + ', R2 = ' + str(r2_rounded))
        # Note that positive time means shifting the stimulus forward in time relative to a stationary response time series

        if not os.path.exists(savePath):
            os.makedirs(savePath)
        plt.savefig(savePath + trialDescriptor + '_crossCorrelation_' + stimulusName + '-' + responseName + saveSuffix + '.png')
        plt.close()

        return fitStats

    if performTrialwise:

        gaussStats = {stimulusNames[1] + '-' + responseNames[1]: ''}
        gaussStatsPooled = {stimulusNames[1] + '-' + responseNames[1]: ''}

        for cc in range(len(stimulusNames)):

            fitStats_perComparison = []
            saveSuffix = ''
            correlogram = meanCorrelations[stimulusNames[cc] + '-' + responseNames[cc]]

            fitStats_perComparison = fitGaussian(correlogram, correlationTimebase, stimulusNames[cc], responseNames[cc], saveSuffix)

            gaussStats.update({stimulusNames[cc] + '-' + responseNames[cc]: fitStats_perComparison})

            fitStats_pooledAcrossTrials = []

            for tt in range(nTrials):
                correlogram = correlationsPooled[stimulusNames[cc] + '-' + responseNames[cc]][tt]

                fitStats_perTrial = fitGaussian(correlogram, correlationTimebase, stimulusNames[cc],
                                                     responseNames[cc], '_trial'+str(tt+1))
                fitStats_pooledAcrossTrials.append(fitStats_perTrial)
            gaussStatsPooled.update({stimulusNames[cc] + '-' + responseNames[cc]: fitStats_pooledAcrossTrials})

        gaussStatsPooled.update({stimulusNames[cc] + '-' + responseNames[cc]: fitStats_pooledAcrossTrials})

        if trialParams['experimentName'] == 'tadin2019Continuous':
            correlogram = (meanCorrelations['targetXVelocities-mouseXVelocities'] + meanCorrelations['targetYVelocities-mouseYVelocities'])/2
            saveSuffix = ''
            stimulusName = 'targetVelocities'
            responseName = 'mouseVelocities'

            fitStats_perComparison = fitGaussian(correlogram, correlationTimebase, stimulusName, responseName, saveSuffix)
            gaussStats.update({stimulusName+'-'+responseName: fitStats_perComparison})

            fitStats_pooledAcrossTrials = []
            for tt in range(nTrials):
                correlogram = (np.array(correlationsPooled['targetXVelocities-mouseXVelocities'][tt])+np.array(correlationsPooled['targetYVelocities-mouseYVelocities'][tt]))/2

                fitStats_perTrial = fitGaussian(correlogram, correlationTimebase, 'targetVelocities',
                                                     'mouseVelocities', '_trial'+str(tt+1))

                fitStats_pooledAcrossTrials.append(fitStats_perTrial)

            gaussStatsPooled.update({'targetVelocities-mouseVelocities': fitStats_pooledAcrossTrials})


    return meanCorrelations, correlationsPooled, gaussStats, gaussStatsPooled

