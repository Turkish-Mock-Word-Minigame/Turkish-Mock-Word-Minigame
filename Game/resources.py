import os
from nltk import ConditionalProbDist, MLEProbDist
import pickle

absolute_path = os.path.dirname(__file__)

ngram_pbs = ConditionalProbDist(
    pickle.load(open(os.path.join(absolute_path, "./data/freq_cfd.pkl"), "rb")), MLEProbDist)

unwanted_words = pickle.load(open(os.path.join(absolute_path, "./data/names.pkl"), "rb")) + \
    pickle.load(open(os.path.join(absolute_path, "./data/stopwords.pkl"), "rb"))
