"""Empirical Bayesian analysis.
"""
from __future__ import annotations

from ..base import ColumnsType, Numeric1DArray
from .base import BayesModelBase, BayesResults

import math
import warnings
from typing import Any, Tuple, TypeVar

import numpy as np
from scipy.optimize import minimize_scalar

PriorMeanParams = TypeVar("PriorMeanParams")
PriorCovParams = TypeVar("PriorCovParams")


class EmpiricalBayesBase(BayesModelBase):
    """Mixin for empirical Bayes models. Inherits from
    :class:`conditional_inference.bayes.base.BayesModelBase`.
    """

    def estimate_prior_mean(
        self, prior_mean_params: PriorMeanParams = None
    ) -> np.ndarray:
        """Estimate prior mean vector.

        Args:
            prior_mean_params (PriorMeanParams, optional): Parameters which determine the prior
                mean. Defaults to None.

        Raises:
            NotImplementedError: Classes which inherit the mixin should implement this
                method.

        Returns:
            np.ndarray: (n,) array of prior means.
        """
        raise NotImplementedError()  # pragma: no cover

    def estimate_prior_cov(self, prior_cov_params: PriorCovParams = None) -> np.ndarray:
        """Estimate prior covariance matrix.

        Args:
            prior_cov_params (PriorCovParams, optional): Parameters which determine the prior covariance. Defaults to None.

        Raises:
            NotImplementedError: Classes which inherit the mixin should implement this
                method.

        Returns:
            np.ndarray: (n, n) prior covariance matrix.
        """
        raise NotImplementedError()  # pragma: no cover

    def _estimate_prior_mean_params(
        self, prior_cov: np.ndarray = None
    ) -> PriorMeanParams:
        """Estimate prior mean parameters.

        Args:
            prior_cov (np.ndarray, optional): (n, n) prior covariance matrix. Defaults to None.

        Raises:
            NotImplementedError: Classes which inherit the mixin should implement this
                method.

        Returns:
            PriorMeanParams: Prior mean parameters.
        """
        raise NotImplementedError()  # pragma: no cover

    def _estimate_prior_cov_params(
        self, prior_mean: np.ndarray = None
    ) -> PriorCovParams:
        """Estimate prior covariance parameters.

        Args:
            prior_mean (np.ndarray, optional): (n,) array of prior means. Defaults to None.

        Raises:
            NotImplementedError: Classes which inherit the mixin should implement this
                method.

        Returns:
            PriorCovParams: Prior covariance parameters.
        """
        raise NotImplementedError()  # pragma: no cover

    def estimate_posterior_mean(
        self, prior_mean: np.ndarray = None, prior_cov: np.ndarray = None
    ) -> np.ndarray:
        """Estimate the posterior mean vector.

        Args:
            prior_mean (np.ndarray, optional): (n,) array of prior means. Defaults to None.
            prior_cov (np.ndarray, optional): (n, n) prior covariance matrix. Defaults to None.

        Returns:
            np.ndarray: (n,) array of posterior means.
        """
        prior_mean, prior_cov = self._get_prior_mean_cov(prior_mean, prior_cov)
        xi = self._compute_xi(prior_cov)
        return prior_mean + (np.identity(self.mean.shape[0]) - xi) @ (
            self.mean - prior_mean
        )

    def estimate_posterior_cov(self, prior_cov: np.ndarray = None) -> np.ndarray:
        """Estimate the posterior covariance matrix.

        Args:
            prior_cov (np.ndarray, optional): (n, n) prior covariance matrix. Defaults to None.

        Returns:
            np.ndarray: (n, n) posterior covariance matrix.

        Notes:
            This approximation uses a plug-in estimator which likely underestimates the
            posterior covariance.
        """
        if prior_cov is None:
            prior_cov = self.estimate_prior_cov()
        xi = self._compute_xi(prior_cov)
        return (np.identity(self.mean.shape[0]) - xi) @ self.cov

    def fit(
        self,
        cols: ColumnsType = None,
        title: str = "Empirical Bayes estimates",
        **kwargs: Any,
    ) -> BayesResults:
        """Fit the model.

        Args:
            cols (ColumnsType, optional): Names or indices of the policies of interest. Defaults to
                None.
            title (str, optional): Results title. Defaults to "Empirical Bayes results".
            **kwargs (Any): Passed to ``BayesResults``.

        Returns:
            BayesResults: Results.
        """
        prior_mean_params, prior_cov_params = self._estimate_prior_params()
        prior_mean = self.estimate_prior_mean(prior_mean_params)
        prior_cov = self.estimate_prior_cov(prior_cov_params)
        return BayesResults(
            self,
            cols,
            params=self.estimate_posterior_mean(prior_mean, prior_cov),
            cov_params=self.estimate_posterior_cov(prior_cov),
            title=title,
            **kwargs,
        )

    def log_likelihood(self, prior_mean: np.ndarray, prior_cov: np.ndarray) -> float:
        """Evaluate the log likelihood.

        Args:
            prior_mean (np.ndarray): (n,) array of pior means.
            prior_cov (np.ndarray): (n, n) prior covariance matrix.

        Returns:
            float: Log likelihood of observing the input prior mean and covariance
            given the data.
        """
        marginal_mean = prior_mean
        marginal_cov = prior_cov + self.cov
        inv_marginal_cov = np.linalg.inv(marginal_cov)
        return -0.5 * (
            self.mean.shape[0] * np.log(2 * math.pi)
            + np.log(np.linalg.det(marginal_cov))
            + (self.mean - marginal_mean).T
            @ inv_marginal_cov
            @ (self.mean - marginal_mean)
        )

    def _estimate_prior_params(
        self, tol: float = 1e-3, max_iter: int = 100
    ) -> Tuple[PriorMeanParams, PriorCovParams]:
        """Estimate parameters using expectation maximization.

        Args:
            tol (float, optional): Stopping criterion. Defaults to 1e-3.
            max_iter (int, optional): Stopping criterion. Defaults to 100.

        Returns:
            Tuple[PriorMeanParams, PriorCovParams]: Prior mean and covariance parameters.
        """
        prior_cov = np.zeros(shape=(self.cov.shape))
        prev_log_likelihood = -np.inf
        for _ in range(max_iter):
            prior_mean_params = self._estimate_prior_mean_params(prior_cov)
            prior_mean = self.estimate_prior_mean(prior_mean_params)
            prior_cov_params = self._estimate_prior_cov_params(prior_mean)
            prior_cov = self.estimate_prior_cov(prior_cov_params)
            log_likelihood = self.log_likelihood(prior_mean, prior_cov)
            if abs(log_likelihood - prev_log_likelihood) <= tol:
                return prior_mean_params, prior_cov_params
            prev_log_likelihood = log_likelihood
        warnings.warn(  # pragma: no cover
            "Prior parameter estimation reached maximum iterations before convergence",
            RuntimeWarning,
        )
        return prior_mean_params, prior_cov_params  # pragma: no cover

    def _get_prior_mean_cov(
        self, prior_mean: np.ndarray, prior_cov: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        # get the prior mean vector and covariance matrix
        if prior_mean is None or prior_cov is None:
            prior_mean_params, prior_cov_params = self._estimate_prior_params()
            if prior_mean is None:
                prior_mean = self.estimate_prior_mean(prior_mean_params)
            if prior_cov is None:
                prior_cov = self.estimate_prior_cov(prior_cov_params)
        return prior_mean, prior_cov


class LinearEmpiricalBayes(EmpiricalBayesBase):
    """Empirical linear Bayesian model. Inherits from :class:`EmpiricalBayesBase`.

    Assumes the prior mean vector is a linear combination of the feature matrix.

    Args:
        mean (Numeric1DArray): (n,) array of conventionally-estimated means.
        cov (np.ndarray): (n, n) covariance matrix.
        X (np.ndarray, optional): (n, p) feature matrix. Defaults to None.
        max_prior_cov (float, optional): Maximum prior covariance. The prior covariance
            is assumed to be proportional to the identity matrix. Defaults to 1e6.

    Notes:
        This class' attributes are identical to those of :class:`EmpiricalBayesBase`.
        Note that the estimated posterior covariance matrix doesn't account for
        uncertainty in the estimated prior covariance parameter, and therefore may
        underestimate the posterior covariance.

    Examples:

        .. code-block::

            >>> import numpy as np
            >>> from conditional_inference.bayes.empirical_bayes import LinearEmpiricalBayes
            >>> from scipy.stats import multivariate_normal
            >>> n_policies = 5
            >>> prior_cov = np.identity(n_policies)
            >>> prior_mean = np.zeros(n_policies)
            >>> true_mean = multivariate_normal(prior_mean, prior_cov).rvs()
            >>> sample_cov = np.identity(n_policies)
            >>> sample_mean = multivariate_normal(true_mean, sample_cov).rvs()
            >>> model = LinearEmpiricalBayes(sample_mean, sample_cov)
            >>> model.fit(cols="sorted").summary()
              Empirical Bayes estimates
            ==============================
                coef  pvalue [0.025 0.975]
            ------------------------------
            x3  2.372  0.004  0.614  4.129
            x0  1.251  0.082 -0.507  3.008
            x4 -0.475  0.702 -2.233  1.283
            x1 -0.626  0.758 -2.384  1.131
            x2 -1.976  0.986 -3.734 -0.218
            ===============
            Dep. Variable y
            ---------------
    """

    def __init__(
        self,
        mean: Numeric1DArray,
        cov: np.ndarray,
        X: np.ndarray = None,
        max_prior_cov: float = 1e6,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(mean, cov, X, *args, **kwargs)
        self.max_prior_cov = max_prior_cov

    def estimate_prior_mean(self, prior_mean_params: np.ndarray) -> np.ndarray:
        """Estimate the prior mean vector.

        Args:
            prior_mean_params (np.ndarray): (p,) array of prior mean parameters.

        Returns:
            np.ndarray: (n,) array of prior means.
        """
        return self.X @ prior_mean_params

    def estimate_prior_cov(self, prior_cov_params: float) -> np.ndarray:
        """Estimate the prior covariance matrix.

        Args:
            prior_cov_params (float): Prior covariance parameter. The prior covariance
                is assumed to be proportional to the identity matrix.

        Returns:
            np.ndarray: (n, n) prior covariance matrix.
        """
        return prior_cov_params * np.identity(self.mean.shape[0])

    def estimate_posterior_cov(self, prior_cov: np.ndarray = None) -> np.ndarray:
        """Estimate the posterior covariance matrix.

        Args:
            prior_cov (np.ndarray, optional): (n, n) prior covariance matrix. Defaults to None.

        Returns:
            np.ndarray: (n, n) posterior covariance matrix.
        """
        if prior_cov is None:
            prior_cov = self.estimate_prior_cov()
        post_mean_uncertainty = super().estimate_posterior_cov(prior_cov)
        xi = self._compute_xi(prior_cov)
        X_T = self.X.T
        tau_inv = np.linalg.inv(prior_cov + self.cov)
        prior_mean_uncertainty = (
            xi @ self.X @ np.linalg.inv(X_T @ tau_inv @ self.X) @ X_T @ xi
        )
        return post_mean_uncertainty + prior_mean_uncertainty

    def _estimate_prior_mean_params(self, prior_cov: np.ndarray) -> np.ndarray:
        """Estimate prior mean parameter vector.

        Args:
            prior_cov (np.ndarray): (n, n) prior covariance matrix.

        Returns:
            np.ndarray: (p,) array of prior mean parameters.
        """
        X_T = self.X.T
        tau_inv = np.linalg.inv(prior_cov + self.cov)
        return np.linalg.inv(X_T @ tau_inv @ self.X) @ X_T @ tau_inv @ self.mean

    def _estimate_prior_cov_params(self, prior_mean: np.ndarray) -> float:
        """Estimate the prior covariance parameter by MLE.

        Args:
            prior_mean (np.ndarray): (n,) array of prior means.

        Returns:
            float: Prior covariance parameter. The prior covariance is proportional to
                the identity matrix.
        """

        def loss(prior_cov_params):
            prior_cov = self.estimate_prior_cov(prior_cov_params)
            return -self.log_likelihood(prior_mean, prior_cov)

        return minimize_scalar(loss, bounds=(0, self.max_prior_cov), method="bounded").x


class JamesStein(EmpiricalBayesBase):
    """James-Stein estimator. Inherits from :class:`EmpiricalBayesBase`.

    Notes:
        This estimator is most appropriate when the sample covariance matrix is
        proportional to the identity matrix.

    Examples:

        .. code-block::

            >>> import numpy as np
            >>> from conditional_inference.bayes.empirical_bayes import JamesStein
            >>> from scipy.stats import multivariate_normal
            >>> n_policies = 5
            >>> prior_cov = np.identity(n_policies)
            >>> prior_mean = np.zeros(n_policies)
            >>> true_mean = multivariate_normal(prior_mean, prior_cov).rvs()
            >>> sample_cov = np.identity(n_policies)
            >>> sample_mean = multivariate_normal(true_mean, sample_cov).rvs()
            >>> model = JamesStein(sample_mean, sample_cov)
            >>> model.fit(cols="sorted").summary()
              Empirical Bayes estimates
            ==============================
                coef  pvalue [0.025 0.975]
            ------------------------------
            x4  3.707  0.000  1.710  5.704
            x2  1.734  0.035 -0.143  3.611
            x0  0.623  0.257 -1.245  2.491
            x1 -0.586  0.726 -2.494  1.323
            x3 -0.697  0.762 -2.612  1.218
            ===============
            Dep. Variable y
            ---------------
    """

    def estimate_prior_mean(self, prior_mean_params: np.ndarray) -> np.ndarray:
        """Estimate the prior mean vector.

        Args:
            prior_mean_params (np.ndarray): (p,) array of prior mean parameters.

        Returns:
            np.ndarray: (n,) array of prior means.
        """
        return self.X @ prior_mean_params

    def estimate_prior_cov(self, prior_cov_params: float) -> np.ndarray:
        """Estimate the prior covariance matrix.

        Args:
            prior_cov_params (float): Prior covariance parameter.

        Returns:
            np.ndarray: (n, n) prior covariance matrix.
        """
        return prior_cov_params * np.identity(self.mean.shape[0]) - self.cov

    def estimate_posterior_cov(
        self, prior_cov: np.ndarray = None, prior_mean: np.ndarray = None
    ) -> np.ndarray:
        """Estimate the posterior covariance matrix.

        Args:
            prior_cov (np.ndarray, optional): (n, n) prior covariance matrix. Defaults to None.
            prior_mean (np.ndarray, optional): (n,) array of prior means. Defaults to None.

        Returns:
            np.ndarray: (n, n) posterior covariance matrix.
        """
        prior_mean, prior_cov = self._get_prior_mean_cov(prior_mean, prior_cov)

        # variance due to uncertainty in estimate of posterior mean
        post_mean_uncertainty = super().estimate_posterior_cov(prior_cov)

        # variance due to uncertainty in estimate of prior mean
        xi = self._compute_xi(prior_cov)
        X_T = self.X.T
        tau_inv = np.linalg.inv(prior_cov + self.cov)
        prior_mean_uncertainty = (
            xi @ self.X @ np.linalg.inv(X_T @ tau_inv @ self.X) @ X_T @ xi
        )

        # variance due to uncertainty in estimate of prior covariance
        error = (self.mean - prior_mean).reshape(-1, 1)
        prior_cov_uncertainty = (
            xi @ error @ error.T @ xi * 2 / (self.mean.shape[0] - self.X.shape[1] - 2)
        )

        return post_mean_uncertainty + prior_mean_uncertainty + prior_cov_uncertainty

    def _estimate_prior_params(self) -> Tuple[np.ndarray, float]:
        """Estimate prior mean and covariance parameters.

        Returns:
            Tuple[np.ndarray, float]: (p,) array of prior mean parameters, prior
                covariance parameter.
        """
        prior_mean_params = np.linalg.inv(self.X.T @ self.X) @ self.X.T @ self.mean
        prior_mean = self.estimate_prior_mean(prior_mean_params)
        prior_cov_params = ((self.mean - prior_mean) ** 2).sum() / (
            self.mean.shape[0] - self.X.shape[1] - 2
        )
        min_prior_cov_params = self._find_min_prior_cov_params()
        if min_prior_cov_params > prior_cov_params:
            warnings.warn(
                f"The prior variance parameter given by the James-Stein estimator {prior_cov_params} implies the prior covariance matrix is not positive semi-definite. Increasing the prior variance parameter to {min_prior_cov_params}.",
                RuntimeWarning,
            )
            prior_cov_params = min_prior_cov_params
        return prior_mean_params, prior_cov_params

    def _find_min_prior_cov_params(
        self,
        bounds: Tuple[float, float] = (0, np.inf),
        i: int = 0,
        prev_prior_cov_params: float = None,
        tol: float = 1e-6,
        max_iter: int = 100,
    ):
        """Find the minimum prior covariance parameter such that the prior covariance
        matrix is PSD.

        Args:
            bounds (Tuple[float, float], optional): Current boundaries in which the
                minimum prior cov parameter could be. Defaults to (0, np.inf).
            i (int, optional): Iteration. Defaults to 0.
            prev_prior_cov_params (float, optional): Prior covariance parameter from
                the previous iteration. Defaults to None.
            tol (float, optional): Stopping criteria. Defaults to 1e-6.
            max_iter (int, optional): Stopping criteria. Defaults to 100.
        """

        def get_prior_cov_params():
            if bounds == (0, np.inf):
                return 1
            elif bounds[1] == np.inf:
                return 2 * bounds[0]
            else:
                return 0.5 * (bounds[0] + bounds[1])

        prior_cov_params = get_prior_cov_params()
        if (
            prev_prior_cov_params is not None
            and abs(prev_prior_cov_params - prior_cov_params) < tol
        ) or i == max_iter:
            return bounds[1]
        prior_cov = self.estimate_prior_cov(prior_cov_params)
        try:
            # if this succeeds, the prior covariance matrix is PSD
            np.linalg.cholesky(prior_cov)
            bounds = bounds[0], prior_cov_params
        except:
            bounds = prior_cov_params, bounds[1]
        return self._find_min_prior_cov_params(bounds, i + 1, prior_cov_params)
