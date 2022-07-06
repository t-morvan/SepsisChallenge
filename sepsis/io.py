""""
Read data

TO DO: importlib for relative import
"""

import pandas as pd


def get_train() -> pd.DataFrame:
    """
    Return:
        train data
    """
    return pd.read_csv("../data/train.csv")


def get_valid() -> pd.DataFrame:
    """
    Return:
        valid data
    """
    return pd.read_csv("../data/valid.csv")
