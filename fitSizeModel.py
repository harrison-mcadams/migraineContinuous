import numpy as np

#sizes = np.array(np.array(range(8000))/1000)
#peaks = np.array([[10, 20, 10], [20, 30, 20]])
#contrasts = np.array([0.07])

peaks = {'Contrast0.99': np.array([0.18234518105358205, 0.20264061079696338, 0.1981082847585681, 0.18080599608687076, 0.15722726992694327, 0.16269456002947744, 0.14312130222704605, 0.15304341039629224, 0.12895487914436726, 0.14489882964646794])}
peaks.update({'Contrast0.07': np.array([0.03995675021506772, 0.12698832336642718, 0.15314555810206895, 0.18447519902923457, 0.1605805751639129, 0.15533122870542898, 0.1261433142092353, 0.08349659698610355, 0.05624312637041744, 0.054932249827459714])})
#peaks = np.array([0.03995, 0.12698, 0.15314, 0.18447, 0.16058, 0.15533, 0.12614, 0.083496, 0.05624, 0.05493])

sizes = np.array([0.375, 0.5, 0.75, 1., 1.5, 2., 3., 4., 6., 8.])
#contrasts = np.array([0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07])

#sizes = np.array([0.375, 0.5, 0.75, 1])
contrasts = np.array([0.07, 0.99])
#peaks = np.array([0.03995675021506772, 0.03995675021506772, 0.03995675021506772, 0.03995675021506772,
#                  0.12698832336642718, 0.12698832336642718, 0.12698832336642718, 0.12698832336642718,
#                  0.15314555810206895, 0.15314555810206895, 0.15314555810206895, 0.15314555810206895,
#                  0.18447519902923457, 0.18447519902923457, 0.18447519902923457, 0.18447519902923457])
def fitSizeModel(sizes, peaks, contrasts):

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

    Ae = 51
    Ai = 0.051
    n = 1.5
    c50 = 0.04
    beta = 2.5
    S = 1.0
    m = 6.8
    k = 0.21
    R0 = 0
    C = .18/30


    def sizeModel(sizesXcontrasts, C, Ae, Ai, n, c50, beta, S, m, k, R0):
        from scipy import special

        sizes, contrasts = sizesXcontrasts

        Rs = []
        for size in sizes:
            for contrast in contrasts:
                ECrf = Ae * (contrast**n)/((contrast**n)+(c50**n))
                ICrf = Ai*ECrf
                alpha = S/(1+m*np.e**(-k/contrast))
                E = ECrf * special.erf(size/alpha)
                I = ICrf * special.erf(size/beta) *(beta/alpha)
                R = C*(R0 + E - I)
                Rs.append(R)



        Rs = np.array(Rs)
        return Rs

    p0 = [C, Ae, Ai, n, c50, beta, S, m, k, R0]
    Rs = sizeModel((sizes,contrasts), C, Ae, Ai, n, c50, beta, S, m, k, R0)

    Rs_sizesXcontrasts = Rs.reshape(len(sizes), len(contrasts))
    # Do the fit

    #plt.plot(np.log(sizes), Rs_sizesXcontrasts[:,0])
    #plt.plot(np.log(sizes), Rs_sizesXcontrasts[:,-1])

    popt, pcov = curve_fit(sizeModel, (sizes_repackaged,contrasts_repackaged), peaks_vector, p0=p0)
                           #, p0=[shift, 0.4, maxCorrelation],
                           #bounds=([0, 0, -1], [2, 0.5, 1]))


    predictionSizes = np.array(range(int(sizes[-1])*1000))/1000
    y_pred = sizeModel((predictionSizes,contrasts), *popt)
    y_pred = y_pred.reshape(len(predictionSizes), len(contrasts))

    plt.plot(np.log(predictionSizes), y_pred[:,0])
    plt.plot(np.log(sizes), peaks['Contrast0.07'])

    plt.plot(np.log(predictionSizes), y_pred[:,1])
    plt.plot(np.log(sizes), peaks['Contrast0.99'])
    plt.xlim([np.log(0.25), np.log(10)])
    plt.ylim([0, 0.25])
    plt.xticks(np.log(sizes), sizes)

    print('yikes')


fitSizeModel(sizes, peaks, contrasts)
