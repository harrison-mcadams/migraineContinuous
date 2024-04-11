import analyzeTadin, random
import numpy as np
import matplotlib.pyplot as plt

subjectID = 'harry_carlynSizes_combined'


inputtedContrasts = []
#inputtedContrasts = [2, 99]
inputtedTargetRadii = []
#inputtedTargetRadii = np.array([1.33, 2.33, 4, 7, 12])*0.5

comparison = 'targetXVelocities-mouseXVelocities'
load = True

peaks, peaksTrials, contrasts, targetRadii = analyzeTadin.analyzeTadin(subjectID, inputtedContrasts, inputtedTargetRadii, comparison, load)

nBootstraps = 10000
nSimulatedTrialsPerCondition = 15


means = {'Contrast'+str(contrasts[0]): ''}
sems = {'Contrast'+str(contrasts[0]): ''}
for cc in range(len(contrasts)):

    thisContrastsMeans = []
    thisContrastsSEMs = []
    for rr in range(len(targetRadii)):

        # Data for all trials of this contrast and stimulus type
        veridicalData = peaksTrials['Contrast'+str(contrasts[cc])][rr]

        bootstrapPooler = []


        for ii in range(nBootstraps):

            bootstrapSample = random.choices(veridicalData,k=nSimulatedTrialsPerCondition)

            bootstrapPooler.append(np.mean(bootstrapSample))

            test = True

        mean = np.mean(bootstrapPooler)
        sem = np.std(bootstrapPooler)

        thisContrastsMeans.append(mean)
        thisContrastsSEMs.append(sem)

    means.update({'Contrast' + str(contrasts[cc]): thisContrastsMeans})
    sems.update({'Contrast' + str(contrasts[cc]): thisContrastsSEMs})

targetRadii = np.array(targetRadii)
for cc in contrasts:
    plt.errorbar(np.log(np.array(targetRadii) * 2), means['Contrast' + str(cc)], sems['Contrast' + str(cc)],
                 label='Contrast: ' + str(cc))
# plt.errorbar(np.log(targetRadii*2), peaks['Contrast'+str(contrasts[1])], peakErrors['Contrast'+str(contrasts[1])], label='Contrast: '+str(contrasts[1]))
plt.xticks(np.log(targetRadii * 2), targetRadii * 2)
plt.xlabel('Stimulus Size (degrees)')
plt.ylabel('Kernel Peak (r, +/- SEM)')
plt.legend()
plt.ylim(0.055, 0.24)
plt.savefig('/Users/harrisonmcadams/Desktop/migraineContinuous/analysis/tadin2019Continuous/harry_carlynSizes_combined/noiseSimulation_N=' + str(nSimulatedTrialsPerCondition)+'.png')
plt.close()



debug = True