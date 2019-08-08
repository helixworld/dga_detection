__author__ = "Payas Gupta"


class PreProcessor(object):
    def __init__(self, df):
        self.df = df

    def clean_labels(self):
        self.df.dropna(subset=['is_dga'], inplace=True)
        self.df.is_dga = self.df.is_dga.str.lower()

        self.df.is_dga = self.df.is_dga.apply(lambda x: x[0] == "d")
