from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import SplineTransformer
from sklearn.utils import check_array
from sklearn.utils.validation import FLOAT_DTYPES, check_is_fitted


class MonotonicSplineTransformer(TransformerMixin, BaseEstimator):
    """The `MonotonicSplineTransformer` integrates the output of the `SplineTransformer` in an attempt to make monotonic features.

    This estimator is heavily inspired by [this blogpost](https://matekadlicsko.github.io/posts/monotonic-splines/) by Mate Kadlicsko.

    Parameters
    ----------
    n_knots : int, default=3
        The number of knots to use in the spline transformation.
    degree : int, default=3
    knots: str, default="uniform"

    Attributes
    ----------
    spline_transformer_ : trained SplineTransformer

    Examples
    --------
    ```py
    ```
    """

    def __init__(self, n_knots=3, degree=3, knots="uniform"):
        self.n_knots = n_knots
        self.degree = degree
        self.knots = knots

    def fit(self, X, y=None):
        """Fit the `MonotonicSplineTransformer` transformer by computing the spline transformation of `X`.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data to transform.
        y : array-like of shape (n_samples,), default=None
            Ignored, present for compatibility.

        Returns
        -------
        self : MonotonicSplineTransformer
            The fitted transformer.

        Raises
        ------
        ValueError
            If `X` contains non-numeric columns.
        """
        X = check_array(X, copy=True, force_all_finite=False, dtype=FLOAT_DTYPES, estimator=self)

        # If X contains infs, we need to replace them by nans before computing quantiles
        self.spline_transformer_ = SplineTransformer(n_knots=self.n_knots, degree=self.degree, knots=self.knots)
        self.spline_transformer_.fit(X)
        return self

    def transform(self, X):
        """Performs the Ispline transformation on `X`.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)

        Returns
        -------
        X : np.ndarray of shape (n_samples, n_out)
            Transformed `X` values.

        Raises
        ------
        ValueError
            If the number of columns from `X` differs from the number of columns when fitting.
        """
        check_is_fitted(self, "spline_transformer_")
        X = check_array(
            X,
            force_all_finite=False,
            dtype=FLOAT_DTYPES,
            estimator=self,
        )
        return self.spline_transformer_.transform(X).cumsum(axis=0)