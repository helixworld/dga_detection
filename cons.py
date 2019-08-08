__author__ = "Payas Gupta"

RESULTS_DIR = "results"
MODEL_DIR = "model"
DATA_DIR = "data"

ALEXA_TOP_1M = "{}/top-1m.csv".format(DATA_DIR)
WORDS_FILE = '{}/words_dictionary.json'.format(DATA_DIR)
ORIGINAL_TLDS = {"com", "org", "net", "int", "edu", "gov", "mil"}
FEATURES = ["total_length", "dom_length", "in_alexa_top", "legit_words_count", "is_tld_original"]
