import os, codecs
import nltk, string
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
from .utils import *

cur_path = os.path.dirname(os.path.abspath(__file__))
venues = []

class Tokenizer:
    __state = {}
    stopwords = None

    def get_stopwords_from_file(self, fname):
        with codecs.open(fname, "r", "utf8") as f:
            content = f.readlines()
            return [x.rstrip('\n') for x in content]

    def tokenizer(self, t):
        wordnet_lemmatizer = WordNetLemmatizer()
        tokens = nltk.word_tokenize(t.lower())
        filtered = [w for w in tokens\
                    if w not in stopwords.words("english")\
                    and w not in string.punctuation\
                    and w not in self.stopwords]
        tagged = [word[0] for word in nltk.pos_tag(filtered)]
        lemma = [wordnet_lemmatizer.lemmatize(tag) for tag in tagged]
        return lemma

    def __init__(self):
        # make it singleton class to read stopwords from file only once
        self.__dict__ = self.__state
        if self.stopwords is None:
            f_stopwords = os.path.join(cur_path, "data/stopwords")
            self.stopwords = self.get_stopwords_from_file(f_stopwords)


def createWordcloud():
    global venues
    venuesdata = open(os.path.join(cur_path, "data/conferences"))
    venues = venuesdata.readlines()

    wordset = Counter([])
    T = Tokenizer()
    for line in venues:
        words = T.tokenizer(line)
        wordset += Counter(words)
    return wordset.most_common(30)

def getVenueList(keyword):
    global venues
    keyword_vlist = [v.split()[:-1] for v in venues if v.lower().find(keyword) >= 0]
    vlist = [(v[0], " ".join(v[1:]), getVenueWeight(v[0])) for v in keyword_vlist]
    return vlist
