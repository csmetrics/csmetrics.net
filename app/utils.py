import os, numpy, pickle
import json, csv
import itertools
from random import randint

cur_path = os.path.dirname(os.path.abspath(__file__))
FILE_VENUE_WEIGHT = os.path.join(cur_path, "data/venue_weight.csv")
FILE_MEMBER = os.path.join(cur_path, "data/member_list.csv")

DIR_RAW_DATA_ALL = os.path.join(cur_path, "../score_data")
DIR_RAW_DATA = os.path.join(cur_path, "../scores")

paperData = {}
citationData = {}
instName = set()

# only load once
instMap = None
venueWeight = None

def readPaperCount_all():
    global paperData, citationData, instName
    try:
        for cfile in os.listdir(DIR_RAW_DATA_ALL):
            confname = os.path.splitext(cfile)[0]
            cflist = pickle.load(open(os.path.join(DIR_RAW_DATA_ALL, cfile), "rb"))
            # print(cflist)
            for k, v in cflist["count_score"].items():
                if type(k[0]).__name__ == 'str':
                    # confname(upper), venue, year
                    paperData[(confname, k[0], k[1])] = v
                    instName.add(k[0])
            for k, v in cflist["cited_score_dict"].items():
                if type(k[0]).__name__ == 'str':
                    citationData[(confname, k[0], k[1])] = v
                    instName.add(k[0])
    except Exception as e:
        print(e)
        print(confname, k, v)


def readPaperCount():
    global paperData, citationData, instName
    try:
        for cfile in os.listdir(DIR_RAW_DATA):
            confname, year, type = os.path.splitext(cfile)[0].split('_')
            confname = confname.upper()
            if type == "author": # only considr affil for now
                continue
            cflist = json.load(open(os.path.join(DIR_RAW_DATA, cfile), "rb"))
            for k, v in cflist.items():
                # confname(upper), venue, year
                paperData[(confname, k, int(year))] = v["Publication Count"]
                citationData[(confname, k, int(year))] = v["Citation Count"]
                instName.add(k)
    except Exception as e:
        print(e)
        print(confname, k, v)


def loadInstData():
    global instMap
    if instMap == None:
        memberlist = open(FILE_MEMBER)
        reader = csv.reader(memberlist)
        next(reader) # skip the first line
        instMap = dict((r[1].strip(), r[0].strip()) for r in reader)

def loadVenueWeight():
    global venueWeight
    if venueWeight == None:
        weightfile = open(FILE_VENUE_WEIGHT)
        reader = csv.reader(weightfile)
        next(reader) # skip the first line
        # r[1]: Arithmetic Mean of Citations/Paper
        # r[2]: Geometric Mean of Citations/Paper
        venueWeight = dict((r[0], float(r[2])) for r in reader)

def loadData():
    # readPaperCount_all()
    readPaperCount()
    loadInstData()
    loadVenueWeight()


def getVenueWeight(venue):
    global venueWeight
    venue = venue.lower()
    if venue in venueWeight:
        return venueWeight[venue]
    else:
        return 0.0


def findInstitution(inst):
    global instMap
    if inst in instMap:
        return instMap[inst], 1
    else:
        return inst, 0

def getPaperScore(conflist, pubrange, citrange, weight):
    global paperData, citationData, instName

    pub = dict(zip(instName, [0 for col in range(len(instName))]))
    cite = dict(zip(instName, [0 for col in range(len(instName))]))
    wpub = dict(zip(instName, [0 for col in range(len(instName))]))
    wcite = dict(zip(instName, [0 for col in range(len(instName))]))
    pubyears = range(pubrange[0], pubrange[1], 1)
    cityears = range(citrange[0], citrange[1], 1)
    for t in itertools.product(*[conflist, list(instName), pubyears]):
        if t not in paperData: continue
        w = venueWeight[t[0].lower()] if weight and t[0].lower() in venueWeight else 1
        pub[t[1]] += paperData[t]
        wpub[t[1]] += paperData[t] * w
    for t in itertools.product(*[conflist, list(instName), cityears]):
        if t not in citationData: continue
        w = venueWeight[t[0].lower()] if weight and t[0].lower() in venueWeight else 1
        cite[t[1]] += citationData[t]
        wcite[t[1]] += citationData[t] * w

    rlist = []
    for v in instName:
        if pub[v] > 0 or cite[v] > 0:
            name, type = findInstitution(v) # type 0: not CRA member, type 1: CRA member
            rlist.append((name, pub[v], wpub[v], cite[v], wcite[v], type))
    return rlist
