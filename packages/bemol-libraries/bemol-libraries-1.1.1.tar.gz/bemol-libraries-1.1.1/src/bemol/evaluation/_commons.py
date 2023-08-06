import numpy as np


def check_dist(distribution: np.array) -> np.array:
    """Performs a series of validations for the given input distribution

    Parameters
    ----------
    distribution : np.array
        Input distribution

    Returns
    -------
    np.array
        Full checked distribution
    """
    distribution = np.array(distribution)

    if distribution.max() > 1.0:
        distribution /= 100
    if np.count_nonzero(np.isnan(distribution)):
        raise ValueError('Distribution with NaN values!')
    if not ((distribution >= 0.0).all() and (distribution <= 1.0).all()):
        raise ValueError(
            'Distribution out of range [0.0, 1.0] or [0.0, 100.0]!')
    if len(distribution.shape) != 1:
        raise AttributeError('Distribution must be a 1-d array')

    return np.array(distribution)


COLOR_SCHEME = {
    "primary": "#0092D4",  # Bemol blue
    "secondary": "#E3596B",  # Bemol red
    "aux_1": "#FFFFFF",  # White
    "aux_2": "#0087D0",  # Dark Bemol blue
    "aux_3": "#DBDBD9",  # Gray
    "aux_4": "#CCCCCC",  # Dark gray
    "aux_5": "#3B3B3B"  # Very very dark gray :p
}
