def maximizeLikelihood(x, x_hat):
    import numpy as np
    import scipy
    import matplotlib.pyplot as plt

    def create_bidiagonal_matrix(size, k):
        """
        Creates a bidiagonal matrix D of size (size x size) with 1 on the main diagonal
        and K-1 on the below-diagonal.

        Args:
            size: The size of the square matrix.
            k: The value to place on the below-diagonal (K-1).

        Returns:
            A NumPy array representing the bidiagonal matrix.
        """
        # Validate input (size must be greater than 1)
        if size <= 1:
            raise ValueError("Size of the matrix must be greater than 1.")

        # Create a diagonal of ones with size
        diagonal = np.ones(size)

        # Create a ones array with size-1 for the below diagonal (shifted by 1)
        below_diagonal = np.ones(size - 1) * (k - 1)

        # Combine them using np.diag for efficient diagonal matrix creation
        D = np.diag(diagonal, k=0) + np.diag(below_diagonal, k=-1)

        return D

    x_diff = np.diff(x)
    Q = np.var(x_diff)

    Rs = np.arange(1,1001,1)


    posteriors = []
    for R in Rs:

        P = Q/2 * (((1 + 4 * R / Q)**0.5) - 1)

        K = (Q + P) / (Q + P + R)

        size = len(x_hat)
        D = create_bidiagonal_matrix(size, K)


        firstTransposedMatrix = (x_hat - K * np.linalg.inv(D)@x)
        firstTransposedMatrix.transpose()

        DTransposed = D.transpose()

        n = len(x_hat)

        temp = D@x_hat - K*x
        tempTransposed = temp.transpose()

        #posterior = - n / 2 * np.log(2*np.pi) - 1/2 * scipy.linalg.logm((((K**2)*R*np.linalg.inv(D)@DTransposed))) - 1/2 * firstTransposedMatrix @ np.linalg.inv((((K**2)*R*np.linalg.inv(D)@DTransposed))) @ (x_hat - K*np.linalg.inv(D)@x)

        nLL = 0 - (-1/(2*(K**2)*R)*tempTransposed@temp - n/2 * np.log(R) - n * np.log(K))

        posteriors.append(nLL)

    # Print the resulting bidiagonal matrix
    print('I think the positional uncertainty is: ' + str(round(posteriors.index(min(posteriors))**0.5,2)))


    