

#subjectID = 'horizontalPilot_S1.25-20_combined'
#sizes = [0.625, 1.25, 2.5, 5.0, 10.0]
#contrasts = [2,99]
#comparison = 'targetXVelocities-mouseXVelocities'

#load = True

#peaks, contrasts, targetRadii = analyzeTadin.analyzeTadin(subjectID, contrasts, sizes, comparison, load)


#sizes = np.array(np.array(range(8000))/1000)
#peaks = np.array([[10, 20, 10], [20, 30, 20]])
#contrasts = np.array([0.07])

#peaks = {'Contrast0.99': ''}
#peaks.update({'Contrast0.99': np.array([0.18234518105358205, 0.20264061079696338, 0.1981082847585681, 0.18080599608687076, 0.15722726992694327, 0.16269456002947744, 0.14312130222704605, 0.15304341039629224, 0.12895487914436726, 0.14489882964646794])})
#peaks.update({'Contrast0.07': np.array([0.03995675021506772, 0.12698832336642718, 0.15314555810206895, 0.18447519902923457, 0.1605805751639129, 0.15533122870542898, 0.1261433142092353, 0.08349659698610355, 0.05624312637041744, 0.054932249827459714])})

#peaks.update({'Contrast0.99': np.array([0.18234518105358205, 0.20264061079696338, 0.1981082847585681, 0.18080599608687076, 0.15722726992694327, 0.16269456002947744])})
#peaks.update({'Contrast0.07': np.array([0.03995675021506772, 0.12698832336642718, 0.15314555810206895, 0.18447519902923457, 0.1605805751639129, 0.15533122870542898])})


#peaks = np.array([0.03995, 0.12698, 0.15314, 0.18447, 0.16058, 0.15533, 0.12614, 0.083496, 0.05624, 0.05493])

#sizes = np.array([0.375, 0.5, 0.75, 1., 1.5, 2., 3., 4., 6., 8.])
#sizes = np.array([0.375, 0.5, 0.75, 1., 1.5, 2.])

#contrasts = np.array([0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07])

#sizes = np.array([0.375, 0.5, 0.75, 1])
#contrasts = np.array([0.99])
#peaks = np.array([0.03995675021506772, 0.03995675021506772, 0.03995675021506772, 0.03995675021506772])
#                  0.12698832336642718, 0.12698832336642718, 0.12698832336642718, 0.12698832336642718,
#                  0.15314555810206895, 0.15314555810206895, 0.15314555810206895, 0.15314555810206895,
#                  0.18447519902923457, 0.18447519902923457, 0.18447519902923457, 0.18447519902923457])


#peaks, contrasts, targetRadii = analyzeTadin.analyzeTadin('tadinReplication')

def fitSurroundSuppression(subjectID, **kwargs):

    from scipy import special
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.optimize import curve_fit
    from sklearn.metrics import r2_score
    import os
    import makeGroupResponse
    import analyzeTadin

    if 'skipC2S15' in kwargs:
        skipC2S15 = kwargs['skipC2S15']
    else:
        skipC2S15 = False

    if 'summaryStatistic' in kwargs:
        summaryStatistic = kwargs['summaryStatistic']
    else:
        summaryStatistic = 'peaks'

    if 'contrasts' in kwargs:
        contrasts = kwargs['contrasts']
    else:
        contrasts = [2,99]

    if 'sizes' in kwargs:
        sizes = kwargs['sizes']
    else:
        sizes = [1.5, 3, 6, 12]

    if 'model' in kwargs:
        model = kwargs['model']
    else:
        model = 'tadin'

    if 'useLog' in kwargs:
        useLog = kwargs['useLog']
    else:
        useLog = False

    # Get the data
    groups = ['migraine', 'controls', 'ptha']
    if subjectID in groups:
        summaryResults, pooledResults = makeGroupResponse.makeGroupResponse()
        stats = {'mean': summaryResults[summaryStatistic][subjectID]}
        stats.update({'SEM': summaryResults[summaryStatistic+'SEM'][subjectID]})
    else:
        baseStats, correlograms = analyzeTadin.analyzeTadin(subjectID)
        stats = {'mean': baseStats[summaryStatistic[:-1]]}
        stats.update({'SEM': baseStats[summaryStatistic[:-1]+'SEM']})


    peaks_vector = []
    sizes_vector = []
    contrasts_vector = []

    for contrast in contrasts:
        for size in sizes:

            if skipC2S15:

                if size == 1.5 and contrast == 2:
                    test='badCondition'
                else:
                    peaks_vector.append(stats['mean']['Contrast'+str(contrast)]['Size'+str(size)])
                    sizes_vector.append(size)
                    contrasts_vector.append(contrast)
            else:
                peaks_vector.append(stats['mean']['Contrast' + str(contrast)]['Size' + str(size)])
                sizes_vector.append(size)
                contrasts_vector.append(contrast)

    peaks_matrix = np.zeros([len(sizes_vector), len(contrasts_vector)])
    peaks_vector2 = []
    sizeCounter = 0
    for size in sizes_vector:

        contrastCounter = 0
        for contrast in contrasts_vector:
            peaks_matrix[sizeCounter,contrastCounter] = stats['mean']['Contrast' + str(contrast)]['Size' + str(size)]
            peaks_vector2.append(stats['mean']['Contrast' + str(contrast)]['Size' + str(size)])


    if model == 'tadin':

        # define the model params
        params = {'Ae': [0, 100, 1000],
            'Ai': [0, 100, 1000],
            'alpha': [0,1,10],
            'beta': [0,3,10],
            'c50e': [0, 0.1, 1],
            'c50i': [0, 0.1, 1],
            'ne': [0, 3, 7],
            'ni': [0, 5, 7]}


        def calcCRF(contrasts, Ae, Ai, c50e, c50i, ne, ni):

            Kes = []
            Kis = []
            for contrast in contrasts:


                contrast = contrast / 100

                Ke = Ae * contrast ** ne / ((contrast) ** ne + c50e ** ne)
                Kes.append(Ke)
                Ki = Ai * contrast ** ni / ((contrast) ** ni + c50i ** ni)
                Kis.append(Ki)

            return Kes, Kis


        def calcSRF(sizes, alpha, beta):

            Es = []
            Is = []
            for size in sizes:

                    if useLog:
                        size = np.log(size)

                    E = 1-np.e**(-((size**2)/(alpha**2))/2)
                    Es.append(E)

                    I = 1-np.e**(-((size**2)/(beta**2))/2)
                    Is.append(I)

            return Es, Is

        def calcSurroundSuppression(sizes, contrasts, Kes, Kis, Es, Is):

            contrastCounter = 0
            Rs = []

            sizeCounter = 0
            for size in sizes:

                contrastCounter = 0
                for contrast in contrasts:

                    R = (Kes[contrastCounter] * Es[sizeCounter]) / (1 + Kis[contrastCounter]*Is[sizeCounter])
                    Rs.append(R)


                    contrastCounter = contrastCounter + 1
                sizeCounter = sizeCounter + 1

            return Rs


        def spatialSuppressionMechanisticModel(sizesXcontrast, Ae, Ai, alpha, beta,  c50e, c50i, ne, ni):

            sizes, contrasts = sizesXcontrast

            Kes, Kis = calcCRF(contrasts, Ae, Ai, c50e, c50i, ne, ni)

            Es, Is = calcSRF(sizes, alpha, beta)

            Rs = calcSurroundSuppression(sizes, contrasts, Kes, Kis, Es, Is)



            return np.array(Rs)



        # assemble params:
        paramNames = list(params.keys())
        startingValues = []
        upperLimits = []
        lowerLimits = []
        for param in paramNames:
            startingValues.append(params[param][1])
            upperLimits.append(params[param][2])
            lowerLimits.append(params[param][0])





        popt, pcov = curve_fit(spatialSuppressionMechanisticModel, (sizes_vector,contrasts_vector), peaks_vector2, p0=startingValues, maxfev=10000, bounds=[lowerLimits, upperLimits])

        #[alpha0, beta1, Ae2, Ai3, ne4, ni5, c50e6, c50i7, R0, C]

        fittedParams = {'Ae': popt[0],
            'Ai': popt[1],
            'alpha': popt[2],
            'beta': popt[3],
            'c50e': popt[4],
            'c50i': popt[5],
            'ne': popt[6],
            'ni': popt[7]}


    predictionSizes = np.array(range(int(np.ceil(sizes[-1]*1.5*1000))))/1000

    if useLog:
        predictionSizes = predictionSizes[1:-1]
    y_pred = spatialSuppressionMechanisticModel((predictionSizes,contrasts), *popt)
    y_pred = y_pred.reshape(len(predictionSizes), len(contrasts))

    y_pred_veridical = spatialSuppressionMechanisticModel((sizes_vector,contrasts_vector), *popt)

    r2 = r2_score(peaks_vector2, y_pred_veridical)



    counter = 0
    for contrast in contrasts:

        meanVector = []
        SEMVector = []
        for size in sizes:
            meanVector.append(stats['mean']['Contrast'+str(contrast)]['Size'+str(size)])
            SEMVector.append(stats['SEM']['Contrast'+str(contrast)]['Size'+str(size)])

        fig, (ax1, ax2, ax3) = plt.subplots(1,3)

        ax1.plot(np.log(predictionSizes), y_pred[:,counter], color='red')
        #plt.plot(np.log(sizes), meanVector, label=str(contrast)+'%')
        ax1.errorbar(np.log(sizes), meanVector, SEMVector,
                     label='Contrast: ' + str(contrast), ls='none')

        counter = counter+1



 #   plt.plot(np.log(sizes), peaks['Contrast0.07'])
    ax1.set_xlim([np.log(sizes[0]) - np.log(1.1), np.log(sizes[-1]) + np.log(1.1)])
    ax1.set_ylim([-0, 0.25])
    ax1.set_xticks(np.log(sizes), sizes)
    ax1.set_xlabel('Stimulus Size (degrees)')
    ax1.set_ylabel(summaryStatistic)
    ax1.legend()
    ax1.set_title('R2 = '+str(round(r2,4)))

    # Plot the SRF
    ax2.set_title('Size Response Function')
    Es, Is = calcSRF(predictionSizes, fittedParams['alpha'], fittedParams['beta'])
    ax2.plot(predictionSizes, Es, label='E')
    ax2.plot(predictionSizes, Is, label='I')
    ax2.set_xlim([np.log(sizes[0]) - np.log(1.1), np.log(sizes[-1]) + np.log(1.1)])
    ax2.set_xticks(np.log(sizes), sizes)
    ax2.set_xlabel('Stimulus Size (degrees)')
    ax2.legend()

    # Plot the CRF
    ax3.set_title('Contrast Response Function')
    predictionContrasts = np.linspace(0, 100, 10000)

    Kes, Kis = calcCRF(predictionContrasts, fittedParams['Ae'], fittedParams['Ai'], fittedParams['c50e'], fittedParams['c50i'], fittedParams['ne'], fittedParams['ni'])
    ax3.plot(predictionContrasts, Kes, label='Ke')
    ax3.plot(predictionContrasts, Kis, label='Ki')
    ax3.set_xlim([-5, 105])
    ax3.set_xticks([0, 50, 100])
    ax3.set_xlabel('Stimulus Contrast')
    ax3.legend()

    savePathRoot = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/analysis/'
    savePath = savePathRoot + '/' + 'horizontalContinuous' + '/modelFits/'

    contrastsString = ",".join(str(x) for x in contrasts)
    sizesString = ",".join(str(x) for x in sizes)
    fig.set_figwidth(13)

    fig.savefig(savePath + 'C' + contrastsString + '_S' + sizesString + '_'+subjectID+'_tadinFit.png', bbox_inches="tight")
    fig.close()



fitSurroundSuppression('controls', contrasts=[99])


#print('end')
