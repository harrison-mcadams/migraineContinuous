def getTrialList(trialParams, **kwargs):

    import random

    if 'demo' in kwargs:
        if kwargs['demo']:
            demo = True
    else:
        demo = False

    randomizeTrialOrder = True

    nContrastLevels = len(trialParams['contrasts'])
    nTargetSizes = len(trialParams['targetRadii_degrees'])
    nTrialRepeats = trialParams['trialRepeats']

    paramsAcrossTrials = []
    for cc in range(nContrastLevels):
        for ss in range(nTargetSizes):
            for rr in range(nTrialRepeats):
                paramsAcrossTrials.append([trialParams['contrasts'][cc], trialParams['targetRadii_degrees'][ss]])

    if randomizeTrialOrder:
        random.shuffle(paramsAcrossTrials)

    return paramsAcrossTrials