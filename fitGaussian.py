## Fit the cross correlation
def fitGaussian(correlogram, correlationTimebase, stimulusName, responseName, saveSuffix, savePath, trialDescriptor):

    import numpy as np
    import matplotlib.pyplot as plt
    import os
    from psychopy import visual
    from scipy.optimize import curve_fit

    correlogram = list(correlogram)
    time0 = np.argmin(np.abs(np.array(correlationTimebase) - 0))
    #maxCorrelation = max(correlogram[time0:-1], key=abs)
    maxCorrelation = max(correlogram[time0:-1])
    maxCorrelation = max(correlogram[time0:time0+1000])

    maxCorrelationRounded = round(maxCorrelation, 3)
    indexOfMaxCorrelation = correlogram.index(maxCorrelation)
    shift = correlationTimebase[indexOfMaxCorrelation]

    # Fit a Gaussian to cross correlogram

    def func(x, lag, width, peak):
        return visual.filters.makeGauss(np.log(x), mean=np.log(lag), sd=np.log(width), gain=peak, base=0)

    if np.sum(np.isnan(correlogram)) == len(correlogram):
        peak = np.nan
        lag = np.nan
        width_fwhm = np.nan
        r2 = np.nan

        peak_rounded = np.nan
        lag_rounded = np.nan
        width_fwhm_rounded = np.nan
        r2_rounded = np.nan

        y_pred = correlogram

    else:

        # Do the fit
        popt, pcov = curve_fit(func, range(len(correlogram)), correlogram, p0=[indexOfMaxCorrelation, 1.1, maxCorrelation],
                               bounds = ([time0, 0, -1], [len(correlogram), 2, 1]), maxfev=100000)
                            #p0=[shift, 0.4, maxCorrelation])
                               #bounds=([0, 0, -1], [2, 0.5, 1]))
        lag = correlationTimebase[0] + popt[0]*(correlationTimebase[1]-correlationTimebase[0])
        width_sigma = popt[1]
        width_fwhm = width_sigma * ((8 * np.log(2)) ** 0.5)
        peak = popt[2]
        peak_rounded = round(peak, 3)
        width_fwhm_rounded = round(width_fwhm, 3)
        lag_rounded = round(lag, 3)

        y_pred = func(range(len(correlogram)), *popt)

        SSres = sum((np.array(correlogram) - np.array(y_pred)) ** 2)
        SStot = sum((np.array(correlogram) - np.mean(correlogram)) ** 2)
        r2 = 1 - SSres / SStot
        r2_rounded = round(r2, 3)

    fitStats= {'peak': peak}
    fitStats.update({'lag': lag})
    fitStats.update({'width': width_fwhm})
    fitStats.update({'R2': r2})

    plt.plot(correlationTimebase, correlogram, label='CCG')
    plt.plot(correlationTimebase, y_pred, label='Fit')
    plt.legend()
    plt.title('Peak: ' + str(peak_rounded) + ', Lag: ' + str(lag_rounded) + ', Width: ' + str(
        width_fwhm_rounded) + ', R2 = ' + str(r2_rounded))
    # Note that positive time means shifting the stimulus forward in time relative to a stationary response time series

    if not os.path.exists(savePath):
        os.makedirs(savePath)
    plt.savefig(savePath + trialDescriptor + '_crossCorrelation_' + stimulusName + '-' + responseName + saveSuffix + '.png')
    plt.close()

    return fitStats