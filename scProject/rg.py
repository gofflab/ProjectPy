from . import matcher
from scipy.optimize import lsq_linear
from sklearn import linear_model
import numpy as np


def NNLR_ElasticNet(dataset_filtered, patterns_filtered, projectionName, alpha, L1, iterations=10000):
    """ This method performs an elastic net regression from sci-kit learn.

    :param dataset_filtered: AnnData object cells x genes
    :param patterns_filtered: AnnData object features x genes
    :param projectionName: index of the projection in dataset_filtered.obsm
    :type projectionName: String
    :param alpha: regularization parameter
    :type alpha: double
    :param L1: regularization parameter
    :type L1: double
    :param iterations: number of iterations while performing the regression
    :return: void, the dataset_filtered is mutated and the projection is stored in dataset_filtered.obsm[projectionName]
    """
    matcher.sourceIsValid(dataset_filtered)
    matcher.sourceIsValid(patterns_filtered)
    model = linear_model.ElasticNet(alpha=alpha, l1_ratio=L1, max_iter=iterations, positive=True)
    model.fit(patterns_filtered.X.T, dataset_filtered.X.T)
    dataset_filtered.obsm[projectionName] = model.coef_
    print(model.coef_.shape)


# still experimenting with this but same idea as NNLR_Elastic net, but implements a lasso regression instead
def NNLR_positive_Lasso(dataset_filtered, patterns_filtered, projectionName, alpha, iterations=10000):
    """This method performs a positive lasso regression from sci-kit learn.

    :param dataset_filtered: AnnData object cells x genes
    :param patterns_filtered: AnnData object features x genes
    :param projectionName: index of the projection in dataset_filtered.obsm
    :param alpha: regularization parameter
    :param iterations: number of iterations while performing the regression
    :return: void, the dataset_filtered is mutated and the projection is stored in dataset_filtered.obsm[projectionName]
    """
    matcher.sourceIsValid(dataset_filtered)
    matcher.sourceIsValid(patterns_filtered)
    model = linear_model.Lasso(alpha=alpha, max_iter=iterations, positive=True)
    model.fit(patterns_filtered.X.T, dataset_filtered.X.T)
    dataset_filtered.obsm[projectionName] = model.coef_
    print(model.coef_.shape)


# still experimenting with this but same idea as NNLR_Elastic net, but implements ordinary least squares from scipy no
# regularization
def NNLR_LeastSquares(dataset_filtered, patterns_filtered, projectionName):
    """This performs a non negative least squares regression using Scipy.

    :param dataset_filtered: AnnData object cells x genes
    :param patterns_filtered: AnnData object features x genes
    :param projectionName: index of the projection in dataset_filtered.obsm
    :return: void, the dataset_filtered is mutated and the projection is stored in dataset_filtered.obsm[projectionName]
    """
    matcher.sourceIsValid(dataset_filtered)
    matcher.sourceIsValid(patterns_filtered)
    print(patterns_filtered.X.shape[0], "patterns", dataset_filtered.X.T.shape[1], "data")
    pattern_matrix = np.zeros([patterns_filtered.X.shape[0], dataset_filtered.X.T.shape[1]])
    for i in range(dataset_filtered.shape[1]):
        scip = lsq_linear(np.array(patterns_filtered.X.T).astype('double'),
                          np.array(dataset_filtered.X.T[:, i]).astype('double'),
                          bounds=(0, 1000),
                          method='bvls',
                          lsq_solver='exact')
        pattern_matrix[:, i] = scip.x
    # print(pattern_matrix.shape)
    # print(MSE, "Mean Squared Error")
    dataset_filtered.obsm[projectionName] = np.transpose(pattern_matrix)
