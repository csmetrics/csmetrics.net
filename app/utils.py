import os, numpy, pickle
import json, csv
import itertools
from operator import itemgetter
from random import randint

cur_path = os.path.dirname(os.path.abspath(__file__))
FILE_VENUE_WEIGHT = os.path.join(cur_path, "data/venue_weight.csv")
FILE_MEMBER = os.path.join(cur_path, "data/member_list.csv")

FILE_FULLNAME = os.path.join(cur_path, "data/venue_fullname.csv")
FILE_CATEGORY = os.path.join(cur_path, "data/venue_category.csv")

DIR_RAW_DATA_ALL = os.path.join(cur_path, "../score_data")
DIR_RAW_DATA = os.path.join(cur_path, "../scores")

venueName = {}
venueCategory = {}

paperData = {}
citationData = {}
instName = set()

# only load once
instMap = None
venueWeight = None


def readVenueName():
    global venueName
    venuefullname = open(FILE_FULLNAME)
    reader = csv.reader(venuefullname, delimiter=',')
    next(reader) # skip the first line
    venueName = dict((r[0], {"abbr": r[1], "full": r[2]}) for r in reader if r[0] != "")


def readPaperCount_all():
    global paperData, instName, citationData
    try:
        for cfile in os.listdir(DIR_RAW_DATA_ALL):
            confname = os.path.splitext(cfile)[0]
            cflist = pickle.load(open(os.path.join(DIR_RAW_DATA_ALL, cfile), "r"))
            # print(cflist)
            for k, v in cflist["count_score"].items():
                if type(k[0]).__name__ == 'str':
                    # confname, venue, year
                    paperData[(confname, k[0], k[1])] = v
                    instName.add(k[0])
            for k, v in cflist["cited_score_dict"].items():
                if type(k[0]).__name__ == 'str':
                    citationData[(confname, k[0], k[1])] = v
                    instName.add(k[0])
    except Exception as e:
        print(e)
        print(confname, k, v)

# confconf = {}
def readPaperCount():
    global paperData, instName, citationData
    try:
        for cfile in os.listdir(DIR_RAW_DATA):
            confname, year, type = os.path.splitext(cfile)[0].split('_')
            if type == "author": # only considr affil for now
                continue
            # if confname in confconf:
            #     confconf[confname].append(year)
            # else:
            #     confconf[confname] = []
            #     confconf[confname].append(year)
            cflist = json.load(open(os.path.join(DIR_RAW_DATA, cfile), "r"))
            for k, v in cflist.items():
                # confname, venue, year
                paperData[(confname, k, int(year))] = v["Publication Count"]
                citationData[(confname, k, int(year))] = v["Citation Count"]
                instName.add(k)
    except Exception as e:
        print(e)


def loadInstData():
    global instMap
    if instMap != None:
        return
    instMap = dict()
    memberlist = open(FILE_MEMBER)
    reader = csv.reader(memberlist)
    next(reader) # skip the first line
    for r in reader:
        for k in r[2:]:
            if k != "":
                instMap[k.strip()] = {"name": r[1].strip(), "type": r[0].strip()}


def loadVenueWeight():
    global venueWeight
    if venueWeight == None:
        weightfile = open(FILE_VENUE_WEIGHT)
        reader = csv.reader(weightfile)
        next(reader) # skip the first line
        # r[1]: Arithmetic Mean of Citations/Paper
        # r[2]: Geometric Mean of Citations/Paper
        venueWeight = dict((r[0], float(r[2])) for r in reader)
    # for k in venueWeight.keys():
    #     if k in confconf:
    #         print (k, ":", sorted(confconf[k], reverse=False))
    #     else:
    #         print (k, ":", "No Data")

def loadData():
    # readPaperCount_all()
    readPaperCount()
    loadInstData()
    loadVenueWeight()


def getVenueWeight(venue):
    global venueWeight
    if venue in venueWeight:
        return venueWeight[venue]
    else:
        return 0.0


def getVenueType(venue):
    global venueCategory
    return venueCategory[venue]["type"]


def findInstitution(inst):
    global instMap
    if inst in instMap:
        return instMap[inst]["name"], 2 if instMap[inst]["type"] == "academic" else 1
    else:
        return inst, 0


def createCategorycloud():
    global venueCategory
    readVenueName()
    venuesdata = open(FILE_CATEGORY)
    reader = csv.reader(venuesdata, delimiter=',')
    next(reader) # skip the first line
    venueCategory = dict((r[0], {
                "topic1":[w.strip().lower() for w in r[2].split(',')],
                "topic2":[w.strip().lower() for w in r[3].split(',')],
                "type": r[4]
            }) for r in reader if r[0] != '')

    wordset = {}
    for v in venueCategory.keys():
        for t2 in venueCategory[v]["topic2"]: wordset[t2] = 2
        for t1 in venueCategory[v]["topic1"]: wordset[t1] = 1
    # remove duplicated other, it is manually added at the end of the list
    wordset.pop("other")
    sorted_tags = sorted(wordset.items(), key=itemgetter(0))
    if '' == sorted_tags[0][0]:    # put other to the last in the list
        temp = sorted_tags[0]
        sorted_tags = sorted_tags[1:]
        sorted_tags.append(temp)
    # print(sorted_tags)
    return sorted_tags


def getVenueList(keyword):
    global venueName
    keyword_vlist = []
    # if keyword != "other":
    for k, v in venueCategory.items():
        if keyword in v["topic1"] or keyword in v["topic2"]:
            keyword_vlist.append(k)
    # else: # other goes the last
    #     for k, v in venueCategory.items():
    #         if "" in v["topic1"] and "" in v["topic2"]:
    #             keyword_vlist.append(k)

    vlist = [(venueName[v]["abbr"], venueName[v]["full"], getVenueWeight(v), getVenueType(v))\
                for v in keyword_vlist]
    return vlist


def getPaperScore(conflistname, pubrange, citrange, weight):
    global instName, venueName, venueCategory, paperData, citationData

    conflist = [k for k,v in venueName.items() if v["abbr"] in conflistname]
    pub = dict(zip(instName, [0 for col in range(len(instName))]))
    cite = dict(zip(instName, [0 for col in range(len(instName))]))
    wpub = dict(zip(instName, [0 for col in range(len(instName))]))
    pubyears = range(pubrange[0], pubrange[1]+1, 1)
    cityears = range(citrange[0], citrange[1]+1, 1)

    for t in itertools.product(*[conflist, list(instName), pubyears]):
        if t not in paperData: continue
        w = venueWeight[t[0]] if weight and t[0] in venueWeight else 1
        pub[t[1]] += paperData[t]
        wpub[t[1]] += paperData[t] * w
    for t in itertools.product(*[conflist, list(instName), cityears]):
        if t not in citationData: continue
        cite[t[1]] += citationData[t]

    # sum by alias name
    rlist = {}
    for v in instName:
        if pub[v] > 0 or cite[v] > 0:
            name, type = findInstitution(v) # type 0: not CRA member, type 1: CRA member
            if type == 0: # only include CRA members for now
                continue
            if name in rlist:
                rlist[name][0] += pub[v]
                rlist[name][1] += wpub[v]
                rlist[name][2] += cite[v]
            else:
                rlist[name] = [pub[v], wpub[v], cite[v], type]
    return [(k, v[0], v[1], v[2], v[3]) for k, v in rlist.items()]
