def simulateKalman(targetPositions, **kwargs):

    x = targetPositions

    import numpy as np
    import matplotlib.pyplot as plt

    # use the true target position vector to compute Q

    x_diff = np.diff(targetPositions)
    Q = np.var(x_diff)

    R = Q*1/6

    x_pred = []
    P = []
    K = []
    y = []

    counter = 0
    for ii in x:




    plt.plot(x)
    plt.plot(x_pred)

    a = np.diff(x)
    b = np.diff(x_pred)
    a = (a - np.mean(a)) / (np.std(a) * len(a))
    b = (b - np.mean(b)) / (np.std(b))
    correlations = np.correlate(a, b, 'full')

    print('done')


