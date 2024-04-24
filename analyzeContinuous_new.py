def analyzeContinuous_new(subjectID, experimentName, trialParams):

    ## Find the data
    import glob
    import pickle
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    from psychopy import visual
    from scipy.optimize import curve_fit
    import fitGaussian

    ## Establish analysis parameters
    debugPlotting = False
    savePathRoot = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/analysis/'
    savePath = savePathRoot + '/' + experimentName + '/' + subjectID + '/'

    trials = 'all'

    samplingRate = 1/1000

    dataPath = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/data/'

    # Find the trials

    if experimentName == 'horizontalContinuous':
        relevantTrialFiles = glob.glob(dataPath + '/' + experimentName + '/' + subjectID + '/**/*S' + str(trialParams['targetRadius_degrees']) + '_C' + str(trialParams['contrast']) + '_raw.pkl', recursive=True)
        eventNames = ['mouseYVelocities', 'targetXVelocities', 'targetYVelocities', 'mouseXs', 'mouseYs', 'targetXs', 'targetYs', 'mouseXVelocities']
        eventTimeNames = ['frameTimes', 'frameTimes', 'frameTimes', 'frameTimes', 'frameTimes', 'frameTimes', 'frameTimes', 'frameTimes']
        trialParamsOfInterest = ['targetRadius_degrees', 'contrast']
        trialDescriptor = 'S'+str(trialParams['targetRadius_degrees'])+'_C'+str(trialParams['contrast'])
        oneDMotion = True
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
    if trialParams['experimentName'] == 'tadin2019Continuous' or trialParams['experimentName'] == 'horizontalContinuous':
        if oneDMotion:
            stimulusNames = ['targetXVelocities']
            responseNames = ['mouseXVelocities']
            combineXY = False
        else:
            stimulusNames = ['targetXVelocities', 'targetYVelocities']
            responseNames = ['mouseXVelocities', 'mouseYVelocities']
            combineXY = True
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

        correlationsPooled = {stimulusNames[0]+'-'+responseNames[0]: ''}
        meanCorrelations = {stimulusNames[0]+'-'+responseNames[0]: ''}
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
        if combineXY:
            meanCorrelations.update({'targetVelocities-mouseVelocities': (meanCorrelations['targetXVelocities-mouseXVelocities'] + meanCorrelations['targetYVelocities-mouseYVelocities'])/2})



    if performTrialwise:

        gaussStats = {stimulusNames[0] + '-' + responseNames[0]: ''}
        gaussStatsPooled = {stimulusNames[0] + '-' + responseNames[0]: ''}

        for cc in range(len(stimulusNames)):

            fitStats_perComparison = []
            saveSuffix = ''
            correlogram = meanCorrelations[stimulusNames[cc] + '-' + responseNames[cc]]

            fitStats_perComparison = fitGaussian.fitGaussian(correlogram, correlationTimebase, stimulusNames[cc], responseNames[cc], saveSuffix, savePath, trialDescriptor)

            gaussStats.update({stimulusNames[cc] + '-' + responseNames[cc]: fitStats_perComparison})

            fitStats_pooledAcrossTrials = []

            for tt in range(nTrials):
                correlogram = correlationsPooled[stimulusNames[cc] + '-' + responseNames[cc]][tt]

                fitStats_perTrial = fitGaussian.fitGaussian(correlogram, correlationTimebase, stimulusNames[cc],
                                                     responseNames[cc], '_trial'+str(tt+1), savePath, trialDescriptor)
                fitStats_pooledAcrossTrials.append(fitStats_perTrial)
            gaussStatsPooled.update({stimulusNames[cc] + '-' + responseNames[cc]: fitStats_pooledAcrossTrials})

        gaussStatsPooled.update({stimulusNames[cc] + '-' + responseNames[cc]: fitStats_pooledAcrossTrials})

        if combineXY:
            if trialParams['experimentName'] == 'tadin2019Continuous':
                correlogram = (meanCorrelations['targetXVelocities-mouseXVelocities'] + meanCorrelations['targetYVelocities-mouseYVelocities'])/2
                saveSuffix = ''
                stimulusName = 'targetVelocities'
                responseName = 'mouseVelocities'

                fitStats_perComparison = fitGaussian.fitGaussian(correlogram, correlationTimebase, stimulusName, responseName, saveSuffix, savePath, trialDescriptor)
                gaussStats.update({stimulusName+'-'+responseName: fitStats_perComparison})

                fitStats_pooledAcrossTrials = []
                for tt in range(nTrials):
                    correlogram = (np.array(correlationsPooled['targetXVelocities-mouseXVelocities'][tt])+np.array(correlationsPooled['targetYVelocities-mouseYVelocities'][tt]))/2

                    fitStats_perTrial = fitGaussian.fitGaussian(correlogram, correlationTimebase, 'targetVelocities',
                                                         'mouseVelocities', '_trial'+str(tt+1), savePath, trialDescriptor)

                    fitStats_pooledAcrossTrials.append(fitStats_perTrial)

                gaussStatsPooled.update({'targetVelocities-mouseVelocities': fitStats_pooledAcrossTrials})


    return meanCorrelations, correlationsPooled, gaussStats, gaussStatsPooled








