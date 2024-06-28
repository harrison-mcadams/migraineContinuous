def simulateKalman(targetPositions, **kwargs):

    x = targetPositions

    import numpy as np
    import matplotlib.pyplot as plt

    # use the true target position vector to compute Q

    x_diff = np.diff(targetPositions)
    Q = np.var(x_diff)

    R = Q*1/6

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
            P_t_minus1 = P_t[counter - 1]


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
        

    #

    plt.plot(x)
    plt.plot(x_pred)
    plt.show()

    a = np.diff(x)
    b = np.diff(x_pred)
    a = (a - np.mean(a)) / (np.std(a) * len(a))
    b = (b - np.mean(b)) / (np.std(b))
    correlations = np.correlate(a, b, 'full')

    print('done')


