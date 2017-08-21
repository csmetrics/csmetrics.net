import os, numpy, pickle
import json, csv
import itertools
from random import randint

cur_path = os.path.dirname(os.path.abspath(__file__))

paperData = {}
citationData = {}
instName = set()

# only load once
instMap = None
venueWeight = None

def readPaperCount():
    global paperData, citationData, instName
    fpath = os.path.join(cur_path, "../score_data")
    try:
        for cfile in os.listdir(fpath):
            confname = cfile.split('.')[0]
            cflist = pickle.load(open(os.path.join(fpath, cfile), "rb"))
            # print(cflist)
            for k, v in cflist["count_score"].items():
                if type(k[0]).__name__ == 'str':
                    paperData[(confname, k[0], k[1])] = v
                    instName.add(k[0])
            for k, v in cflist["cited_score_dict"].items():
                if type(k[0]).__name__ == 'str':
                    citationData[(confname, k[0], k[1])] = v
                    instName.add(k[0])
    except Exception as e:
        print(e)
        print(confname, k, v)


def loadInstData():
    global instMap
    if instMap == None:
        instMap = {}
        memberlist = open(os.path.join(cur_path, "data/Member_List.txt"))
        for l in memberlist.readlines():
            name, key = l.split('\t')
            instMap[key.strip()] = name.strip('"')

def loadVenueWeight():
    global venueWeight
    if venueWeight == None:
        weightfile = open(os.path.join(cur_path, "data/venue_weight.csv"))
        reader = csv.reader(weightfile)
        next(reader) # skip the first line
        # r[1]: Arithmetic Mean of Citations/Paper
        # r[2]: Geometric Mean of Citations/Paper
        venueWeight = dict((r[0], float(r[2])) for r in reader)

def loadData():
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
        return instMap[inst]
    else:
        return inst


def getExampleScore():
    rawdata = open(os.path.join(cur_path, "data/aamas2007affil.txt"))
    lines = rawdata.readlines()
    data = []
    for i in range(2, len(lines), 3):
        uname = lines[i].split(' ', 1)[1].strip()
        citation = float(lines[i+1].split(' ', 1)[1].strip())
        data.append((findInstitution(uname), randint(10, 400), citation, 0))
    return data

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
    rlist = [(findInstitution(v), pub[v], wpub[v], cite[v], wcite[v], 0) for v in instName if pub[v]>0 or cite[v]>0]
    return rlist
