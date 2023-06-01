import os, numpy, pickle
import json, csv
import itertools
from operator import itemgetter
from random import randint
from datetime import datetime
# from .mag_search import gen_inst_alias, clean_inst

cur_path = os.path.dirname(os.path.abspath(__file__))
FILE_VENUE_WEIGHT = os.path.join(cur_path, "data/venue_weight.csv")
FILE_INST_FULL = os.path.join(cur_path, "data/inst_full_clean.csv")

FILE_VENUE = os.path.join(cur_path, "data/venue_list.csv")
DIR_RAW_DATA = os.path.join(cur_path, "../data/scores")

venueName = {}
venueCategory = {}
categorySet = {}
instName = set()

# only load once
instInfo = None
venueWeight = None
paperData = None
citationData = None

ContinentOrdered = [
    "All",
    "Asia",
    "Africa",
    "Europe",
    "North America",
    "South America",
    "Oceania",
    "Other"
]


def readVenueName():
    global venueName
    venuefullname = open(FILE_VENUE)
    reader = csv.reader(venuefullname, delimiter=',')
    next(reader) # skip the first line
    for r in reader:
        if not r[0]:
            continue
        topic_list = list({
            *[token.strip() for token in r[2].split(',') if token],
            *[token.strip() for token in r[3].split(',') if token]
        })
        venueName[r[0]] = dict(
            abbr=r[1],
            full=r[5],
            link=r[6],
            topic=topic_list if topic_list else ['other']
        )


def readPaperCount():
    global paperData, instName, citationData
    if paperData != None:
        return
    try:
        paperData = {}
        citationData = {}
        for cfile in os.listdir(DIR_RAW_DATA):
            confname, year, type = os.path.splitext(cfile)[0].split('_')
            if type == "author": # only considr affil for now
                continue
            cflist = json.load(open(os.path.join(DIR_RAW_DATA, cfile), "r"))
            for k, v in cflist.items():
                # inst, confname, year
                if k not in paperData:
                    paperData[k] = []
                paperData[k].append({"conf": confname, "year": int(year), "pubCount": v["Publication Count"],
                                    "wPubCount": venueWeight[confname]*v["Publication Count"]})
                if k not in citationData:
                    citationData[k] = []
                citationData[k].append({"conf": confname, "year": int(year), "citeCount": v["Citation Count"]})
                instName.add(k)

        # gen_inst_alias(instName)
    except Exception as e:
        print(e)


def loadInstData():
    global instInfo

    # load inst_fullname
    if instInfo != None:
        return
    instInfo = dict()
    infolist = open(FILE_INST_FULL)
    reader = csv.reader(infolist)
    next(reader) # skip the first line
    for r in reader:
        instInfo[r[1].strip()] = {
            "fullname": r[1].strip(),
            "type": r[2].strip(),
            "continent": r[3].strip(),
            "country": r[4].strip() if r[4].strip() != "No data" else "",
            "url": r[5].strip()
        }


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
    loadVenueWeight()
    readPaperCount()
    loadInstData()


def getVenueWeight(venue):
    global venueWeight
    if venue in venueWeight:
        return venueWeight[venue]
    else:
        return 0.0


def getVenueType(venue):
    global venueCategory
    return venueCategory[venue]["type"]



def createCategoryCloud():
    global venueCategory, categorySet
    readVenueName()
    venuesdata = open(FILE_VENUE)
    reader = csv.reader(venuesdata, delimiter=',')
    next(reader) # skip the first line
    for r in reader:
        if not r[0]:
            continue
        topics = []
        topic_1 = [w.strip().lower() for w in r[2].split(',')] if r[2] else None
        topic_2 = [w.strip().lower() for w in r[3].split(',')] if r[3] else None
        if topic_1:
            topics.extend(topic_1)
        if topic_2:
            topics.extend(topic_2)
        for topic in topics:
            if topic in categorySet:
                categorySet[topic].append(r[0])
            else:
                categorySet[topic] = [r[0]]
        venueCategory[r[0]] = {"topic1":topic_1, "topic2":topic_2, "type": r[4]}

    wordset = sorted(list(categorySet.keys()))
    wordset.remove("other") # move other to the end
    return wordset+["other"]


def getVenueList(keywords=None):
    global venueName, categorySet
    if keywords:
        keyword_vlist = set()
        for k in keywords:
            keyword_vlist.update(set(categorySet[k.lower()]))
        vlist = [(
            venueName[v]["abbr"],
            venueName[v]["full"],
            getVenueWeight(v),
            getVenueType(v),
            venueName[v]["link"],
            venueName[v]["topic"]) for v in keyword_vlist
        ]
    else:
        vlist = [(
            venueName[v]["abbr"],
            venueName[v]["full"],
            getVenueWeight(v),
            getVenueType(v),
            venueName[v]["link"],
            venueName[v]["topic"]) for v in venueName
        ]
    return vlist


def getPaperScore(conflistname, pubrange, citrange, weight):
    global instName, venueName, venueCategory, paperData, citationData

    cite = {}
    wpub = {}
    conflist = [k for k,v in venueName.items() if v["abbr"] in conflistname]
    pubyears = range(pubrange[0], pubrange[1]+1, 1)
    cityears = range(citrange[0], citrange[1]+1, 1)

    for inst in list(instName):
        wpub[inst] = sum([p["wPubCount"] if weight else p["pubCount"]\
                        for p in paperData[inst] if p["conf"] in conflist and p["year"] in pubyears])
        cite[inst] = sum([c["citeCount"] for c in citationData[inst] if c["conf"] in conflist and c["year"] in cityears])

    # sum by openalex key
    rlist = {}
    for v in instName:
        if v not in instInfo:
            continue
        if wpub[v] > 0 or cite[v] > 0:
            name = v
            type = instInfo[v]["type"]
            if name in rlist:
                rlist[name][0] += wpub[v]
                rlist[name][1] += cite[v]
            else:
                rlist[name] = [wpub[v], cite[v], type]

    return [{"name": instInfo[k]["fullname"],
            "type": instInfo[k]["type"],
            "continent": instInfo[k]["continent"],
            "country": instInfo[k]["country"],
            "wpub": v[0], "cite": v[1],
            "url": instInfo[k]["url"]
        } for k, v in rlist.items()]
