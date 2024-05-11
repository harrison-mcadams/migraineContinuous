

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
    import makeStruct

    from matplotlib.widgets import Button, Slider

    if 'skipC2S15' in kwargs:
        skipC2S15 = kwargs['skipC2S15']
    else:
        skipC2S15 = False

    if 'params' in kwargs:
        inputtedParams = kwargs['params']
    else:
        inputtedParams = []

    if 'debug' in kwargs:
        debug = kwargs['debug']
    else:
        debug = False

    if 'summaryStatistic' in kwargs:
        summaryStatistic = kwargs['summaryStatistic']
    else:
        summaryStatistic = 'peaks'

    if 'contrasts' in kwargs:
        contrasts = kwargs['contrasts']
    else:
        contrasts = [2,99]

    if 'useR0' in kwargs:
        useR0 = kwargs['useR0']
    else:
        useR0 = False

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
    groups = ['migraine', 'controls', 'ptha', 'pooled']
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

            if skipC2S15:
                if size == 1.5 and contrast == 2:
                    peaks_vector2.append(np.nan)
                else:
                    peaks_vector2.append(stats['mean']['Contrast' + str(contrast)]['Size' + str(size)])

            else:

                peaks_matrix[sizeCounter,contrastCounter] = stats['mean']['Contrast' + str(contrast)]['Size' + str(size)]
                peaks_vector2.append(stats['mean']['Contrast' + str(contrast)]['Size' + str(size)])
            #peaks_vector2.append(stats['mean']['Contrast' + str(contrasts_vector[contrastCounter])]['Size' + str(sizes_vector[sizeCounter])])


            contrastCounter = contrastCounter + 1

        sizeCounter = sizeCounter + 1


    if model == 'tadin':

        # define the model params
        params = {'Ae': [0, 100, 1000],
            'Ai': [0, 100, 1000],
            'alpha': [0,1,10],
            'beta': [0,3,10],
            'c50e': [0, 0.1, 2],
            'c50i': [0, 0.1, 2],
            'ne': [0, 3, 7],
            'ni': [0, 5, 7],
            'criterion': [1,2000,10000],
                  'R0': [0,6,100]}

        if inputtedParams == []:
            test = 'do nothing'
        else:
            inputtedParamNames = list(inputtedParams.keys())
            for ii in inputtedParamNames:
                params[ii] = inputtedParams[ii]

        SRFParamLabels = ['alpha', 'beta', 'criterion', 'R0']
        CRFParamLabels = ['Ae', 'Ai', 'c50e', 'c50i', 'ne', 'ni']

        nLongestParamList = max([len(SRFParamLabels), len(CRFParamLabels)])


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

        def calcSurroundSuppression(sizes, contrasts, Kes, Kis, Es, Is, criterion, R0):

            if model == 'tadin':
                contrastCounter = 0
                Rs = []

                sizeCounter = 0
                for size in sizes:


                    R = (Kes[sizeCounter] * Es[sizeCounter]) / (1 + Kis[sizeCounter]*Is[sizeCounter])

                    if useR0:
                        R = R + R0

                    if summaryStatistic == 'lags':

                        threshold = criterion/(R + R0)

                        R = threshold

                    Rs.append(R)


                    sizeCounter = sizeCounter + 1

            return Rs


        def spatialSuppressionMechanisticModel(sizesXcontrast, Ae, Ai, alpha, beta,  c50e, c50i, ne, ni, criterion, R0):

            sizes, contrasts = sizesXcontrast

            Kes, Kis = calcCRF(contrasts, Ae, Ai, c50e, c50i, ne, ni)

            Es, Is = calcSRF(sizes, alpha, beta)

            Rs = calcSurroundSuppression(sizes, contrasts, Kes, Kis, Es, Is, criterion, R0)





            return np.array(Rs)



        # assemble params:
        paramNames = list(params.keys())
        startingValues = []
        upperLimits = []
        lowerLimits = []
        for param in paramNames:
            startingValues.append(params[param][1])

            if params[param][2] == params[param][0]:
                diff = 0.001
                upperLimits.append(params[param][2]*(1+diff))
                lowerLimits.append(params[param][0]*(1-diff))
            else:
                upperLimits.append(params[param][2])
                lowerLimits.append(params[param][0])





        popt, pcov = curve_fit(spatialSuppressionMechanisticModel, (sizes_vector,contrasts_vector), peaks_vector, p0=startingValues, maxfev=10000, bounds=[lowerLimits, upperLimits], check_finite=False)

        #[alpha0, beta1, Ae2, Ai3, ne4, ni5, c50e6, c50i7, R0, C]

        fittedParams = {'Ae': popt[0],
            'Ai': popt[1],
            'alpha': popt[2],
            'beta': popt[3],
            'c50e': popt[4],
            'c50i': popt[5],
            'ne': popt[6],
            'ni': popt[7],
            'criterion': popt[8],
            'R0': popt[9]}


    predictionSizes = np.array(range(int(np.ceil(sizes[-1]*1.5*1000))))/1000

    if useLog:
        predictionSizes = predictionSizes[1:-1]

    sizes_vector_forPlotting = []
    contrasts_vector_forPlotting = []

    for contrast in contrasts:
        for size in predictionSizes:

                sizes_vector_forPlotting.append(size)
                contrasts_vector_forPlotting.append(contrast)

    y_pred = spatialSuppressionMechanisticModel((sizes_vector_forPlotting,contrasts_vector_forPlotting), *popt)
    y_pred = y_pred.reshape(len(contrasts), len(predictionSizes))

    y_pred_veridical = spatialSuppressionMechanisticModel((sizes_vector,contrasts_vector), *popt)

    r2 = r2_score(peaks_vector, y_pred_veridical)

    fig, axes = plt.subplots(1, 3)

    axes_ss = axes[0]
    counter = 0
    ss = makeStruct.makeStruct([contrasts])
    for contrast in contrasts:

        meanVector = []
        SEMVector = []
        for size in sizes:
            meanVector.append(stats['mean']['Contrast'+str(contrast)]['Size'+str(size)])
            SEMVector.append(stats['SEM']['Contrast'+str(contrast)]['Size'+str(size)])



        ss[str(contrast)], = axes_ss.plot(np.log(predictionSizes), y_pred[counter], color='red')
        #plt.plot(np.log(sizes), meanVector, label=str(contrast)+'%')
        axes_ss.errorbar(np.log(sizes), meanVector, SEMVector,
                     label='Contrast: ' + str(contrast), ls='none')

        counter = counter+1



 #   plt.plot(np.log(sizes), peaks['Contrast0.07'])
    axes_ss.set_xlim([np.log(sizes[0]) - np.log(1.1), np.log(sizes[-1]) + np.log(1.1)])

    yLims = {'peaks': [-0.025, 0.25],
             'correlograms': [-0.025, 0.25],
             'widths': [0, 500],
             'lags': [200, 500]}
    axes_ss.set_ylim(yLims[summaryStatistic])

    axes_ss.set_xticks(np.log(sizes), sizes)
    axes_ss.set_xlabel('Stimulus Size (degrees)')
    axes_ss.set_ylabel(summaryStatistic)
    axes_ss.legend()
    axes_ss.set_title('R2 = '+str(round(r2,4)))

    # Plot the SRF
    axes_srf = axes[1]
    axes_srf.set_title('Size Response Function')
    Es, Is = calcSRF(predictionSizes, fittedParams['alpha'], fittedParams['beta'])
    srf_e, = axes_srf.plot(predictionSizes, Es, label='E')
    srf_i, = axes_srf.plot(predictionSizes, Is, label='I')
    axes_srf.set_xlim([np.log(sizes[0]) - np.log(1.1), np.log(sizes[-1]) + np.log(1.1)])
    axes_srf.set_xticks(np.log(sizes), sizes)
    axes_srf.set_xlabel('Stimulus Size (degrees)')
    axes_srf.legend()

    # Plot the CRF
    axes_crf = axes[2]
    axes_crf.set_title('Contrast Response Function')
    predictionContrasts = np.linspace(0, 100, 10000)

    Kes, Kis = calcCRF(predictionContrasts, fittedParams['Ae'], fittedParams['Ai'], fittedParams['c50e'], fittedParams['c50i'], fittedParams['ne'], fittedParams['ni'])
    crf_Kes, = axes_crf.plot(predictionContrasts, Kes, label='Ke')
    crf_Kis, = axes_crf.plot(predictionContrasts, Kis, label='Ki')
    axes_crf.set_xlim([-5, 105])
    axes_crf.set_xticks([0, 50, 100])
    axes_crf.set_xlabel('Stimulus Contrast')
    axes_crf.legend()

    savePathRoot = os.path.expanduser('~') + '/Desktop/surroundSuppressionPTHA/analysis/'
    savePath = savePathRoot + '/' + 'horizontalContinuous' + '/modelFits/' + summaryStatistic +'/'

    contrastsString = ",".join(str(x) for x in contrasts)
    sizesString = ",".join(str(x) for x in sizes)
    fig.set_figwidth(13)

    y_adjustment = 0.5
    fig.subplots_adjust(bottom=y_adjustment)


    axis_ss_position = axes_ss.get_position()
    axis_srf_position = axes_srf.get_position()
    axis_crf_position = axes_crf.get_position()

    # Make SRF sliders
    SRFSliders = makeStruct.makeStruct([SRFParamLabels])
    SRFSliderAxes = makeStruct.makeStruct([SRFParamLabels])
    counter = 0

    nSRFSliders = len(SRFParamLabels)
    SRFY_adjustment = (y_adjustment-0.1)/nSRFSliders

    for SRFParamLabel in SRFParamLabels:


        SRFSliderAxes[SRFParamLabel] = fig.add_axes([axis_srf_position.x0, counter*SRFY_adjustment, axis_srf_position.x1-axis_srf_position.x0, SRFY_adjustment])

        counter = counter + 1

        SRFSliders[SRFParamLabel] = Slider(
        ax=SRFSliderAxes[SRFParamLabel],
        label=SRFParamLabel,
        valmin=params[SRFParamLabel][0],
        valmax=params[SRFParamLabel][2],
        valinit=fittedParams[SRFParamLabel],
        orientation="horizontal"
    )

    # Make SRF sliders
    CRFSliders = makeStruct.makeStruct([CRFParamLabels])
    CRFSliderAxes = makeStruct.makeStruct([CRFParamLabels])
    counter = 0

    nCRFSliders = len(CRFParamLabels)
    CRFY_adjustment = (y_adjustment - 0.1) / nCRFSliders

    for CRFParamLabel in CRFParamLabels:
        CRFSliderAxes[CRFParamLabel] = fig.add_axes(
            [axis_crf_position.x0, counter * CRFY_adjustment, axis_crf_position.x1 - axis_crf_position.x0,
             CRFY_adjustment])

        counter = counter + 1

        CRFSliders[CRFParamLabel] = Slider(
            ax=CRFSliderAxes[CRFParamLabel],
            label=CRFParamLabel,
            valmin=params[CRFParamLabel][0],
            valmax=params[CRFParamLabel][2],
            valinit=fittedParams[CRFParamLabel],
            orientation="horizontal"
        )

    #axes[1][0]

    # The function to be called anytime a slider's value changes
    def update(val):

        Es, Is = calcSRF(predictionSizes, SRFSliders['alpha'].val, SRFSliders['beta'].val)

        Kes, Kis = calcCRF(predictionContrasts, CRFSliders['Ae'].val, CRFSliders['Ai'].val, CRFSliders['c50e'].val,
                           CRFSliders['c50i'].val, CRFSliders['ne'].val, CRFSliders['ni'].val)

        Rs = spatialSuppressionMechanisticModel((predictionSizes, contrasts), CRFSliders['Ae'].val, CRFSliders['Ai'].val,
                                                SRFSliders['alpha'].val, SRFSliders['beta'].val, CRFSliders['c50e'].val,
                                                CRFSliders['c50i'].val, CRFSliders['ne'].val, CRFSliders['ni'].val, SRFSliders['criterion'].val, SRFSliders['R0'].val)

        Rs = Rs.reshape(len(predictionSizes), len(contrasts))

        srf_e.set_ydata(Es)
        srf_i.set_ydata(Is)

        crf_Kes.set_ydata(Kes)
        crf_Kis.set_ydata(Kis)



        contrastCounter = 0
        for contrast in contrasts:
            ss[str(contrast)].set_ydata(Rs[:, contrastCounter])
            contrastCounter = contrastCounter + 1

        fig.canvas.draw_idle()

    # register the update function with each slider
    for SRFParamLabel in SRFParamLabels:
        SRFSliders[SRFParamLabel].on_changed(update)

    for CRFParamLabel in CRFParamLabels:
        CRFSliders[CRFParamLabel].on_changed(update)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = fig.add_axes([0.1, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')

    def reset(event):
        for SRFParamLabel in SRFParamLabels:
            SRFSliders[SRFParamLabel].reset()

        for CRFParamLabel in CRFParamLabels:
            CRFSliders[CRFParamLabel].reset()

    button.on_clicked(reset)

    if debug:
        plt.show()


    fig.savefig(savePath + 'C' + contrastsString + '_S' + sizesString + '_'+subjectID+'_tadinFit.png', bbox_inches="tight")
    #fig.close()



params = {'alpha': [1, 1, 1]}
fitSurroundSuppression('migraine', contrasts=[2, 99], skipC2S15=True, summaryStatistic='lags', params=params)


#print('end')
