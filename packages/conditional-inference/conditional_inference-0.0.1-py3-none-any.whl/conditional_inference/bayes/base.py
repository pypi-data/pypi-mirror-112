"""Base classes and mixins for Bayesian analysis.
"""
from __future__ import annotations

from ..base import ModelBase, Numeric1DArray, ResultsBase, ColumnsType

from typing import Any

import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import norm, multivariate_normal


class BayesModelBase(ModelBase):
    """Mixin for Bayesian models. Inherits from :class:`conditional_inference.base.ModelBase`.

    Args:
        mean (Numeric1DArray): (n,) array of conventionally-estimated means.
        cov (np.ndarray): (n, n) covariance matrix.
        X (np.ndarray, optional): (n, p) feature matrix. If ``None``, a constant
            regressor will be used. Defaults to None.
        *args (Any): Passed to ``ModelBase``.
        **kwargs (Any): Passed to ``ModelBase``.

    Attributes:
        X (np.ndarray, optional): (n, p) feature matrix.

    Notes:
        This class also contains the attributes of ``ModelBase``.
    """

    def __init__(
        self,
        mean: Numeric1DArray,
        cov: np.ndarray,
        X: np.ndarray = None,
        *args: Any,
        **kwargs: Any
    ):
        super().__init__(mean, cov, *args, **kwargs)
        self.X = np.ones((mean.shape[0], 1)) if X is None else X

    def _compute_xi(self, prior_cov: np.ndarray) -> np.ndarray:
        """Compute xi; see paper for mathematical detail.

        Args:
            prior_cov (np.ndarray): (n, n) prior covariance matrix.

        Returns:
            np.ndarray: (n, n) weight matrix.
        """
        return self.cov @ np.linalg.inv(prior_cov + self.cov)


class BayesResults(ResultsBase):
    """Results of Bayesian analysis. Inherits from :class:`conditional_inference.base.ResultsBase`.

    Args:
        model (BayesModelBase): Model on which results are based.
        cols (ColumnsType): Columns of interest.
        params (np.ndarray): (n,) array of point estimates, usually the average posterior mean.
        cov_params (np.ndarray): (n, n) posterior covariance matrix.
        n_samples (int, optional): Number of samples to draw for approximations, such as likelihood calculations. Defaults to 1000.
        title (str, optional): Results title. Defaults to "Bayesian estimates".

    Attributes:
        params (np.ndarray): (n,) array of point estimates, usually the average posterior mean.
        cov_params (np.ndarray): (n, n) posterior covariance matrix.
        distributions (List[scipy.stats.norm]): Marginal posterior distributions.
        multivariate_distribution (scipy.stats.multivariate_normal): Joint posterior distribution.
        pvalues (np.ndarray): (n,) array of probabilities that the true mean is less than 0.
        posterior_mean_rvs (np.ndarray): (n_samples, n) matrix of draws from the posterior.
        rank_matrix (pd.DataFrame): (n, n) dataframe of probabilities that column i has rank j.

    Notes:
        This class also contains the attributes of ``ResultsBase``.
    """

    def __init__(
        self,
        model: BayesModelBase,
        cols: ColumnsType,
        params: np.ndarray,
        cov_params: np.ndarray,
        n_samples: int = 1000,
        title: str = "Bayesian estimates",
    ):
        super().__init__(model, cols, title)
        self.params = params[self.indices]
        self.cov_params = cov_params[self.indices][:, self.indices]
        self.distributions = [
            norm(params[k], np.sqrt(cov_params[k, k])) for k in self.indices
        ]
        self.pvalues = np.array([dist.cdf(0) for dist in self.distributions])
        if (abs(self.cov_params - self.cov_params[0, 0]) <= 1e-4).all():
            # policy effects are perfectly correlated
            # this occurs when prior covariance == 0
            self.multivariate_distribution = None
            err = norm(0, np.sqrt(self.cov_params[0, 0])).rvs(n_samples)
            self.posterior_mean_rvs = self.params + np.repeat(
                err.reshape(-1, 1), self.params.shape[0], axis=1
            )
        else:
            self.multivariate_distribution = multivariate_normal(
                self.params, self.cov_params
            )
            self.posterior_mean_rvs = self.multivariate_distribution.rvs(n_samples)
        self.sample_weight = 1 / self.posterior_mean_rvs.shape[0]
        self.rank_matrix = self._compute_rank_matrix()

    def likelihood(self, mean: Numeric1DArray, cov: np.ndarray) -> float:
        """Compute the likelihood of observing sample means.

        Args:
            mean (Numeric1DArray): (n,) array of sample means.
            cov (np.ndarray): (n, n) covariance matrix for sample means.

        Returns:
            float: Likelihood.
        """
        likelihood = np.array(
            [
                multivariate_normal(params, cov).pdf(mean)
                for params in self.posterior_mean_rvs
            ]
        )
        return (self.sample_weight * likelihood).sum()

    def rank_matrix_plot(self, title: str = None, *args: Any, **kwargs: Any):
        """Plot a heatmap of the rank matrix.

        Args:
            title (str, optional): Plot title. Defaults to None.
            *args (Any): Passed to ``sns.heatmap``.
            **kwargs (Any): Passed to ``sns.heatmap``.

        Returns:
            AxesSubplot: Heatmap.
        """
        ax = sns.heatmap(
            self.rank_matrix, center=1 / self.params.shape[0], *args, **kwargs
        )
        ax.set_title(title or self.title)
        return ax

    def _compute_rank_matrix(self) -> pd.DataFrame:
        """Compute the rank matrix

        Returns:
            pd.DataFrame: Rank matrix.
        """
        argsort = np.argsort(-self.posterior_mean_rvs, axis=1)
        rank_matrix = np.array(
            [
                ((argsort == k).T * self.sample_weight).sum(axis=1)
                for k in range(self.posterior_mean_rvs.shape[1])
            ]
        ).T
        rank_df = pd.DataFrame(
            rank_matrix, columns=[self.model.exog_names[k] for k in self.indices]
        )
        rank_df.index.name = "Rank"
        return rank_df
