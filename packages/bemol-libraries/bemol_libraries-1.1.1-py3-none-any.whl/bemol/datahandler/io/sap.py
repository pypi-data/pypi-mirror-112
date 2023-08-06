import os
import typing
import warnings
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm
import concurrent.futures


def __sap_to_pd(file_path: str, encoding: str = "latin-1") -> pd.DataFrame:
    """This function can read a valid SAP text file and converts it to a Pandas
    DataFrame object.

    Parameters
    ----------
    file_path : str
        A valid path to a SAP txt file.
    encoding : str, optional
        File encoding type, by default "latin-1"

    Returns
    -------
    pd.DataFrame
        Final DataFrame with valid lines from the input raw file.
    """
    # Open the `file_path` and get the valid lines
    with open(file_path, "r", encoding=encoding) as f:
        rows = list(
            filter(
                lambda x: len(x) > 2 and x[0] == "|" and x[1:3] != "--" and x[
                    1:3] != "||",
                f,
            ))  # Gets the valid lines

        # Deletes every row equals to header
        rows = [rows[0]] + list(filter(lambda x: x != rows[0], rows))

        # Cleans up each row and split it by the | (pipe) delimiter
        rows = [[j.rstrip() for j in i.rstrip().strip("|").split("|")]
                for i in rows]

    # Convert the rows list to DataFrame and replace white spaces to np.nan
    return pd.DataFrame(rows[1:], columns=rows[0]).replace(r"^\s*$",
                                                           np.nan,
                                                           regex=True)


def read_saptxts(files_path: typing.Union[str, list],
                 encoding: str = "latin-1",
                 n_jobs: int = None) -> pd.DataFrame:
    """This function can read a single file or set of valid SAP txt files in
    parallel. For multiple files, after reading them, this function gonna
    concatenates all into a single DataFrame to return.

    Parameters
    ----------
    files_path : str, list
        The path of a single SAP text file or a directory path contains multiple
        ones. It can receive a list of valid file paths as well.
    encoding : str, optional
        File encoding type, by default "latin-1"
    n_jobs : int, optional
        Max workers quantity. If it is None or not given, it will default to
        the number of processors on the machine. By default None.

    Returns
    -------
    pd.DataFrame
        Final DataFrame result. When multiple files are given as input, then it
        gonna be a concatenate DataFrame of each read file.

    Raises
    ------
    ValueError
        Wrong file name type, once the input `files_path` must be a list or an
        absolute/relative path to SAP txt files.
    """
    # If the `files_path` a singe SAP txt file, then simplely call `__sap_to_pd`
    if isinstance(files_path, str) and os.path.isfile(files_path):
        return __sap_to_pd(files_path, encoding)
    # Otherwise, if it's a list or a general absolute/relative path...
    elif isinstance(files_path, (str, list)):
        # Ensures that the `files path` be a list of files. So, if the
        # user gives a list, nothing gonna be done. Otherwise, is
        # expected a relative/absolute path, then it uses glob to
        # extract the files from it.
        files_path = (glob(files_path)
                      if not isinstance(files_path, list) else files_path)
        # Filters only the valid files, i.e., valid files ending with ".txt"
        # (this excludes subdirs too).
        files_path = [
            f for f in files_path
            if os.path.isfile(f) and f.lower().endswith(".txt")
        ]

        # Creates a SubProcess pool to read a single file per subprocess.
        with concurrent.futures.ProcessPoolExecutor(n_jobs) as executor:
            # Launches the subprocess to read each valid files in `files_path`
            # list using the `__sap_to_pd` function.
            future_to_pd = {
                executor.submit(__sap_to_pd, f, encoding): f
                for f in files_path
            }
            # Empty list to stores the completed subprocess results (i.e., the
            # computed DataFrames)
            complete_pds = []
            # For each finalized subprocess...
            for future in tqdm(
                    concurrent.futures.as_completed(future_to_pd),
                    desc="SAP files",
                    unit="file",
                    total=len(files_path),
            ):
                # Gets the file name that this subprocess was responsible for
                fname = future_to_pd[future]
                try:
                    # Tries to get its results (DataFrame)
                    complete_pds.append(future.result())
                except Exception as exc:
                    # Exceptions treatment, if occur
                    warnings.warn("%r generated an exception: %s" %
                                  (fname, exc))

            # Finally, concatenates each generated DataFrame into a single one.
            return pd.concat(complete_pds, axis=0)
    else:
        raise ValueError(
            "Wrong file name type. Please, try a list or an absolute/relative path to SAP txt files."
        )
