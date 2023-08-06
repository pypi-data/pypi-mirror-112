from typing import Union
import pandas as pd
import os
import time
import urllib

def split_train_test(filename: str=None, size=0.8, random_state:int=int(time.time())):
    """Split the training dataset and the testing dataset

    Args:
        filename (str, optional): the dataset. The dataset is a csv file and must include Target column. Defaults to the dataset in the paper https://github.com/KardelUM/Carom/raw/master/caromDataset.csv.
        size (float/tuple, optional): The size for training dataset and testing dataset. 
                                    When size is a 2 elements tuple, training dataset size is the fist element and the testing dataset siz eis the second element
                                    When size is a float, it means the fraction for training dataset.
        random_state (int, optional): random state. Defaults to the seconds since the epoch, in UTC.

    Returns:
        (pd.DataFrame, pd.DataFrame): Training dataset and testing dataset.
    """
    if filename is None:
        filename="https://github.com/KardelUM/Carom/raw/master/caromDataset.csv"
    df = pd.read_csv(filename)
    Ntarget =  len(df["Target"].unique())
    if isinstance(size, tuple):
        # if size is a tuple, the first is the training size and the second is the testing size
        Ntraining, Ntesting = size
        df_train = df.groupby("Target").sample(n=int(Ntraining/Ntarget), random_state=random_state)
        df_test = df.drop(df_train.index.to_list()).groupby("Target").sample(n=int(Ntesting/Ntarget), random_state=random_state+1).reset_index(drop=True)
        df_train.reset_index(drop=True)
    else:
        df_train = df.groupby("Target").sample(frac=size, random_state=random_state)
        df_test = df.drop(df_train.index.to_list()).reset_index(drop=True)
        df_train.reset_index(drop=True)
    return df_train, df_test


