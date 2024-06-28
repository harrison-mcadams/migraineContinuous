def simulateKalman(targetPositions, **kwargs):

    x = targetPositions

    import numpy as np
    import matplotlib.pyplot as plt

    # use the true target position vector to compute Q

    x_diff = np.diff(targetPositions)
    Q = np.var(x_diff)

    R = Q*30*2

    x_hat = []
    P = []
    K = []
    y = []

    P_t_0 = 0
    x_hat_0 = 0


    counter = 0


    for ii in x:

        if counter == 0:

            x_hat_minus1 = x_hat_0
            P_t_minus1 = P_t_0

        else:
            x_hat_minus1 = x_hat[counter - 1]
            P_t_minus1 = P[counter - 1]


        # Prediction
        x_t = x[counter]

        # Estimation
        v_t = np.random.normal(loc=0.0, scale=np.sqrt(R))
        y_t = x_t + v_t

        # Time for the Kalman filter
        S_t = P_t_minus1 + Q

        K_t = S_t / (S_t + R)

        x_hat_t = x_hat_minus1 + K_t * (y_t - x_hat_minus1)

        P_t = K_t * R

        P.append(P_t)
        x_hat.append(x_hat_t)

        counter = counter + 1
        

    # Do some plotting
    fig, (ax1, ax2) = plt.subplots(2)

    ax1.plot(x, label='Target')
    ax1.plot(x_hat, label='Cursor')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Position')
    ax1.legend()
    ax1.set_title('Position Uncertainty Estimate = '+ str(round(R**0.5,2)))




    a = np.diff(x_hat)
    b = np.diff(x)
    a = (a - np.mean(a)) / (np.std(a) * len(a))
    b = (b - np.mean(b)) / (np.std(b))
    correlations = np.correlate(a, b, 'full')

    startTime = -1
    endTime = 2
    dt = 1/60

    zeroIndex = int(np.floor(len(correlations) / 2))
    startIndex = int(zeroIndex + startTime / dt)
    endIndex = int(zeroIndex + endTime / dt)


    correlogram_toPlot = correlations[startIndex:endIndex]
    timebase_toPlot = np.arange(startTime, endTime, dt)

    ax2.plot(timebase_toPlot, correlogram_toPlot)
    ax2.set_ylabel('Correlation')
    ax2.set_xlabel('Time [s]')

    plt.tight_layout
    #plt.show()

    return x_hat




    print('done')


