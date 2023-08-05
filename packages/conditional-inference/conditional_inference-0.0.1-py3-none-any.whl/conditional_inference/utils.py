from typing import Union, Sequence

import numpy as np
from scipy.stats import multivariate_normal

Numeric1DArray = Sequence[float]


def convert_to_array(arr: Union[Numeric1DArray, np.ndarray, float]) -> np.ndarray:
    """Convert to numpy array.

    Args:
        arr (Union[Numeric1DArray, np.ndarray, float]): Value to convert.

    Returns:
        np.ndarray: Converted value.
    """
    if isinstance(arr, np.ndarray):
        return arr
    if np.isscalar(arr):
        return np.array([float(arr)])  # type: ignore
    return np.array([float(i) for i in arr])  # type: ignore


def ranked_mean_squared_error(
    mean: Numeric1DArray,
    cov: np.ndarray,
    estimated_means: np.ndarray,
    sample_weight: np.ndarray = None,
) -> float:
    """Compute ranked mean squared error.

    This loss function consider what the MSE would be if you drew sample means from
    population means given by ``estimated_means``, rank ordered them, and compared them
    to the observed sample means given by ``mean``.

    Args:
        mean (Numeric1DArray): (n,) array of observed sample means.
        cov (np.ndarray): (n, n) covariance matrix of sample means.
        estimated_means (np.ndarray): (# samples, n) matrix of draws from distribution of
            population means.
        sample_weight (np.ndarray, optional): (# samples,) array of sample weights for
            ``estimated_means``. Defaults to None.

    Returns:
        float: Loss.
    """
    if sample_weight is None:
        sample_weight = np.ones(estimated_means.shape[0])
    sample_weight = np.array(sample_weight)
    sample_weight /= sample_weight.sum()

    mean = np.array(mean)
    mean = mean[mean.argsort()]
    mse = 0
    for estimated_mean, weight in zip(estimated_means, sample_weight):
        sample_mean = multivariate_normal(estimated_mean, cov).rvs()
        mse += weight * ((mean - sample_mean[sample_mean.argsort()]) ** 2).mean()
    return mse


def weighted_quantile(
    values: np.array,
    quantiles: np.array,
    sample_weight: np.array = None,
    values_sorted: bool = False,
) -> np.array:
    """Compute weighted quantiles.

    Args:
        values (np.array): (n,) array over which to compute quantiles.
        quantiles (np.array): (k,) array of quantiles of interest.
        sample_weight (np.array, optional): (n,) array of sample weights. Defaults to None.
        values_sorted (bool, optional): Indicates that ``values`` have been pre-sorted. Defaults to False.

    Returns:
        np.array: (k,) array of weighted quantiles.

    Notes:
        Credit to `Stackoverflow <https://stackoverflow.com/a/29677616/10676300>`_.
    """
    values = np.array(values)
    quantiles = convert_to_array(quantiles)
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    sample_weight = np.array(sample_weight)
    assert np.all(quantiles >= 0) and np.all(
        quantiles <= 1
    ), "quantiles should be in [0, 1]"

    if not values_sorted:
        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]

    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    weighted_quantiles /= np.sum(sample_weight)
    return np.interp(quantiles, weighted_quantiles, values)


def weighted_cdf(values: np.array, x: float, sample_weight: np.array = None) -> float:
    """Compute weighted CDF.

    Args:
        values (np.array): (n,) array over which to compute the CDF.
        x (float): Point at which to evaluate the CDF.
        sample_weight (np.array, optional): (n,) array of sample weights. Defaults to None.

    Returns:
        float: CDF of ``values`` evaluated at ``x``.
    """
    values = np.array(values)
    if sample_weight is None:
        sample_weight = np.ones(values.shape[0])
    sample_weight = np.array(sample_weight)
    return ((values < x) * sample_weight / sample_weight.sum()).sum()
