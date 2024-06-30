def analyzeKalman(subjectID):
    import pickle, getExperimentParams, glob, simulateKalman, maximizeLikelihood, findR, makeStruct


    experimentName = 'horizontalContinuous'

    basicTrialParams = getExperimentParams.getExperimentParams(experimentName)

    # Load up an example trialParams from the session
    relevantTrialFiles = glob.glob \
        (basicTrialParams['dataPath'] + '/' + basicTrialParams['experimentName'] + '/' + subjectID + '/**/*_raw.pkl', recursive=True)


    contrasts = [2, 99]
    sizes = [1.5, 3, 6, 12]

    contrastFieldNames = []
    for contrast in contrasts:
        contrastFieldNames.append('Contrast'+str(contrast))

    sizeFieldNames = []
    for size in sizes:
        sizeFieldNames.append('Size'+str(size))

    trialData = []
    for tt in range(len(relevantTrialFiles)):
        with open(relevantTrialFiles[tt], 'rb') as f:
            trialData.append(pickle.load(f))

    Rs = makeStruct.makeStruct([contrastFieldNames, sizeFieldNames])

    # Loop over all trials
    for tt in range(len(relevantTrialFiles)):

        # Grab the data
        x = trialData[tt]['targetXs']
        x_hat = trialData[tt]['mouseXs']

        # Grab some info about the trials
        contrast = trialData[tt]['trialParams']['contrast']
        size = trialData[tt]['trialParams']['targetRadius_degrees']*2

        if size > 1.5:
            size = f"{size:.0f}"

        # Perform the fitting to extract R for the trial

        #maximizeLikelihood.maximizeLikelihood(x, x_hat)
        R = findR.findR(x, x_hat)

        Rs['Contrast'+str(contrast)]['Size'+str(size)].append(R)

        print('done one loop iteration')








    print('test')

analyzeKalman('SS_1074')