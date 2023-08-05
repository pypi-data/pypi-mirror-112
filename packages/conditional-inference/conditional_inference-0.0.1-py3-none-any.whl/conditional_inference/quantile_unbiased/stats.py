from __future__ import annotations

from ..base import Numeric1DArray
from ..utils import convert_to_array

import warnings
import textwrap
from typing import Any, Callable, List, Tuple, Union

import numpy as np
from scipy.misc import derivative
from scipy.optimize import fsolve
from scipy.stats import norm, rv_continuous


def truncated_cdf(  # pylint: disable=invalid-name,too-many-arguments
    x: Union[float, Numeric1DArray],
    truncation_set: List[Tuple[float, float]] = None,
    loc: float = 0,
    scale: float = 1,
    cdf: Callable[[Numeric1DArray], np.ndarray] = norm.cdf,
    projection_interval: Union[float, Tuple[float, float]] = (-np.inf, np.inf),
) -> np.ndarray:
    """Computed the truncated cumulative distribution function.

    Args:
        x (Union[float, Numeric1DArray]): (n,) array of values at which the truncated CDF is
            evaluated.
        truncation_set (List[Tuple[float, float]]): List of real-valued intervals of the truncation
            set. If ``None``, will use ``[(-np.inf, np.inf)]``. Defaults to None.
        loc (float, optional): Used to shift the distribution. Defaults to 0.
        scale (float, optional): Used to scale the distribution. Defaults to 1.
        cdf (Callable[[Numeric1DArray], np.ndarray], optional): The untruncated CDF. Defaults to
            norm.cdf.
        projection_interval (Union[float, Tuple[float, float]], optional): The projection interval
            centered on 0. The final truncation set is the intersection of `truncation_set` and the
            projection interval. If `float`, the projection interval is assumed to be symmetric
            around 0. Defaults to (-np.inf, np.inf).

    Returns:
        np.ndarray: (n,) array of the truncated CDF evaluated at `x`.

    Examples:
        Compute the CDF evaluated at 1 of a normal truncated to the union of the intervals (-2, -1), (0, 2).

        .. doctest::

            >>> from conditional_inference.quantile_unbiased import truncated_cdf
            >>> truncated_cdf(1, truncation_set=[(-2, -1), (0, 2)])
            array([0.77835111])
    """

    def clip_truncation_set(projection_interval):
        # take the intersection of the truncation set and projection interval centered on `loc`
        if np.isscalar(projection_interval):
            projection_interval = (-abs(projection_interval), abs(projection_interval))
        intersection = []
        for interval in truncation_set:
            if interval[1] < interval[0]:
                raise ValueError(
                    textwrap.fill(
                        textwrap.dedent(
                            f"""Invalid interval {interval}: upper bound is below the lower bound.
                """
                        )
                    )
                )
            clipped_interval = (
                max(interval[0], loc + projection_interval[0]),
                min(interval[1], loc + projection_interval[1]),
            )
            if clipped_interval[0] < clipped_interval[1]:
                intersection.append(clipped_interval)
        return intersection

    def get_truncation_bounds():
        # convert truncation set to 2 vectors for the 1) lower and 2) upper bounds of the
        # truncation set invervals
        if not truncation_set:
            warnings.warn("Empty truncation set", RuntimeWarning)
            return None, None
        a, b = list(zip(*truncation_set))
        a, b = convert_to_array(a), convert_to_array(b)
        if not np.array([(a >= a_i) | (a_i >= b) for a_i in a]).all():
            raise ValueError(
                f"Invalid intervals a={a}, b={b}: make sure your intervals do not overlap"
            )
        return normalize(a), normalize(b)

    def normalize(arr):
        # shift and scale the vectors
        return (arr - loc) / scale

    def handle_Z_eq_0():
        # handle the case where there is 0 probability that a value could fall within the
        # truncation set based on the untruncated CDF
        def convert_0_1(xi_i):
            # converts cdf to 0 or 1 depending on bounds and xi
            return alpha_min < xi_i if xi_i > 0 else beta_max < xi_i

        warnings.warn(
            "Truncation set contains none of the distribution; results may be incorrect",
            RuntimeWarning,
        )
        alpha_min, beta_max = alpha.min(), beta.max()
        return np.vectorize(convert_0_1)(xi).astype(float)

    def compute_truncated_cdf():
        # n x p indicates xi is above the upper bound of the interval
        idx = np.array([beta < xi_i for xi_i in xi])
        # n x 1 CDF for the intervals where xi is above the upper bound
        z_xi = idx @ (cdf(beta) - cdf(alpha))

        # n x p indicates xi is in the interval
        idx = np.array([(alpha < xi_i) & (xi_i < beta) for xi_i in xi])
        # n x p CDF of xi repeated p times
        xi_cdf = np.repeat(cdf(xi), alpha.shape[0]).reshape(xi.shape[0], alpha.shape[0])
        # n x 1 CDF of xi for the interval which contains it
        y_xi = (idx * (xi_cdf - cdf(alpha))).sum(axis=1)

        return (z_xi + y_xi) / Z

    if truncation_set is None:
        truncation_set = [(-np.inf, np.inf)]
    truncation_set = clip_truncation_set(projection_interval)
    alpha, beta = get_truncation_bounds()
    xi = normalize(convert_to_array(x))
    if alpha is None and beta is None:  # i.e., truncation set is empty
        return (loc < xi).astype(float)
    Z = (cdf(beta) - cdf(alpha)).sum()
    return handle_Z_eq_0() if Z == 0 else compute_truncated_cdf()


class cond_quant_unbiased(rv_continuous):  # pylint: disable=invalid-name
    """Conditional quantile-unbiased distribution.

    Inherits from `scipy.stats.rv_continuous <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html>`_  and handles standard public methods (``pdf``, ``cdf``, etc.). # pylint:disable=line-too-long

    Args:
        y (float): Value at which the truncated CDF is evaluated
        bounds (Tuple[float, float], optional): Lower and upper bounds of the support of the
            distribution. Defaults to (-np.inf, np.inf).
        dx (float): Used to numerically approximate the PDF.
        **truncated_cdf_kwargs (Any): Keyword arguments for :func:`truncated_cdf`.

    Attributes:
        y (float): Value at which the truncated CDF is evaluated.
        bounds (Tuple[float, float]): Lower and upper bound of the support of the distribution.
            Defaults to (-np.inf, np.inf).
        dx (float): Used to numerically approximate the PDF.
        truncated_cdf_kwargs (dict): Keyword arguments for :func:`truncated_cdf`.

    Examples:
        Compute a median-unbiased estimate of a normally distributed variable given that its
        observed value is 1 and falls between 0 and 3.

        .. doctest::

            >>> from conditional_inference.quantile_unbiased import cond_quant_unbiased
            >>> dist = cond_quant_unbiased(1, truncation_set=[(0, 3)])
            >>> dist.ppf(.5)
            0.7108033900602353
    """

    def __init__(
        self,
        y: float,
        bounds: Tuple[float, float] = (-np.inf, np.inf),
        dx: float = None,
        **truncated_cdf_kwargs: Any,
    ):
        super().__init__()
        self.y = y  # pylint: disable=invalid-name
        self.bounds = bounds
        self.truncated_cdf_kwargs = truncated_cdf_kwargs
        self._cdf_min = (
            0
            if bounds[0] == -np.inf
            else 1 - self._truncated_cdf(np.array([bounds[0]]))
        )
        if self._cdf_min >= 1:
            warnings.warn(
                "Untruncated CDF of lower bound == 1: try decreasing the lower bound",
                RuntimeWarning,
            )
        self._cdf_max = (
            1 if bounds[1] == np.inf else 1 - self._truncated_cdf(np.array([bounds[1]]))
        )
        if self._cdf_max <= 0:
            warnings.warn(
                "Untruncated CDF of upper bound == 0: try increasing the upper bound",
                RuntimeWarning,
            )
        self.dx = (  # pylint: disable=invalid-name
            np.diff(self.ppf([0.95, 0.05])) / 50 if dx is None else dx
        )

    @property
    def bounds(self):  # pylint: disable=missing-docstring
        # Potentially restrict the bounds of this distribution to ensure the truncation set and
        # projection interval overlap
        projection_interval = self.truncated_cdf_kwargs.get("projection_interval")
        truncation_set = self.truncated_cdf_kwargs.get("truncation_set")
        if projection_interval is None or truncation_set is None:
            return self._bounds
        if np.isscalar(projection_interval):
            projection_interval = (-abs(projection_interval), abs(projection_interval))
        a, b = zip(*truncation_set)  # pylint: disable=invalid-name
        return (
            max(self._bounds[0], np.min(a) - projection_interval[1]),
            min(self._bounds[1], np.max(b) - projection_interval[0]),
        )

    @bounds.setter
    def bounds(self, bounds):
        self._bounds = bounds

    def _truncated_cdf(  # pylint: disable=invalid-name
        self, x: np.ndarray
    ) -> np.ndarray:
        """Compute the truncated CDF evaluated at `self.y` with shift `x`."""
        return np.array(
            [
                truncated_cdf(self.y, loc=x_i, **self.truncated_cdf_kwargs)[0]  # type: ignore
                for x_i in x
            ]
        )

    def _cdf(self, x: np.ndarray) -> np.ndarray:  # pylint: disable=arguments-differ
        """Cumulative distribution function.

        Args:
            x (np.ndarray): (n,) array of values at which to evaluate the CDF.

        Returns:
            np.ndarray: (n,) array of evaluations.
        """
        if self._cdf_min >= 1 or self._cdf_max <= 0:

            def handle_cdf_out_of_bounds(x_i):
                return self.bounds[0] <= x_i if self.y < x_i else self.bounds[1] < x_i

            warnings.warn(
                textwrap.fill(
                    textwrap.dedent(
                        """
                Untruncated CDF of lower bound >= 1 or CDF of upper bound <= 0; results may be
                incorrect
            """
                    )
                )
            )

            return np.vectorize(handle_cdf_out_of_bounds)(x).astype(float)

        cdf = (1 - self._truncated_cdf(x) - self._cdf_min) / (
            self._cdf_max - self._cdf_min
        )
        return ((self.bounds[0] < x) & (x < self.bounds[1])) * cdf + (
            self.bounds[1] <= x
        ).astype(float)

    def _pdf(self, x: np.ndarray) -> np.ndarray:  # pylint: disable=arguments-differ
        """Probability density function.

        Args:
            x (np.ndarray): (n,) array of values at which to evaluate the PDF.

        Returns:
            np.ndarray: (n,) array of evaluations.
        """
        pdf = derivative(self._cdf, x, dx=self.dx, order=5)
        return ((self.bounds[0] < x) & (x < self.bounds[1])) * pdf

    def _ppf(self, q: np.ndarray) -> np.ndarray:  # pylint: disable=arguments-differ
        """See self.ppf."""

        def func(mu, q_i):
            return self._truncated_cdf(mu) - (1 - q_i)

        if self._cdf_min >= 1 or self._cdf_max <= 0:
            warnings.warn(
                textwrap.fill(
                    textwrap.dedent(
                        """
                Untruncated CDF of lower bound >= 1 or CDF of upper bound <= 0: results may be
                incorrect
            """
                    )
                )
            )

            val = self.bounds[0] if self.bounds[0] > self.y else self.bounds[1]
            return np.full(q.shape, val)
        q_t = q * (self._cdf_max - self._cdf_min) + self._cdf_min
        return [fsolve(func, [self.y], args=(q_i,))[0] for q_i in q_t]

    def ppf(  # pylint: disable=arguments-differ
        self, q: Union[float, Numeric1DArray]
    ) -> np.ndarray:
        """Percent point function.

        Args:
            q (np.ndarray): (n,) array of quantiles at which to evaluate the PPF.

        Returns:
            np.ndarray: (n,) array of evaluations.
        """
        return np.clip(super().ppf(q), *self.bounds)
