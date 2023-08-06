import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patheffects as patheffects
import numpy as np
from ._commons import check_dist, COLOR_SCHEME
from sklearn.metrics import auc, roc_curve


class ROC:
    """
    The ROC (Receiver Operating Characteristic) curve is a graph showing the
    performance of a classification model at all classification thresholds. This
    curve plots two parameters: the True Positive Rate (TPR) and the False
    Positive Rate (FPR), along with the AUC (Area Under the Curve) to show and
    compute the area under the ROC curve.

    Attributes
    ----------
    auc : float
        Area under the curve value.
    optimal_threshold : float
        It is the maximum difference between TPR and FPR.
    tpr : np.array
        Returns the true positive rate points used to plot the ROC.
    fpr : np.array
        Returns the false positive rate points used to plot the ROC.

    Methods
    -------
    plot(title:str=None, fontsize:int=12, legend_loc='lower right',
        ax:matplotlib.axes._axes.Axes=None):
        This method plots the ROC curve and AUC graph.
    """
    def __init__(self, scores: np.array, targets: np.array):
        """
        This class plots the ROC curve graphic, AUC, and calculates the
        optimal threshold for a binary classifier.

        Parameters
        ----------
        scores : np.array
            Credit score distributions. It must be a Numpy array with values
            between 0.0 and 1.0 or even 0.0 and 100.0.
        targets : np.array
            The target of each instance of the `scores` parameter. It must be a
            Numpy array with binary values (0 or 1). By default, the positive class
            stands for "Regular customer/good payer".
        """
        self._scores = check_dist(scores)
        self._targets = targets
        self.fpr, self.tpr, self._thresholds = roc_curve(
            self._targets, self._scores)
        self.auc = auc(self.fpr, self.tpr)
        self._opt_threshold_index = np.argmax(self.tpr - self.fpr)
        self.optimal_threshold = self._thresholds[self._opt_threshold_index]

    @property
    def _targets(self) -> np.array:
        """
        Getter method for targets.

        Returns
        -------
        np.array
            Validated targets distribution.
        """
        return self.___targets

    @_targets.setter
    def _targets(self, value: np.array):
        """
        Setter for targets distribution.

        Parameters
        ----------
        value : np.array
            Raw binary targets.

        Raises
        ------
        ValueError
            Occurs when the target distribution does not fit with the required
            pattern.
        """
        if value.size == 0 or not np.array_equal(value, value.astype(bool)):
            raise ValueError('The target must contains only zeros and ones!')
        else:
            self.___targets = value

    def plot(self,
             title: str = None,
             fontsize: int = 12,
             legend_loc: str = 'lower right',
             ax: plt.Axes = None):
        """
        Method to plot the ROC curve and AUC.

        Parameters
        ----------
        title : str, optional
            Set the plot title. If None, it will be automatically generated,
            by default None.
        fontsize : int, optional
            Base font size to be used in the plot texts, by default 12.
        ax : plt.Axes, optional
            Matplotlib axis to export the plot, by default None.
        """
        if ax is None:
            _, ax = plt.subplots(figsize=(6, 4), facecolor=(1, 1, 1), dpi=90)

        # The following lines gonna be responsible for drawing the colorful ROC
        points = np.array([self.fpr, self.tpr]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        cmap = plt.get_cmap("coolwarm")
        lc = LineCollection(
            segments,
            array=self._thresholds,
            cmap=cmap,
            norm=plt.Normalize(0.0, 1.0),
            linewidth=5,
            alpha=1.0,
            zorder=4,
        )
        ax.add_collection(lc)

        # This next lines will add the threshold ColorBar
        cb = plt.colorbar(lc, ax=ax, label="Thresholds")
        cb.outline.set_linewidth(0)

        # The following lines gonna draw the aux lines
        ax.vlines(
            self.fpr[self._opt_threshold_index],
            0,
            self.tpr[self._opt_threshold_index],
            color=COLOR_SCHEME['aux_5'],
            zorder=3,
            linestyles=":",
        )

        ax.hlines(
            self.tpr[self._opt_threshold_index],
            0,
            self.fpr[self._opt_threshold_index],
            color=COLOR_SCHEME['aux_5'],
            zorder=3,
            linestyles=":",
            label="Optimal Threshold: {:.2f}".format(self.optimal_threshold)
            if self.optimal_threshold < 1.0 else "Optimal Threshold: 1.0",
        )

        ax.plot(
            [0, 1],
            [0, 1],
            "k--",
            lw=1.5,
            color=COLOR_SCHEME['aux_4'],
            alpha=0.7,
            zorder=2,
            label="Random guess",
        )

        # Draw the AUC
        ax.fill_between(
            self.fpr,
            self.tpr,
            facecolor=COLOR_SCHEME['aux_3'],
            alpha=0.45,
            zorder=1,
            label="Area Under The Curve: {:.2%}".format(self.auc),
        )

        # Insert the ROC Curve threshold labels
        for k in range(len(self.tpr) - 1):
            if k % int(len(self._thresholds) / 10) == 0:
                ax.annotate(
                    str(np.round(self._thresholds[1:][k], 2)),
                    (self.fpr[k], self.tpr[k]),
                    path_effects=[
                        patheffects.withStroke(linewidth=3, foreground="white")
                    ],
                    xytext=(0, 0),
                    fontsize=fontsize - 3,
                    textcoords="offset points",
                    ha="center",
                    zorder=5,
                )

        # Adjust plot settings
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlim(-0.05, 1.05)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_bounds(0, 1)
        ax.spines["left"].set_bounds(0, 1)
        ax.tick_params("y", labelsize=fontsize - 2)
        ax.tick_params("x", labelsize=fontsize - 2)

        ax.set_title(
            "Receiver Operating Characteristic Curve"
            if title is None else title,
            {
                "size": fontsize,
            },
        )

        ax.set_ylabel(
            "True Positive Rate",
            {
                "size": fontsize - 2,
            },
        )
        ax.set_xlabel(
            "False Positive Rate",
            {
                "size": fontsize - 2,
            },
        )

        ax.legend(loc=legend_loc,
                  bbox_to_anchor=(0.95, 0.05),
                  fontsize=fontsize - 4)
