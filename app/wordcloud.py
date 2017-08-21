import os, codecs, csv
from collections import Counter
from .utils import *

cur_path = os.path.dirname(os.path.abspath(__file__))
venueName = {}
venueCategory = {}


def readVenueName():
    global venueName
    venuefullname = open(os.path.join(cur_path, "data/venue_fullname.csv"))
    reader = csv.reader(venuefullname, delimiter=':')
    venueName = dict((r[0].lower(), r[1]) for r in reader)

def createCategorycloud():
    global venueName, venueCategory
    readVenueName()
    venuesdata = open(os.path.join(cur_path, "data/category_sample.csv"))
    reader = csv.reader(venuesdata, delimiter=':')
    venueCategory = dict((r[2].lower(), {"topic1":r[0].split(','), "topic2":r[1].split(',')}) for r in reader)

    wordset = Counter([])
    for v in venueCategory.keys():
        wordset += Counter(venueCategory[v]["topic1"])
        wordset += Counter(venueCategory[v]["topic2"])
    return wordset.most_common()

def getVenueList(keyword):
    global venueName, venueCategory
    keyword_vlist = []
    for k, v in venueCategory.items():
        if keyword in v["topic1"] or keyword in v["topic2"]:
            keyword_vlist.append(k)
    vlist = [(v, venueName[v], getVenueWeight(v)) for v in keyword_vlist]
    # print(vlist)
    return vlist
