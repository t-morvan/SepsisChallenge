""""
Splitting data set

Strategy : stratified split for each source (A and B)
"""

import os
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit


def read_source(
    directory: str, source_name: str
) -> Tuple[List[pd.DataFrame], List[int]]:
    """ "
    List of all patients data from the input source
    + add if the patient had sepsis

    Args:
        directory: source directory
        source_name: short source name

    Return:
        list of patient's data, list of sepsis indicators
    """

    data = []
    labels = []
    for patient in os.scandir(directory):
        df = pd.read_csv(patient.path, delimiter="|")
        df["ID"] = patient.name[1:-4]  # file name format p(ID number).psv
        df["source"] = source_name
        labels.append(df["SepsisLabel"].any())
        data.append(df)

    return data, labels


def split_source(
    data: List[pd.DataFrame], labels: List[int], train_size: float
) -> pd.DataFrame:
    """
    Split patients in train/valid

    Args:
        data: list of patient's dataframes
        labels: list of sepsi indicator
        train_size: proportion for train/valid split

    Return:
        train, valid dataframes
    """

    sss = StratifiedShuffleSplit(n_splits=1, train_size=train_size, random_state=42)
    for train_index, valid_index in sss.split(np.ones_like(labels), labels):
        train_data = pd.concat(data[idx] for idx in train_index)
        valid_data = pd.concat(data[idx] for idx in valid_index)

    return train_data, valid_data


def generate_data(train_size: float = 0.8, out: str = "../data") -> None:
    """
    Contatenate each train/valid dataset in a single dataframe

    Args:
         train_size: proportion for train/valid split
         out: save folder

    TO DO : automate to handle abritrary number of data sources
    """

    dataA, labelsA = read_source("../data/training_setA", "A")
    dataB, labelsB = read_source("../data/training_setB", "B")

    train_dataA, valid_dataA = split_source(dataA, labelsA, train_size)
    train_dataB, valid_dataB = split_source(dataB, labelsB, train_size)

    train = pd.concat((train_dataA, train_dataB))
    valid = pd.concat((valid_dataA, valid_dataB))

    train.to_csv(f"{out}/train.csv", index=False)
    valid.to_csv(f"{out}/valid.csv", index=False)


if __name__ == "__main__":
    print("Generating data")
    generate_data()
