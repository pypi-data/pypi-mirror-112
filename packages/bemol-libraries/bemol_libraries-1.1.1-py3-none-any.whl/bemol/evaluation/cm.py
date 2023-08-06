import typing
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from bemol.evaluation.roc import ROC
from sklearn.metrics import confusion_matrix
from ._commons import check_dist


class ConfusionMatrix:
    """
    A Confusion Matrix (CM) contains information about actual and predicted
    classifications done by a classification system. This class creates a CM for
    a binary classification problem.

    Attributes
    ----------
    threshold : float
        This parameter stores the threshold set in the class constructor, or the
        optimal threshold calculated by the ROC class, when a threshold is not
        provided.

    Methods
    -------
    compute() -> typing.Tuple[np.array, np.array]:
        This method returns the confusion matrix and its normalized version.

    plot(title:str=None, classes:list=['Bads', 'Goods'], fontsize:int=12,
         ax:matplotlib.axes._axes.Axes=None):
        This method plots the confusion matrix chart.
    """
    def __init__(self,
                 scores: np.array,
                 targets: np.array,
                 threshold: float = None):
        """
        This class creates a CM for a binary classification problem.

        Parameters
        ----------
        scores : np.array
            Credit score distributions. It must be a Numpy array with values
            between 0.0 and 1.0 or even 0.0 and 100.0.
        targets : np.array
            The target of each instance of the `scores` parameter. It must be a
            Numpy array with binary values (0 or 1). By default, the positive class
            stands for "Regular customer/good payer".
        threshold : float, optional
            The threshold value used to binarize `scores`, by default None. If
            None, then the optimal cutoff of the ROC class gonna be used. If
            not None, must be 0.0 <= value <= 1.0 or 0.0 <= value <= 100.0.
        """
        self._scores = check_dist(scores)
        self._targets = targets
        self.threshold = threshold
        self._bin_scores = (self._scores >= self.threshold).astype(float)

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

    @property
    def threshold(self) -> float:
        """
        Getter for the threshold value.

        Returns
        -------
        float
            A valid threshold value.
        """
        return self.__threshold

    @threshold.setter
    def threshold(self, value: float):
        """
        Setter for the threshold value.

        Parameters
        ----------
        value : float
            Raw value of the threshold, provided by the user.
            If it's None, then this method gonna set the threshold value based
            in the ROC class optimal_threshold attribute.

        Raises
        ------
        ValueError
            Occurs when the provided value is not a float and/or it's not in the
            interval 0.0 <= value <= 1.0 or 0.0 <= value <= 100.0.
        """
        if value is None:
            roc = ROC(self._scores, self._targets)
            self.__threshold = roc.optimal_threshold
        elif isinstance(value, float) and (0.0 <= value <= 1.0
                                           or 0.0 <= value <= 100.0):
            if value > 1.0:
                value = value / 100.0  # put value between 0.0 and 1.0, bemol-libraries default

            self.__threshold = value
        else:
            raise ValueError(
                "The threshold must be None or a float value between 0.0 and 1.0 or 0.0 and 100.0!"
            )

    def compute(self) -> typing.Tuple[np.array, np.array]:
        """
        This method returns the confusion matrix and its normalized version.

        Returns
        -------
        typing.Tuple[np.array, np.array]
            - cm_discret: np.array
                Confusion Matrix discrete/common
            - cm_normalized : np.array
                Normalized version of cm_discret.
        """
        cm_discret = confusion_matrix(self._targets, self._bin_scores)
        cm_normalized = cm_discret / cm_discret.sum(axis=1).reshape(-1, 1)
        return cm_discret, cm_normalized

    def plot(self,
             title: str = None,
             classes: list = ['Bads', 'Goods'],
             fontsize: int = 12,
             ax: plt.Axes = None):
        """
        Method to plot the CM chart.

        Parameters
        ----------
        title : str, optional
            Set the plot title. If None, it will be automatically generated,
            by default None.
        classes : list, optional
            Classification labels, by default ['Bads', 'Goods'].
            It's related to index. Eg.: Bads (0) and Goods (1).
        fontsize : int, optional
            Base font size to be used in the plot texts, by default 12.
        ax : plt.Axes, optional
            Matplotlib axis to export the plot, by default None.
        """
        if ax is None:
            _, ax = plt.subplots(figsize=(6, 4), facecolor=(1, 1, 1), dpi=90)

        cf, normalized = self.compute()
        labels = np.array([
            "{:.2%}\n({})".format(p, v)
            for v, p in zip(cf.reshape(-1), normalized.reshape(-1))
        ]).reshape(2, 2)

        # Confusion matrix plot
        ax = sns.heatmap(
            normalized,
            cmap="PuBu",
            annot=labels,
            annot_kws={"size": fontsize - 2},
            linewidths=2,
            fmt="s",
            ax=ax,
            square=True,
        )

        # Adjust plot settings
        ax.set_title(
            "Confusion Matrix" if title is None else title,
            {
                "size": fontsize,
            },
        )

        ax.set_yticklabels(classes,
                           rotation=90,
                           va="center",
                           fontsize=fontsize - 3)
        ax.set_xticklabels(classes, fontsize=fontsize - 3)
        ax.set_xlabel("Predicted Label", fontsize=fontsize - 2)
        ax.set_ylabel("True Label", fontsize=fontsize - 2)
