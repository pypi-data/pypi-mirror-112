import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
import numpy as np
from scipy.interpolate import make_interp_spline
from ._commons import check_dist, COLOR_SCHEME


class PSI:
    """
    It is a metric to measure how much a variable has shifted in
    distribution between two samples over time. It is widely used for monitoring
    changes in the characteristics of a population and for diagnosing possible
    problems in model performance. It’s good to indicate if the
    model has stopped predicting accurately due to significant changes in the
    population distribution.

    A PSI value of 0 implies the two analyzed distributions are identical
    with the PSI increasing in value as the two distributions diverge. One way
    to interpret these provided values is as follow:
        - If PSI <= 10%, then it means that there is no significant change;
        - If 10% < PSI <= 25%, then it indicates a small change, requiring
    investigation; and
        - If PSI > 25%, then it means that we have a significant change
    between the distributions.

    Methods
    -------
    value() -> float:
        This method returns the PSI value.

    plot(label_a:str="Dist A", label_b:str="Dist B", title:str=None,
    fontsize:int=12, bar_width:float=0.4, ax:matplotlib.axes._axes.Axes=None):
        This method plots the two distributions and the partial PSI
        along with bins.
    """
    def __init__(self, dist_a: np.array, dist_b: np.array, bins: int = 10):
        """
        Population Stability Index (PSI) Class to compare two distributions.

        Parameters
        ----------
        dist_a : np.array
            The first distribution to be compared (referential).
        dist_b : np.array
            The second distribution to be compared (observed).
        bins : int, optional
            Quantity of intervals, by default 10.
        """
        self._dist_a = check_dist(dist_a)
        self._dist_b = check_dist(dist_b)
        self._bins = bins
        self.breakpoints = (np.arange(0, self._bins + 1) / self._bins
                            )  # Calculate each breakpoint (intervals)
        self.percents = [
            np.histogram(dist, self.breakpoints)[0] / dist.shape[0]
            for dist in [self._dist_a, self._dist_b]
        ]  # Gets the instances qty for each breakpoint

    def calculate(self) -> np.array:
        """
        Calculate the PSI for each bin/interval.

        Returns
        -------
        np.array
            Array with index (partial PSI) for each bin.
        """
        pa, pb = self.percents

        # This is the solution to outline the problem with empty bins and later, with log(0)
        # The solution is poor, but it's the only one till now
        pa[pa <= 0] = 0.000000001
        pb[pb <= 0] = 0.000000001

        with np.errstate(invalid='ignore'):
            psi = (pa - pb) * np.log(pa / pb)

        return np.nan_to_num(psi)

    @property
    def value(self) -> float:
        """
        Return the psi value.

        Returns
        -------
        float
            PSI value.
        """
        psi_values = self.calculate()

        return psi_values.sum()

    def plot(self,
             label_a: str = "Dist A",
             label_b: str = "Dist B",
             title: str = None,
             fontsize: int = 12,
             bar_width: float = 0.4,
             ax: plt.Axes = None):
        """
        Plot both distributions and the partial PSI along with bins.

        Parameters
        ----------
        label_a : str, optional
            Distribution A label in graph, by default "Dist A".
        label_b : str, optional
            Distribution B label in graph, by default "Dist B".
        title : str, optional
            Plot title. If None, it will be automatically generated,
            by default None.
        fontsize : int, optional
            Base font size to be used in the plot texts, by default 12.
        bar_width : float, optional
            Width of each bin, by default 0.4.
        ax : plt.Axes, optional
            Matplotlib axis to export the plot, by default None.
        """
        if ax is None:
            _, ax = plt.subplots(figsize=(12, 6), facecolor=(1, 1, 1), dpi=60)

        x = np.arange(self._bins)
        psi_x = np.linspace(x.min(), x.max(), 300)  # More `x` points
        psi_y = make_interp_spline(x, self.calculate(),
                                   k=2)(psi_x)  # Smothed psi line

        ticks = [
            "[{:.0f}, {:.0f})".format(self.breakpoints[i - 1] * 100,
                                      self.breakpoints[i] * 100)
            for i in range(1, len(self.breakpoints))
        ]

        # Plot blue bars for Dist A
        ax.bar(x - bar_width / 2,
               self.percents[0],
               bar_width,
               zorder=2,
               color=COLOR_SCHEME['primary'],
               alpha=0.8,
               label=label_a)

        # Plot red bars for Dist B
        ax.bar(x + bar_width / 2,
               self.percents[1],
               bar_width,
               zorder=2,
               color=COLOR_SCHEME['secondary'],
               alpha=0.8,
               label=label_b)

        # Plot PSI line
        ax.plot(psi_x,
                psi_y,
                linewidth=3,
                color=COLOR_SCHEME['aux_5'],
                label='Distributed PSI')

        ax.fill_between(psi_x,
                        psi_y,
                        color=COLOR_SCHEME['aux_5'],
                        zorder=4,
                        alpha=0.7)

        # Plot partial PSI points
        ax.plot(x,
                self.calculate(),
                'o',
                color=COLOR_SCHEME['aux_5'],
                zorder=5)

        for ix, v in zip(x, self.calculate()):
            ax.annotate("{:.2%}".format(v), (ix, v),
                        xytext=(1.5, 5),
                        textcoords="offset points",
                        fontsize=fontsize - 2,
                        color='black',
                        ha='center',
                        va='bottom')

        # Adjust plot settings
        ax.set_ylim(0)
        ax.set_xticks(x)
        ax.set_yticks(ax.get_yticks().tolist())
        ax.set_xticklabels(ticks)
        ax.set_yticklabels(['{:.1%}'.format(x) for x in ax.get_yticks()], )
        ax.tick_params("y", labelsize=fontsize - 2)
        ax.tick_params("x", labelsize=fontsize - 2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y', color='black', linestyle=':', alpha=.3, zorder=0)
        ax.legend(loc='best')

        ax.set_title(
            "Population Stability Index (PSI) = {value:.2%}".format(
                value=self.value) if title is None else title,
            {'size': fontsize + 2})
