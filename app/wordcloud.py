import os, codecs, csv
from collections import Counter
from operator import itemgetter
from .utils import *

cur_path = os.path.dirname(os.path.abspath(__file__))
FILE_FULLNAME = os.path.join(cur_path, "data/venue_fullname.csv")
FILE_CATEGORY = os.path.join(cur_path, "data/venue_category.csv")

venueName = {}
venueCategory = {}


def readVenueName():
    global venueName
    venuefullname = open(FILE_FULLNAME)
    reader = csv.reader(venuefullname, delimiter=',')
    next(reader) # skip the first line
    venueName = dict((r[0], {"abbr": r[1], "full": r[2]}) for r in reader if r[0] != "")

def createCategorycloud():
    global venueName, venueCategory
    readVenueName()
    venuesdata = open(FILE_CATEGORY)
    reader = csv.reader(venuesdata, delimiter=',')
    next(reader) # skip the first line
    venueCategory = dict((r[3], {
                "topic1":[w.strip().lower() for w in r[0].split(',')],
                "topic2":[w.strip().lower() for w in r[1].split(',')]
            }) for r in reader)

    wordset = {}
    for v in venueCategory.keys():
        for t2 in venueCategory[v]["topic2"]: wordset[t2] = 2
        for t1 in venueCategory[v]["topic1"]: wordset[t1] = 1
    # print(sorted(wordset.items(), key=itemgetter(0)))
    return sorted(wordset.items(), key=itemgetter(0))

def getVenueList(keyword):
    global venueName, venueCategory
    keyword_vlist = []
    if keyword == "others":
        for k, v in venueCategory.items():
            if "" in v["topic1"] and "" in v["topic2"]:
                keyword_vlist.append(k)
    else:
        for k, v in venueCategory.items():
            if keyword in v["topic1"] or keyword in v["topic2"]:
                keyword_vlist.append(k)

    vlist = [(venueName[v]["abbr"], venueName[v]["full"], getVenueWeight(v))\
                for v in keyword_vlist]
    return vlist
