def fitSizeModel(sizes, peaks):

    from scipy import special
    import matplotlib.pyplot as plt
    import numpy as np


    Ae = 51
    Ai = 0.051
    n = 1.5
    c50 = 0.04
    beta = 2.5
    S = 1.0
    m = 6.8
    k = 0.21
    R0 = 0

    def sizeModel(Ae, Ai, n, c50, beta, S, m, k, R0, w, contrast):
        from scipy import special

        ECrf = Ae * (contrast**n)/((contrast**n)+(c50**n))
        ICrf = Ai*ECrf
        alpha = S/(1+m*np.e**(-k/contrast))
        E = ECrf * special.erf(w/alpha)
        I = ICrf * special.erf(w/beta) *(beta/alpha)
        R = R0 + E - I

        return R

    contrast = 0.42
    sizes = [0.125, 0.25, 0.5, 1, 2, 4, 8]
    sizes = range(8000)
    sizes = np.array(sizes)*1/1000

    predictions = []
    for size in sizes:
        R = sizeModel(Ae, Ai, n, c50, beta, S, m, k, R0, size, contrast)
        predictions.append(R)

    plt.plot(np.log(sizes), predictions)
