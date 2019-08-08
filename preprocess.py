__author__ = "Payas Gupta"

import numpy as np


class PreProcessor(object):
    """
    Preprocess the data to filter noise and remove Nan etc
    """

    def __init__(self, df):
        self.df = df

    def clean(self):
        self.clean_labels()
        self.clean_data()

    def clean_labels(self):
        # df.is_dga.isna().value_counts()
        # False    157926
        # True          1
        # Name: is_dga, dtype: int64
        # Throwing the data with nis_dga = na
        self.df.dropna(subset=['is_dga'], inplace=True)
        # Making the is_dga label all lower
        self.df.is_dga = self.df.is_dga.str.lower()
        # """
        # legit    80735
        # dga      77178
        # da           2
        # dg           2
        # lgit         2
        # legip        1
        # lenit        1
        # dgb          1
        # dgs          1
        # dha          1
        # lefit        1
        # dgf          1
        # Name: is_dga, dtype: int64
        # Noticed there are errors in the class label so fixing it
        self.df.is_dga = self.df.is_dga.apply(lambda x: x[0] == "d")
        self.df.reset_index(inplace=True)

    def clean_data(self):
        # Making the domain name also as lower case
        self.df.domain = self.df.domain.str.lower()
        # Strip extra spaces from the domain name
        self.df.domain = self.df.domain.str.strip()
        # Replace the blank domain name with np.nan and then remove it
        self.df.domain.replace('', np.nan, inplace=True)
        # Remove domain where length is zero
        self.df.dropna(subset=["domain"], axis=0, inplace=True)
        self.df.reset_index(inplace=True)
