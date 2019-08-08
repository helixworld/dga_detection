from cons import DATA_DIR

__author__ = "Payas Gupta"

import pandas as pd


def load_dataset(fname):
    """
    Load the training dataset from a file where fields are separated by ctrl-A
    :param fname: Filename which contains the dataset
    :return:
    """
    return pd.read_csv(fname, sep='\x01', header=None,
                       names=['domain', 'origin', 'is_dga'])


def start_training():
    df = load_dataset(fname='{}/dga-dataset.txt'.format(DATA_DIR))
    print(df)
