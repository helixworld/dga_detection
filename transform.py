import csv

from sklearn.base import BaseEstimator, TransformerMixin

from cons import ALEXA_TOP_1M, WORDS_FILE, ORIGINAL_TLDS

__author__ = "Payas Gupta"
import numpy as np
from tld import get_tld
import pandas as pd
import json


class Transformer(BaseEstimator, TransformerMixin):
    """
    Transforms the data and generate features
    """

    def __init__(self):
        self.valid_words = set([])

    # Return self nothing else to do here
    def fit(self, X, y=None):
        return self

    def transform(self, df):
        """
        Transforms the data frame by creating new features. It extracts features like
        tld - Top level domain
        dom - the actual domain name removing the tlds
        total_length - Total Length of the domain name including tlds
        domain_length - Totall length of the actual domain name
        in_alexa_top - Whether the domain name is in Alexa Top 1M list or not
        legit_words_count - Count the legitimate words in the domain name string
        is_tld_original - Is the tld in the original list of tlds
        :return:
        """
        # Create two columns with the TLD and the actual domain name
        df[['tld', 'dom']] = df.domain.apply(lambda x: pd.Series(self.parse_domain(x)))
        # Create another column with the total length of the full domain name
        df["total_length"] = df.domain.apply(len)
        # Create another column with the length of the domain name
        df["dom_length"] = df.dom.map(str).apply(len)
        # Create another column to see if the domain is in top Alexa 1Million genuine list or not
        self.load_top1M()
        df["in_alexa_top"] = df.domain.apply(self.in_alexa_top1M)
        # Create another column to count the total number of legit words
        self.load_words()
        df["legit_words_count"] = df.domain.apply(self.count_legit_words)
        # Create another column to check if the TLD is the original in the original list of TLDs
        df["is_tld_original"] = df.tld.apply(self.is_original_tld)

    def parse_domain(self, domain):
        """
        Parses the full domain
        :param domain:(str) the full domain name
        :return: A list containing the tld and the actual domain name
        """
        try:
            obj = get_tld(domain, fix_protocol=True, as_object=True)
            return [obj.tld, obj.domain]
        except Exception as e:
            return [np.nan, np.nan]

    def load_top1M(self):
        """
        Loads the Alexa top 1M file and stores in a member variable
        :return:
        """
        with open(ALEXA_TOP_1M, mode='r') as infile:
            reader = csv.reader(infile)
            self.alexa_top1M = set([rows[1] for rows in reader])

    def in_alexa_top1M(self, domain):
        """
        Checks if the domain name is in the top 1M Alexa list
        :param domain:(str) the domain name
        :return:(bool) Whether the domain is in the list or not
        """
        return True if domain in self.alexa_top1M else False

    def load_words(self):
        """
        Loads the list of all possible words in the dictionary and stores in a member variable
        :return:
        """
        with open(WORDS_FILE) as word_file:
            self.valid_words = set([w for w in json.load(word_file) if len(w) >= 3])

    def count_legit_words(self, domain):
        """
        Count the number of legitimate words in the domain name (removing the tlds)
        :param domain:(str) The actual domain name
        :return:(int) the count of all possible words in the domain name
        """
        possible_words = set([])
        for i in range(3, len(domain)):
            for j in range(0, len(domain) - (i - 1)):
                possible_words.add(domain[j:j + i])
        return len(possible_words & self.valid_words)

    def is_original_tld(self, tld):
        """
        Checks whether the tld is in the original list of tlds
        :param tld:(str) the top level domain
        :return:(bool) True/False
        """
        return True if tld in ORIGINAL_TLDS else False
