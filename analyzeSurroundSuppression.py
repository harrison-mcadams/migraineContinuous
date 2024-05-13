import fitSurroundSuppression
import makeSubjectList
import makeStruct
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

summaryStatistic = 'lags'
normalize = True

pooledFitParams = fitSurroundSuppression.fitSurroundSuppression('pooled', skipC2S15=True, summaryStatistic=summaryStatistic, normalize=normalize)

paramsToLock = ['R0', 'criterion', 'ni', 'ne', 'c50i', 'c50e']
#paramsToLock = ['R0', 'criterion']


params = makeStruct.makeStruct([paramsToLock])

for param in paramsToLock:
    params[param] = [pooledFitParams[param], pooledFitParams[param], pooledFitParams[param]]


#fitSurroundSuppression.fitSurroundSuppression('SS_1423', skipC2S15=True, summaryStatistic='lags', params=params, debug=True)
subjectIDs = makeSubjectList.makeSubjectList(makePooled=True)

groups = ['controls', 'ptha', 'migraine']
statsToPlot = ['Ae', 'Ai', 'alpha', 'beta', 'beta:alpha', 'r2', 'Ai:Ae']

pooledFitParams = makeStruct.makeStruct([groups, statsToPlot])

for group in groups:
    groupFitParams = fitSurroundSuppression.fitSurroundSuppression(group, skipC2S15=True, summaryStatistic=summaryStatistic, params=params, normalize=normalize)

for subjectID in subjectIDs['pooled']:
    subjectFitParams = fitSurroundSuppression.fitSurroundSuppression(subjectID, skipC2S15=True, summaryStatistic=summaryStatistic, params=params, normalize=normalize)
    #subjectFitParams = fitSurroundSuppression.fitSurroundSuppression(subjectID, skipC2S15=True, summaryStatistic=summaryStatistic)


    # Identify the group
    for potentialGroup in groups:
        if subjectID in subjectIDs[potentialGroup]:

            subjectGroup = potentialGroup

    for stat in statsToPlot:

        if stat == 'beta:alpha':

            statToStash = subjectFitParams['beta']/subjectFitParams['alpha']

        elif stat == 'Ai:Ae':
            statToStash = subjectFitParams['Ai'] / subjectFitParams['Ae']

        else:
            statToStash = subjectFitParams[stat]

        pooledFitParams[subjectGroup][stat].append(statToStash)

for stat in statsToPlot:
    # Sample data (replace with your actual arrays)
    array1 = pooledFitParams['controls'][stat]
    array2 = pooledFitParams['migraine'][stat]
    array3 = pooledFitParams['ptha'][stat]

    # Create a DataFrame with labels for clarity
    data = pd.DataFrame({
        "Group": ["Controls"] * len(array1) + ["Migraine"] * len(array2) + ["PTHA"] * len(array3),
        stat: array1 + array2 + array3
    })

    # Create a beeswarm plot
    sns.boxplot(x="Group", y=stat, showmeans=True, data=data, boxprops={'fill': None})

    sns.swarmplot(x="Group", y=stat, data=data)

    plt.title('Medians: Controls = '+str(round(np.median(pooledFitParams['controls'][stat]),3))+', Migraine = '+str(round(np.median(pooledFitParams['migraine'][stat]),3))+', PTHA = '+str(round(np.median(pooledFitParams['ptha'][stat]),3)))

    savePathRoot = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/analysis/'
    savePath = savePathRoot + '/' + 'horizontalContinuous' + '/modelFits/' + summaryStatistic + '/'
    plt.savefig(savePath + 'groups_' + stat + '.png')
    plt.close()

    # Show the plot



test='testytest'