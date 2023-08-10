import numpy as np

#sizes = np.array(np.array(range(8000))/1000)
#peaks = np.array([[10, 20, 10], [20, 30, 20]])
#contrasts = np.array([0.07])

peaks = {'Contrast0.99': ''}
peaks.update({'Contrast0.99': np.array([0.18234518105358205, 0.20264061079696338, 0.1981082847585681, 0.18080599608687076, 0.15722726992694327, 0.16269456002947744, 0.14312130222704605, 0.15304341039629224, 0.12895487914436726, 0.14489882964646794])})
#peaks.update({'Contrast0.07': np.array([0.03995675021506772, 0.12698832336642718, 0.15314555810206895, 0.18447519902923457, 0.1605805751639129, 0.15533122870542898, 0.1261433142092353, 0.08349659698610355, 0.05624312637041744, 0.054932249827459714])})

#peaks.update({'Contrast0.99': np.array([0.18234518105358205, 0.20264061079696338, 0.1981082847585681, 0.18080599608687076, 0.15722726992694327, 0.16269456002947744])})
#peaks.update({'Contrast0.07': np.array([0.03995675021506772, 0.12698832336642718, 0.15314555810206895, 0.18447519902923457, 0.1605805751639129, 0.15533122870542898])})


#peaks = np.array([0.03995, 0.12698, 0.15314, 0.18447, 0.16058, 0.15533, 0.12614, 0.083496, 0.05624, 0.05493])

sizes = np.array([0.375, 0.5, 0.75, 1., 1.5, 2., 3., 4., 6., 8.])
#sizes = np.array([0.375, 0.5, 0.75, 1., 1.5, 2.])

#contrasts = np.array([0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07])

#sizes = np.array([0.375, 0.5, 0.75, 1])
contrasts = np.array([0.99])
#peaks = np.array([0.03995675021506772, 0.03995675021506772, 0.03995675021506772, 0.03995675021506772,
#                  0.12698832336642718, 0.12698832336642718, 0.12698832336642718, 0.12698832336642718,
#                  0.15314555810206895, 0.15314555810206895, 0.15314555810206895, 0.15314555810206895,
#                  0.18447519902923457, 0.18447519902923457, 0.18447519902923457, 0.18447519902923457])
def fitTadin(sizes, peaks, contrasts):

    from scipy import special
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.optimize import curve_fit


    sizes_repackaged = np.tile(sizes, len(contrasts))
    contrasts_repackaged = np.tile(contrasts, len(sizes))

    peaks_vector = []
    for ss in range(len(sizes_repackaged)):
        for cc in range(len(contrasts_repackaged)):
            sizeIndex = np.where(sizes == sizes_repackaged[ss])
            sizeIndex = sizeIndex[0][0]
            peaks_vector.append(peaks['Contrast'+str(contrasts_repackaged[cc])][sizeIndex])

    def spatialSuppressionMechanisticModel(sizesXcontrast, alpha, beta, Ae, Ai, ne, ni, c50e, c50i, R0, C):

        sizes, contrasts = sizesXcontrast

        Rs = []
        for size in sizes:
            for contrast in contrasts:

                E = 1-np.e**(-(size**2/alpha**2)/2)
                I = 1-np.e**(-(size**2/beta**2)/2)

                Ke = Ae * contrast**ne/((contrast)**ne + c50e**ne)
                Ki = Ai * contrast**ni/((contrast)**ni + c50i**ni)

                R = C*(Ke * E)/(1+Ki*I) + R0
                #R = C*(Ke * E) - Ki*I + R0

                Rs.append(R)

        return np.array(Rs)



    Ae = 250
    Ai = 50
    alpha = 0.57
    beta = 3
    c50e = 0.2
    c50i = 0.2
    ne = 3
    ni = 5

    R0 = 0
    C = 0.2/10

    p0 = [alpha, beta, Ae, Ai, ne, ni, c50e, c50i, R0, C]
    diff = 0.001
    lowerLims = [0, 0, 0, 0, 3-diff, 5-diff, 0.2-diff, 0.2-diff, -1, 0]
    upperLims = [5, 5, 500, 500, 3+diff, 5+diff, 0.2+diff, 0.2+diff, 1, 1]


    showModelFunction = False
    if showModelFunction:
        Rs = spatialSuppressionMechanisticModel((sizes,contrasts), alpha, beta, Ae, Ai, ne, ni, c50e, c50i, R0, C)
        Rs = Rs.reshape(len(sizes), len(contrasts))
        plt.plot(Rs[:,0])
#        plt.plot(Rs[:, 1])

    popt, pcov = curve_fit(spatialSuppressionMechanisticModel, (sizes_repackaged,contrasts_repackaged), peaks_vector, p0=p0, maxfev=10000, bounds=(lowerLims, upperLims))


    predictionSizes = np.array(range(int(sizes[-1])*1000))/1000
    y_pred = spatialSuppressionMechanisticModel((predictionSizes,contrasts), *popt)
    y_pred = y_pred.reshape(len(predictionSizes), len(contrasts))

    counter = 0
    for contrast in contrasts:
        plt.plot(np.log(predictionSizes), y_pred[:,counter])
        plt.plot(np.log(sizes), peaks['Contrast'+str(contrast)])
        counter = counter+1



 #   plt.plot(np.log(sizes), peaks['Contrast0.07'])
    plt.xlim([np.log(0.25), np.log(10)])
    plt.ylim([0, 0.25])
    plt.xticks(np.log(sizes), sizes)

    print('yikes')


fitTadin(sizes, peaks, contrasts)
