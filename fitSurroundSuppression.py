

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
            'c50e': [0, 0.1, 10],
            'c50i': [0, 0.1, 10],
            'ne': [0, 1, 10],
            'ni': [0, 1, 10]}

        def spatialSuppressionMechanisticModel(sizesXcontrast, Ae, Ai, alpha, beta,  c50e, c50i, ne, ni):

            sizes, contrasts = sizesXcontrast

            Rs = []
            for size in sizes:
                for contrast in contrasts:

                    if contrast > 1:
                        contrast = contrast/100

                    E = 1-np.e**(-((size**2)/(alpha**2))/2)
                    I = 1-np.e**(-((size**2)/(beta**2))/2)

                    Ke = Ae * contrast**ne/((contrast)**ne + c50e**ne)
                    Ki = Ai * contrast**ni/((contrast)**ni + c50i**ni)

                    #R = C*(Ke * E)/(1+Ki*I) + R0
                    #R = C*(Ke * E) - Ki*I + R0

                    R = (Ke * E) / (1 + Ki * I)

                    Rs.append(R)

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

        Ae_fit = popt[2]
        Ai_fit = popt[3]
        alpha_fit = popt[0]
        beta_fit = popt[1]
        c50e_fit = popt[6]
        c50i_fit = popt[7]
        ne_fit = popt[4]
        ni_fit = popt[5]

    predictionSizes = np.array(range(int(np.ceil(sizes[-1]*1.5*1000))))/1000
    y_pred = spatialSuppressionMechanisticModel((predictionSizes,contrasts), *popt)
    y_pred = y_pred.reshape(len(predictionSizes), len(contrasts))

    y_pred_veridical = spatialSuppressionMechanisticModel((sizes_vector,contrasts_vector), *popt)

#    r2 = r2_score(peaks_vector, y_pred_veridical)



    counter = 0
    for contrast in contrasts:

        meanVector = []
        SEMVector = []
        for size in sizes:
            meanVector.append(stats['mean']['Contrast'+str(contrast)]['Size'+str(size)])
            SEMVector.append(stats['SEM']['Contrast'+str(contrast)]['Size'+str(size)])


        plt.plot(np.log(predictionSizes), y_pred[:,counter], color='red')
        #plt.plot(np.log(sizes), meanVector, label=str(contrast)+'%')
        plt.errorbar(np.log(sizes), meanVector, SEMVector,
                     label='Contrast: ' + str(contrast), ls='none')

        counter = counter+1



 #   plt.plot(np.log(sizes), peaks['Contrast0.07'])
    plt.xlim([np.log(sizes[0]) - np.log(1.1), np.log(sizes[-1]) + np.log(1.1)])
    plt.ylim([-0, 0.25])
    plt.xticks(np.log(sizes), sizes)
    plt.legend()

    text = 'Excitatory Center:\n\
    - alpha:   ' + str(round(alpha_fit,3)) + '   (' + str(alpha_ll) + ', ' + str(alpha_ul) + ')\n\
    - ne:      ' + str(round(ne_fit,3)) + '   (' + str(ne_ll) + ', ' + str(ne_ul) + ')\n\
    - c50e:    ' + str(round(c50e_fit,3)) + '   (' + str(c50e_ll) + ', ' + str(c50e_ul) + ')\n\
    - Ae:      ' + str(round(Ae_fit,3)) + '   (' + str(Ae_ll) + ', ' + str(Ae_ul) + ')\n\
Inhibitory Surround:\n\
    - beta:    ' + str(round(beta_fit,3)) + '   (' + str(beta_ll) + ', ' + str(beta_ul) + ')\n\
    - ni:      ' + str(round(ni_fit,3)) + '   (' + str(ni_ll) + ', ' + str(ni_ul) + ')\n\
    - c50i:    ' + str(round(c50i_fit,3)) + '   (' + str(c50i_ll) + ', ' + str(c50i_ul) + ')\n\
    - Ai:      ' + str(round(Ai_fit,3)) + '   (' + str(Ai_ll) + ', ' + str(Ai_ul) + ')\n'

    text1 = 'Excitatory Center:\n\
    - alpha:   ' + str(round(alpha_fit, 3)) + '   (' + str(alpha_ll) + ', ' + str(alpha_ul) + ')\n\
    - ne:        ' + str(round(ne_fit, 3)) + '   (' + str(ne_ll) + ', ' + str(ne_ul) + ')\n\
    - c50e:    ' + str(round(c50e_fit, 3)) + '   (' + str(c50e_ll) + ', ' + str(c50e_ul) + ')\n\
    - Ae:        ' + str(round(Ae_fit, 3)) + '   (' + str(Ae_ll) + ', ' + str(Ae_ul) + ')\n'
    text2 = 'Inhibitory Surround:\n\
    - beta:    ' + str(round(beta_fit, 3)) + '   (' + str(beta_ll) + ', ' + str(beta_ul) + ')\n\
    - ni:        ' + str(round(ni_fit, 3)) + '   (' + str(ni_ll) + ', ' + str(ni_ul) + ')\n\
    - c50i:    ' + str(round(c50i_fit, 3)) + '   (' + str(c50i_ll) + ', ' + str(c50i_ul) + ')\n\
    - Ai:        ' + str(round(Ai_fit, 3)) + '   (' + str(Ai_ll) + ', ' + str(Ai_ul) + ')\n'




    #plt.text(np.log(sizes[0]), -0.2, text1, ha='left')
    plt.figtext(0.1, -0.2, text1, ha='left')

    #plt.text((np.log(sizes[-1])+np.log(sizes[0]))/2, -0.2, text2, ha='left')
    plt.figtext(0.6, -0.2, text2, ha='left')


    savePathRoot = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/analysis/'
    savePath = savePathRoot + '/' + 'horizontalContinuous' + '/modelFits/'

    contrastsString = ",".join(str(x) for x in contrasts)
    sizesString = ",".join(str(x) for x in sizes)
    plt.savefig(savePath + 'R2' + str(r2) + '_C' + contrastsString + '_S' + sizesString + '_pooled_TadinFit.png', bbox_inches="tight")
    plt.close()


    ## Plot out the inner model components
    ws = np.linspace(0, 15, 100000)
    Es = []
    Is = []
    for w in ws:
        E = 1 - np.e ** (-((w / alpha_fit) ** 2) / 2)
        Es.append(E)
        I = 1 - np.e ** (-((w / beta_fit) ** 2) / 2)
        Is.append(I)

    plt.plot(np.log(ws), Es, label='E', color='k', linestyle='-')
    plt.plot(np.log(ws), Is, label='I', color='k', linestyle='--')

    plt.legend()
    plt.xlabel('Stimulus Size (degrees)')
    plt.ylabel('E, excitatory center')
    desiredXTicks = [1.5, 3, 6, 12]
    plt.xticks(np.log(desiredXTicks), desiredXTicks)
    plt.xlim([np.log(1.5) - np.log(1.1), np.log(12) + np.log(1.1)])
    plt.savefig(savePath + 'R2' + str(r2) + '_tadinFit_centerSurround.png', bbox_inches="tight")
    plt.close()

    cs = np.linspace(0, 100, 10000)
    Kes = []
    Kis = []

    for c in cs:
        c = c/100
        Ke = Ae_fit * ((c ** ne_fit) / (c ** ne_fit + c50e_fit ** ne_fit))
        Kes.append(Ke)

        Ki = Ai_fit * ((c ** ni_fit) / (c ** ni_fit + c50i_fit ** ni_fit))
        Kis.append(Ki)




    plt.plot(cs, Kes, label='Ke', color='k', linestyle='-')
    plt.plot(cs, Kis, label='Ki', color='k', linestyle='--')

    plt.legend()
    plt.xlabel('Contrast')
    plt.ylabel('K')
    # desiredXTicks = [1.5, 3, 6, 12]
    # plt.xticks(np.log(desiredXTicks), desiredXTicks)
    # plt.xlim([np.log(1.5)-np.log(1.1), np.log(12)+np.log(1.1)])
    plt.savefig(savePath +'R2' + str(r2) + '_tadinFit_nakaRushton.png', bbox_inches="tight")

    plt.close()




    print('yikes')

#fitTadin(sizes, peaks, contrasts)
#sizes = targetRadii

fitSurroundSuppression('controls', contrasts=[2, 99])


#print('end')
