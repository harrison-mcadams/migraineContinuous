import analyzeContinuous_new, getExperimentParams, glob, pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb

subjectID = 'debug'
experimentName = 'tadin2019Continuous'
flexiblyDiscoverTrials = True
inputtedContrast = []
inputtedTargetRadii = []

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

contrasts = list(set(contrasts))
targetRadii = list(set(targetRadii))

contrasts = np.array(np.sort(contrasts))
targetRadii = np.array(np.sort(targetRadii))

trialParams = trialData['trialParams']
trialParams.update({'experimentName': experimentName})

savePath = trialParams['analysisPath']+trialParams['experimentName']+'/'+subjectID+'/'
nTrials = 4

correlationYLims = [-0.05, 0.3]

#contrasts = [2, 99]
#targetRadii = np.array([0.75, 1.33, 2.33, 4, 7])*0.5

peaks = {'Contrast'+str(contrasts[0]): ''}
peaksTrials = {'Contrast'+str(contrasts[0]): ''}

lags = {'Contrast'+str(contrasts[0]): ''}
widths = {'Contrast'+str(contrasts[0]): ''}


correlograms = {'Contrast'+str(contrasts[0]): ''}
correlogramTrials = {'Contrast'+str(contrasts[0]): ''}


for cc in contrasts:



    peakPooler = []
    peaksTrialPooler = []
    lagPooler = []
    widthPooler = []
    correlogramPooler = []
    correlogramTrialsPooler = []


    for rr in targetRadii:

        trialParams.update({'targetRadius_degrees': rr})
        trialParams.update({'contrast': cc})

        meanCorrelations, correlationsPooled, gaussStats, gaussStatsPooled = analyzeContinuous_new.analyzeContinuous_new(subjectID, experimentName, trialParams)
        peak = gaussStats['targetVelocities-mouseVelocities']['peak']
        peakPooler.append(peak)
        lag = gaussStats['targetVelocities-mouseVelocities']['lag']
        lagPooler.append(lag)
        width = gaussStats['targetVelocities-mouseVelocities']['width']
        widthPooler.append(width)
        correlogramPooler.append(meanCorrelations['targetVelocities-mouseVelocities'])
        correlogramTrialsPooler.append(correlationsPooled)

        peaksPerTrial = []
        nTrials = len(gaussStatsPooled['targetVelocities-mouseVelocities'])
        for tt in range(nTrials):
            peaksPerTrial.append(gaussStatsPooled['targetVelocities-mouseVelocities'][tt]['peak'])
        peaksTrialPooler.append(peaksPerTrial)

    peaks.update({'Contrast'+str(cc): peakPooler})
    peaksTrials.update({'Contrast'+str(cc): peaksTrialPooler})
    widths.update({'Contrast'+str(cc): widthPooler})
    lags.update({'Contrast'+str(cc): lagPooler})

    correlograms.update({'Contrast'+str(cc): correlogramPooler})
    correlogramTrials.update({'Contrast'+str(cc): correlogramTrialsPooler})

# Make the error bars
peakErrors = {'Contrast'+str(contrasts[0]): ''}
for cc in range(len(contrasts)):
    SEMPooled = []
    for rr in range(len(targetRadii)):
        nTrials = len(peaksTrials['Contrast'+str(contrasts[cc])][rr][:])
        SEM = np.std(peaksTrials['Contrast'+str(contrasts[cc])][rr][:])/(nTrials**0.5)
        SEMPooled.append(SEM)

    peakErrors.update({'Contrast'+str(contrasts[cc]): SEMPooled})

for cc in contrasts:
    plt.errorbar(np.log(targetRadii*2), peaks['Contrast'+str(cc)], peakErrors['Contrast'+str(cc)], label='Contrast: '+str(cc))
#plt.errorbar(np.log(targetRadii*2), peaks['Contrast'+str(contrasts[1])], peakErrors['Contrast'+str(contrasts[1])], label='Contrast: '+str(contrasts[1]))
plt.xticks(np.log(targetRadii*2), targetRadii*2)
plt.xlabel('Stimulus Size (degrees)')
plt.ylabel('Kernel Peak (r)')
plt.legend()
plt.savefig(savePath + 'CRF_peaks.png')
plt.close()

for cc in contrasts:
    plt.plot(np.log(targetRadii*2), lags['Contrast'+str(cc)], label='Contrast: '+str(cc))
    #plt.plot(np.log(targetRadii*2), lags['Contrast'+str(contrasts[1])], label='Contrast: '+str(contrasts[1]))
plt.xticks(np.log(targetRadii*2), targetRadii*2)
plt.xlabel('Stimulus Size (degrees)')
plt.ylabel('Kernel Lag (s)')
plt.legend()
plt.savefig(savePath + 'CRF_lags.png')
plt.close()

for cc in contrasts:
    plt.plot(np.log(targetRadii*2), widths['Contrast'+str(cc)], label='Contrast: '+str(cc))
#plt.plot(np.log(targetRadii*2), widths['Contrast'+str(contrasts[1])], label='Contrast: '+str(contrasts[1]))
plt.xticks(np.log(targetRadii*2), targetRadii*2)
plt.xlabel('Stimulus Size (degrees)')
plt.ylabel('Kernel Width (FWHM, s)')
plt.legend()
plt.savefig(savePath + 'CRF_widths.png')
plt.close()

correlationsTimebase = np.array(range(-1*1000, 2*1000))/1000
for cc in contrasts:
    correlationPlot = plt.figure()
    for rr in range(len(targetRadii)):

        plt.plot(correlationsTimebase, correlograms['Contrast'+str(cc)][rr], label=targetRadii[rr], color='black', alpha=(rr+1)/(len(targetRadii)+1))

    plt.title('Contrast '+str(cc))
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Correlogram (r)')
    plt.savefig(savePath + 'C' + str(cc) + '_combinedCorrelograms.png')
    plt.close()


xTicks = [0, 500, 1000, 1500, 2000, 2500, 2999]
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



print('oogie')