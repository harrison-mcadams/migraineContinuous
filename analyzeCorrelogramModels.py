import analyzeTadin
import fitCorrelogram
import getExperimentParams
import os
import makeSubjectList
import makeStruct


import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

savePathRoot = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/analysis/'
savePath = savePathRoot + '/' + 'horizontalContinuous' + '/meanResponses/modeling/'

contrasts = [2, 99]
sizes = [1.5, 3, 6, 12]
load = False

groups = ['controls', 'migraine', 'ptha']
subjectIDs = makeSubjectList.makeSubjectList()




modelTypes = ['gamma', 'gaussian', 'logGaussian']

R2s = makeStruct.makeStruct([modelTypes])

skipC2S15 = True
counter = 1
fitsToInvestigate = []
for group in groups:
    for subjectID in subjectIDs[group]:

        stats, correlograms = analyzeTadin.analyzeTadin(subjectID, load=load)

        for contrast in contrasts:
            for size in sizes:
                for modelType in modelTypes:

                    saveName = savePath + subjectID + '_C' + str(contrast) + '_S' + str(size) + '_' + modelType + '.png'
                    fitStats = fitCorrelogram.fitCorrelogram(correlograms['Contrast' + str(contrast)]['Size' + str(size)], correlograms['timebase'],
                                        saveName, modelType=modelType)

                    if skipC2S15:
                        if contrast == 2 and size == 1.5:
                            # skipping
                            test='dumb'
                        else:

                            R2s[modelType].append(fitStats['R2'])



                    else:

                        R2s[modelType].append(fitStats['R2'])
                if counter > 1:
                    if R2s['gaussian'][-1] > R2s['gamma'][-1] or R2s['logGaussian'][-1] > R2s['gamma'][-1]:
                        fitsToInvestigate.append(subjectID + '_C' + str(contrast) + '_S' + str(size))
                counter = counter + 1
# Sample data (replace with your actual arrays)
array1 = R2s['gamma']
array2 = R2s['gaussian']
array3 = R2s['logGaussian']

# Create a DataFrame with labels for clarity
data = pd.DataFrame({
    "Model Type": ["Gamma"] * len(array1) + ["Gaussian"] * len(array2) + ["Log-Gaussian"] * len(array3),
    "R2": array1 + array2 + array3
})

# Create a beeswarm plot
sns.boxplot(x = "Model Type", y = "R2", showmeans=True, data=data, boxprops={'fill': None})

sns.swarmplot(x = "Model Type", y = "R2", data=data)


# Show the plot
plt.title('Medians: Gamma = ' + str(round(np.median(R2s['gamma']),3)) + ', Gaussian = ' + str(round(np.median(R2s['gaussian']),3)) + ', LogGaussian = ' + str(round(np.median(R2s['logGaussian']),3)))
#plt.show()

if skipC2S15:
    saveSuffix = '_skippedC2S15'
else:
    saveSuffix = ''
plt.savefig(savePath+'modelComparison' + saveSuffix + '.png')


print(fitsToInvestigate)

