import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from ._commons import check_dist, COLOR_SCHEME


class ScoreHistogram:
    """
    The ScoreHistogram class builds an approximate representation of the
    credit score distribution. It divides the data into "bins" (or "buckets")
    (that is, divide the entire range of values into a series of intervals)
    and then count how many values fall into each interval. The bins
    (intervals) must be adjacent and are often (but not required to be)
    of equal size. The ScoreHistogram class also provides the delinquency
    rate for each plotted bin.

    Attributes
    ----------
    population : np.array
        The scores volume/percentage for each interval/bin.
    delinquency_rate : np.array
        The calculated delinquency rate for each interval.

    Methods
    -------
    plot(title:str=None, subtitle:str=None, smooth_delinquency:bool=True, fontsize:int=12,
         bar_width:float=0.85, ax:matplotlib.axes._axes.Axes=None):
        Create a histogram plot.
    """
    def __init__(self,
                 scores: np.array,
                 targets: np.array = None,
                 bins: int = 10,
                 homogeneous: bool = False,
                 accumulated_delinquency: bool = False,
                 class_1: str = 'regular'):
        """
        The ScoreHistogram class provides a credit score histogram which
        can be combined with a delinquency rate.

        The ScoreHistogram class help to plot the following plots:
            - Credit score distribution;
            - Credit score distribution + delinquency rate per bin;
            - Credit score distribution + accumulated delinquency rate per bin;
            - Homogeneous Credit score distribution (bins of equal size as
        deciles);
            - Homogeneous Credit score distribution (bins of equal size as
        deciles) + delinquency rate per bin;
            - Homogeneous Credit score distribution (bins of equal size as
        deciles) +  accumulated delinquency rate per bin;

        Parameters
        ----------
        targets : np.array, optional
            The target of each instance of the `scores` parameter. It must be a
            Numpy array with binary values (0 or 1), by default None. By default,
            the positive class stands for "Regular customer/good payer".
        scores : np.array
            Credit score distributions. It must be a Numpy array with values
            between 0.0 and 1.0 or even 0.0 and 100.0.
        bins : int, optional
            The number of intervals to split the credit score distribution
            (`scores` parameter), by default 10.
        homogeneous : bool, optional
            Whether split distribution in deciles or not, by default False.
        accumulated_delinquency : bool, optional
            If True, it will calculate the accumulated delinquency rate
            descending over ascending bins, by default False.
        class_1 : str, optional
            Set the positive class for delinquency rate calculation,
            by default 'regular'.
        """
        self._bins = bins
        self._hom = homogeneous
        self._acc = accumulated_delinquency
        self._breakpoints = np.arange(0, self._bins + 1) / self._bins
        self._mask = None
        self._class_1 = class_1
        self.population = scores
        self.samples = len(scores)
        self.delinquency_rate = targets

    @property
    def population(self) -> np.array:
        """
        Getter method. It'll get the population for each interval.

        Returns
        -------
        np.array
            The population percentage for each interval/bin.
        """
        return self.__population

    @population.setter
    def population(self, value: np.array):
        """
        Setter method. It'll calculate the population percentage for each
        interval.

        Parameters
        ----------
        value : np.array
            Raw scores array.
        """
        dist = check_dist(value)  # validates the received distribution

        # If ScoreHistogram will plot the scores in a homogeneous way, then
        # the received raw score distribution should be split in quantiles.
        if self._hom:
            self._breakpoints = np.hstack((self._breakpoints[0], [
                np.quantile(dist, self._breakpoints[edge])
                for edge in range(1,
                                  len(self._breakpoints) - 1)
            ], self._breakpoints[-1]))

        # Creates the histogram and adjusts the decimals view
        self.__population = np.round(
            np.histogram(dist, self._breakpoints)[0] / len(dist), 4)

        # Gets the indices of each interval to then allow the delinquency rate
        # proper calc
        self._mask = np.digitize(
            dist, self._breakpoints,
            right=False) / self._bins  # right=False means i-1 <= x < i

    @property
    def delinquency_rate(self) -> np.array:
        """
        Getter method for delinquency_rate. It'll get the calculated
        delinquency_rate for each interval.

        Returns
        -------
        np.array
            Calculated delinquency rate for each interval.
        """
        return self.__delinquency_rate

    @delinquency_rate.setter
    def delinquency_rate(self, value: np.array):
        """
        Setter method. It'll calculate the delinquency rate for each score
        interval.

        Parameters
        ----------
        value : np.array
            Raw binary targets.

        Raises
        ------
        ValueError
            If the received value is not a binary array.
        """
        if value is not None:
            if value.size == 0 or not np.array_equal(value,
                                                     value.astype(bool)):
                raise ValueError(
                    'The target must contains only zeros and ones!')

            if self._class_1 not in ['delinquent', 'regular']:
                raise ValueError('Invalid value for class_1: {0}'.format(
                    self._class_1))

            if self._acc:  # Accumulated delinquency rate case
                if self._class_1 == 'regular':
                    aux = np.array([
                        len(value[(self._mask == (i + 1) / self._bins)]) -
                        (value[(self._mask == (i + 1) / self._bins)].sum())
                        for i in range(self._bins)
                    ])  # Gets the delinquents quantity for each bin
                else:
                    aux = np.array([
                        (value[(self._mask == (i + 1) / self._bins)].sum())
                        for i in range(self._bins)
                    ])  # Gets the delinquents quantity for each bin

                aux = np.cumsum(np.flip(aux))  # Gets the accumulated sum

                # Restores the array order and then get the delinquency
                # percentage for each bin
                aux = np.flip(aux) / len(value)
            else:  # The common delinquency rate calc case
                if self._class_1 == 'regular':
                    aux = np.array([
                        1 -
                        (value[(self._mask == (i + 1) / self._bins)].mean())
                        for i in range(self._bins)
                    ])  # Gets the delinquents percentage for each bin
                else:
                    aux = np.array([
                        (value[(self._mask == (i + 1) / self._bins)].mean())
                        for i in range(self._bins)
                    ])  # Gets the delinquents percentage for each bin

            # Replace any possible NaN to a valid number (it may occur when
            # one bin is empty).
            self.__delinquency_rate = np.nan_to_num(aux).round(4)
        else:
            self.__delinquency_rate = None

    def __make_plot_title(self, title: str, subtitle: str):
        """Auxiliary function to plot()"""

        base = "Score Histogram"
        subtitle = '\n' + subtitle if subtitle else '\nSamples: {:,}'.format(
            self.samples)

        if self._hom:
            base = "Homogeneous " + base
        if self._acc:
            base += " with Accumulated Delinquency rate"

        return (title if title else base) + subtitle

    def plot(self,
             title: str = None,
             subtitle: str = None,
             smooth_delinquency: bool = True,
             fontsize: int = 12,
             bar_width: float = 0.85,
             ax: plt.Axes = None,
             show_abs: bool = None):
        """
        Create a histogram plot.

        Parameters
        ----------
        title : str, optional
            Set the plot title. If None, it will be automatically generated,
            by default None.
        subtitle : str, optional
            Set the plot subtitle. If None, it will be automatically generated,
            by default None.
        smooth_delinquency : bool, optional
            Smooth the delinquency range line or not, by default True.
        fontsize : int, optional
            Base font size to be used in the plot texts, by default 12.
        bar_width : float, optional
            Bins width, by default 0.85.
        ax : plt.Axes, optional
            Matplotlib axis to export the plot, by default None.
        show_abs : bool, optional
            Show absolute values under graph, by default None.
        """
        if ax is None:
            _, ax = plt.subplots(figsize=(12, 6), facecolor=(1, 1, 1), dpi=60)

        x = np.arange(self._bins)

        samples_by_group = [
            round(self.samples * percentage) for percentage in self.population
        ]
        # Plot the blue bars
        ax.bar(x,
               self.population,
               width=bar_width,
               color=COLOR_SCHEME["primary"],
               zorder=3)

        for ix, v, s in zip(x, self.population, samples_by_group):
            ax.annotate("{:.2%}".format(v), (ix, v),
                        fontsize=fontsize - 2,
                        color=COLOR_SCHEME["primary"],
                        xytext=(1.5, 5),
                        textcoords="offset points",
                        ha="center",
                        va="bottom",
                        fontweight="bold",
                        rotation=90 if self._bins > 10 else 0)
            if show_abs:
                ax.annotate("{:,}".format(s), (ix, 0),
                            fontsize=fontsize - 2,
                            color=COLOR_SCHEME["primary"],
                            xytext=(1.5, -35),
                            textcoords="offset points",
                            ha="center",
                            va="bottom",
                            rotation=90 if self._bins > 10 else 0)

        # Plot the delinquency rate curve
        all_axis = [ax]
        if self.delinquency_rate is not None:
            ax2 = ax.twinx()
            ax2.tick_params("y",
                            colors=COLOR_SCHEME["secondary"],
                            labelsize=fontsize)

            ax2.set_ylabel('Delinquency Rate', {
                'size': fontsize,
                'color': COLOR_SCHEME["secondary"],
            })
            all_axis += [ax2]
            if smooth_delinquency:
                x_new = np.linspace(x.min(), x.max(), 1000)
                spl = make_interp_spline(x, self.delinquency_rate, k=2)
                y_new = spl(x_new)
                ax2.plot(x_new,
                         y_new,
                         linewidth=4,
                         color=COLOR_SCHEME["secondary"],
                         zorder=4)
            else:
                ax2.plot(x,
                         self.delinquency_rate,
                         linewidth=4,
                         color=COLOR_SCHEME["secondary"],
                         zorder=4)

            for ix, v, s in zip(x, self.delinquency_rate, samples_by_group):
                current_group_samples = round(v * s)
                ax2.annotate(
                    "{:.2%}".format(v),
                    (ix, v),
                    color=COLOR_SCHEME["aux_1"],
                    xytext=(0, 0),
                    textcoords="offset points",
                    ha="center",
                    fontsize=fontsize - 3,
                    fontweight="bold",
                    bbox=dict(
                        boxstyle="round, pad=0.35",
                        fc=COLOR_SCHEME["secondary"],
                        ec=COLOR_SCHEME["secondary"],
                        linewidth=1,
                        alpha=1,
                    ),
                    zorder=5,
                )
                # If self._acc is != None, show_abs breaks for delinquency.
                # TO-DO: Check it later.
                if show_abs and not self._acc:
                    ax2.annotate("{:,}".format(current_group_samples), (ix, 0),
                                 fontsize=fontsize - 2,
                                 color=COLOR_SCHEME["secondary"],
                                 xytext=(1.5, -50),
                                 textcoords="offset points",
                                 ha="center",
                                 va="bottom",
                                 rotation=90 if self._bins > 10 else 0)

        # Adjust plot settings
        xticks = [
            "[{:.0f}, {:.0f})".format(self._breakpoints[i - 1] * 100,
                                      self._breakpoints[i] * 100)
            for i in range(1, len(self._breakpoints))
        ]
        xticks[-1] = xticks[-1][:-1] + "]"

        ax.set_xticks(x)
        ax.set_xticklabels(xticks, rotation=45 if self._bins > 10 else 0)
        ax.tick_params("y", colors=COLOR_SCHEME["primary"], labelsize=fontsize)
        ax.tick_params("x", colors=COLOR_SCHEME["primary"], labelsize=fontsize)

        for axis in all_axis:
            axis.set_ylim(0)
            axis.set_yticks(axis.get_yticks().tolist())
            axis.set_yticklabels(
                ["{:.0%}".format(x) for x in axis.get_yticks()])
            axis.spines["top"].set_visible(False)
            axis.spines["bottom"].set_visible(False)
            axis.spines["right"].set_visible(True if len(all_axis) ==
                                             2 else False)
            axis.spines["left"].set_color(COLOR_SCHEME["primary"])
            axis.spines["right"].set_color(COLOR_SCHEME["secondary"])

        ax.set_title(self.__make_plot_title(title, subtitle),
                     {'size': fontsize + 2})

        ax.set_ylabel('Population', {
            'size': fontsize,
            'color': COLOR_SCHEME["primary"],
        })
