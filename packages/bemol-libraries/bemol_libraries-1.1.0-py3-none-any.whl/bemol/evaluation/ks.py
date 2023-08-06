import matplotlib.pyplot as plt
import numpy as np
from ._commons import check_dist, COLOR_SCHEME
import typing
import warnings
from scipy.stats import kstest


class KolmogorovSmirnov:
    """
    Kolmogorov-Smirnov (KS) Statistics is a non-parametric test, which
    means you don't need to test any assumption related to the distribution,
    and is one of the most important metrics used for validating predictive models.
    KS is used to evaluate the risk differentiation ability of the model, and
    the indicator measures the difference between the cumulative segments of
    the good and bad samples. The KS can also be used to compare two distinct
    distribution (KS-1).

    Attributes
    ----------
    value : np.array
        Return the KS statistic value, it means the maximum difference between
        the cumulative segments of positive and negative samples.

    Methods
    -------
    plot(title=None, dist_labels=None, fontsize=12, legend_loc='lower right',
         ax:matplotlib.axes._axes.Axes=None):
        Method to plot the KS curves.
    """
    def __init__(self, dist_a: np.array, dist_b: np.array, ks_type: int = 2):
        """
        This class calculates the KS-1 or KS-2 statistic based on the two
        given distributions.

        This class assumes binary target distributions where label 1 is the
        positive class and label 0 is the negative class, e.g.,
        "Regular customer/good payer" and "the delinquent", respectively.

        The KS-1 is used to compare two distinct distributions. In the case
        of scores, it can be used to compare scores of two different cohorts.

        In contrast, the KS-2 (two-sample) is used to compare the cumulative
        distribution of Positive and Negative targets. It's an useful metric
        to evaluate credit models (or any other binary classification model),
        once it helps us to understand how well our predictive model is able
        to discriminate between events and non-events. To that, it needs two
        distributions: (a) scores array and (b) its targets.

        Parameters
        ----------
        dist_a : np.array
            Scores distribution array.
        dist_b : np.array
            In KS-1, the secondary scores distribution array; or
            In KS-2, the binary targets of `dist_a`.
        ks_type : int, optional
            KS calc type, by default 2
            Must be '1' for KS-1 or '2' for KS-2.
        """
        self.__type = ks_type
        self._dist_a = check_dist(dist_a)
        self._dist_b = check_dist(dist_b)

    @property
    def __type(self) -> int:
        """
        Getter method for KS type.

        Returns
        -------
        int
            It returns '1' or '2' integer value
        """
        return self.____type

    @__type.setter
    def __type(self, value: int):
        """
        Setter method. It'll help to define the K-S type, which may be KS-1
        or KS-2. This setter uses a string as an indicator ('1' or '2').

        Parameters
        ----------
        value : int
            KS type indicator. Must be 1 or 2.

        Raises
        ------
        ValueError
            Error when the received value isn't the expected string.
        """
        if isinstance(value, int) and value in [1, 2]:
            self.____type = value
        else:
            raise ValueError("Invalid KS type value. Must be '1' or '2'!")

    @property
    def _dist_b(self) -> np.array:
        """
        Getter method for `_dist_b` attribute.

        Returns
        -------
        np.array
            The secondary distribution to be used in KS calc.
        """
        return self.___dist_b

    @_dist_b.setter
    def _dist_b(self, value: np.array):
        """
        Setter method. It'll validate the secondary distribution for KS,
        according to calculus type. In KS-1, are expected two score
        distributions, while in KS-2 the secondary distribution is
        a binary targets array.

        Parameters
        ----------
        value : np.array
            Secondary raw distribution to be used in KS calc.

        Raises
        ------
        ValueError
            Raises this error whenever the method receives an invalid
            distribution for each KS type supported in this class.
        """
        if self.__type == 2 and not np.array_equal(value, value.astype(bool)):
            raise ValueError(
                'The `dist_b` parameter in KS-2 must be the binary targets array of `dist_a`!'
            )
        if self.__type == 1 and np.array_equal(value, value.astype(bool)):
            warnings.warn(
                "Using a binary array as `dist_b` for KS-1! If you are aware of this, ignore this warning"
            )

        self.___dist_b = value

    def _prepare_dists(self) -> typing.Tuple[np.array, np.array]:
        """
        Method to prepare `dist_a` and `dist_b` according to K-S type.

        If the class is set as KS-1, then both distributions gonna be merged
        into a single array, and the same shape targets array will be generated
        with ones to `dist_a` indices and zeros to `dist_b` indices.
        Otherwise, in the KS-2 setting, the `dist_a` remains the raw received
        scores distribution as well as `dist_b` with its targets.

        After this step, both distributions gonna be ordered according to
        `dist_a` (in KS-2) or `dist_a + dist_b` (in KS-1).

        Returns
        -------
        dist : np.array
            Ordered scores distribution.
        targets : np.array
            Targets distributions of `dist`.
        """
        if self.__type == 1:
            # Put both distributions together in an unique array
            dist = np.hstack((self._dist_a, self._dist_b))
            targets = np.hstack(
                (np.ones(self._dist_a.shape), np.zeros(self._dist_b.shape)))
        else:
            dist = self._dist_a
            targets = self._dist_b

        # Get a sorted index array
        _dist_indices_order = dist.argsort()
        dist = dist[_dist_indices_order]
        targets = targets[_dist_indices_order]

        return dist, targets

    def _calculate(
            self) -> typing.Tuple[np.array, np.array, np.array, np.array]:
        """
        Method to calculate the Kolmogorov–Smirnov statistic components.

        Returns
        -------
        dist : np.array
            Ordered scores distribution by `_prepare_dists` method.
        cdf : np.array
            The KS cumulative distribution function (CDF). It's the accumulated
            sum of negative targets divided by its total. It's used to calculate
            the K-S statistic besides plot one of its curves.
        ecdf : np.array
            The KS empirical cumulative distribution function (ECDF). It's the
            accumulated sum of positive targets divided by its total.  It's used
            to calculate the K-S statistic besides plot one of its curves.
        diff : np.array
            Difference between CDF and ECDF. The K-S statistic value is obtained
            as the maximum value of this difference.
        """
        dist, targets = self._prepare_dists()

        positive = targets == 1.0
        negative = ~positive

        ecdf = np.cumsum(positive) / positive.sum()
        cdf = np.cumsum(negative) / negative.sum()
        diff = cdf - ecdf

        return dist, cdf, ecdf, diff

    @property
    def value(self) -> float:
        """
        KS Statistic value getter.

        Returns
        -------
        float
            Return the KS value.
        """
        if self.__type == 2:
            _, _, _, diff = self._calculate()

            return diff.max().round(4)
        else:
            # For KS-1 use the statistic returned by `scipy.stats.kstest()`
            return round(
                kstest(self._dist_a,
                       self._dist_b,
                       alternative='two-sided',
                       mode='auto').statistic, 4)

    def plot(self,
             title: str = None,
             dist_labels: tuple = None,
             fontsize: int = 12,
             legend_loc: str = 'lower right',
             ax: plt.Axes = None):
        """
        Method to plot the KS curves.

        Parameters
        ----------
        title : str, optional
            Set the plot title. If None, it will be automatically generated,
            by default None
        dist_labels : tuple, optional
            Tuple with the labels of `dist_a` and `dist_b`. If None, it will be
            automatically generated, by default None
        fontsize : int, optional
            Base font size to be used in the plot texts, by default 11
        legend_loc : str, optional
            Matplotlib legend position, by default lower right
        ax : plt.Axes, optional
            Matplotlib axis to export the plot, by default None
        """
        dist, cdf, ecdf, diff = self._calculate()
        aux = "\n(KS-{}={:.2%})".format(self.__type, self.value)
        title = 'Kolmogorov–Smirnov Statistic' + aux if title is None else title

        if dist_labels is None:
            dist_labels = ('Delinquents',
                           'Regulars') if self.__type == 2 else ('Dist B',
                                                                 'Dist A')
        if ax is None:
            _, ax = plt.subplots(figsize=(6, 4), facecolor=(1, 1, 1), dpi=90)

        # Main plot
        ax.plot(dist,
                ecdf,
                lw=3,
                color=COLOR_SCHEME["primary"],
                label=dist_labels[1],
                zorder=3)

        ax.plot(dist,
                cdf,
                lw=3,
                color=COLOR_SCHEME["secondary"],
                label=dist_labels[0],
                zorder=3)

        # This calculations are needed in order to find the point of
        # separation in case of KS-1
        # (due to cumulative distribution of dist_a >= dist_b case)
        minS = np.clip(-np.min(diff), 0, 1)
        maxS = np.max(diff)
        max_diff = max(minS, maxS)

        ks1_idx = diff.argmax() if max_diff == maxS else diff.argmin()
        idx = ks1_idx if self.__type == 1 else diff.argmax()
        ax.axvline(
            dist[idx],
            ecdf[idx],
            cdf[idx],
            lw=1.5,
            linestyle="--",
            color="#000",
            zorder=2,
            label="KS={:.2%} at {:.2}".format(self.value, dist[idx]),
        )

        # Reassignment needed in case of KS-1
        # (due to cumulative distribution of dist_a >= dist_b case)
        aux_diff = diff if max_diff == maxS else -diff
        diff = diff if self.__type == 2 else aux_diff

        # Difference curve
        ax.fill_between(dist,
                        diff,
                        linewidth=1.5,
                        edgecolor=COLOR_SCHEME["aux_4"],
                        facecolor=COLOR_SCHEME["aux_3"],
                        alpha=0.4,
                        label="Difference",
                        zorder=1)

        # Graphic settings
        ax.grid(which="both",
                linestyle=":",
                color=COLOR_SCHEME["aux_4"],
                zorder=0,
                alpha=0.3)

        # Adjust plot settings
        ax.xaxis.set_ticks(np.arange(0.0, 1.1, 0.1))
        ax.yaxis.set_ticks(np.arange(0.0, 1.1, 0.1))
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.set_ylim(0, 1.0)
        ax.set_xlim(0, 1.0)
        ax.tick_params("y", labelsize=fontsize - 2)
        ax.tick_params("x", labelsize=fontsize - 2)

        ax.set_title(title, {
            'size': fontsize,
        })

        ax.set_xlabel("Cutoff", {
            'size': fontsize - 2,
        })

        ax.set_ylabel("Cumulative Propability", {
            'size': fontsize - 2,
        })

        ax.legend(loc=legend_loc, prop={
            'size': fontsize - 4,
        })
