import os, numpy, pickle
import json, csv
import itertools
from operator import itemgetter
from random import randint
from datetime import datetime
from .mag_search import gen_inst_alias, clean_inst

cur_path = os.path.dirname(os.path.abspath(__file__))
FILE_VENUE_WEIGHT = os.path.join(cur_path, "data/venue_weight.csv")
FILE_GRID = os.path.join(cur_path, "data/grid.csv")
FILE_INST_ALIAS = os.path.join(cur_path, "data/inst_alias.csv")
FILE_INST_FULL = os.path.join(cur_path, "data/inst_fullname.csv")

FILE_VENUE = os.path.join(cur_path, "data/venue_list.csv")
DIR_RAW_DATA = os.path.join(cur_path, "../data/scores")

venueName = {}
venueCategory = {}
categorySet = {}
instName = set()

# only load once
instMap = None
instInfo = None
venueWeight = None
gridMap = None
paperData = None
citationData = None


def readVenueName():
    global venueName
    venuefullname = open(FILE_VENUE)
    reader = csv.reader(venuefullname, delimiter=',')
    next(reader) # skip the first line
    venueName = dict((r[0], {"abbr": r[1], "full": r[5], "link": r[6]}) for r in reader if r[0] != "")


# confconf = {}
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
            # if confname in confconf:
            #     confconf[confname].append(year)
            # else:
            #     confconf[confname] = []
            #     confconf[confname].append(year)
            cflist = json.load(open(os.path.join(DIR_RAW_DATA, cfile), "r"))
            for k, v in cflist.items():
                # inst, confname, year
                if k in paperData:
                    paperData[k].append({"conf": confname, "year": int(year), "pubCount": v["Publication Count"]})
                else:
                    paperData[k] = [{"conf": confname, "year": int(year), "pubCount": v["Publication Count"]}]
                if k in citationData:
                    citationData[k].append({"conf": confname, "year": int(year), "citeCount": v["Citation Count"]})
                else:
                    citationData[k] = [{"conf": confname, "year": int(year), "citeCount": v["Citation Count"]}]
                # paperData[(confname, k, int(year))] = v["Publication Count"]
                # citationData[(confname, k, int(year))] = v["Citation Count"]
                instName.add(k)

        # gen_inst_alias(instName)
    except Exception as e:
        print(e)


def loadInstData():
    global instMap, instInfo, gridMap

    # load Grid information
    if gridMap != None:
        return
    gridMap = dict()
    reader = csv.reader(open(FILE_GRID))
    next(reader) # skip the first line
    gridMap = {r[0].strip():r[2].strip() for r in reader}
    print(gridMap)

    #load inst_alias
    if instMap != None:
        return
    instMap = dict()
    aliaslist = open(FILE_INST_ALIAS)
    reader = csv.reader(aliaslist)
    next(reader) # skip the first line
    for r in reader:
        for alias in r[1].split(','):
            instMap[alias] = r[0].strip()
    # print([name for name in instName if name not in instMap]) # unregistered name
    for name in [n for n in instName if n not in instMap]:
        instMap[name] = name

    # load inst_fullname
    if instInfo != None:
        return
    instInfo = dict()
    infolist = open(FILE_INST_FULL)
    reader = csv.reader(infolist)
    next(reader) # skip the first line
    for r in reader:
        instInfo[r[0]] = {
            "fullname": r[1].strip(),
            "grid": r[2].strip(),
            "url": r[3].strip(),
            "wiki": r[4].strip()
        }
    for key in set(instMap.values()):
        if key not in instInfo:
            instInfo[key] = {
                "fullname": key,
                "grid": "",
                "url": "",
                "wiki": ""
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
        return instMap[inst], 0
    else:
        return inst, 0


def createCategorycloud():
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


def getVenueList(keywords):
    global venueName, categorySet
    keyword_vlist = set()
    for k in keywords:
        keyword_vlist.update(set(categorySet[k.lower()]))
    vlist = [(venueName[v]["abbr"], venueName[v]["full"], getVenueWeight(v), getVenueType(v), venueName[v]["link"],)\
                for v in keyword_vlist]
    return vlist


def getPaperScore(conflistname, pubrange, citrange, weight):
    global instName, venueName, venueCategory, paperData, citationData

    cite = {}
    wpub = {}
    conflist = [k for k,v in venueName.items() if v["abbr"] in conflistname]
    pubyears = range(pubrange[0], pubrange[1]+1, 1)
    cityears = range(citrange[0], citrange[1]+1, 1)

    for inst in list(instName):
        wpub[inst] = sum([p["pubCount"]*(venueWeight[p["conf"]] if weight and p["conf"] in venueWeight else 1)\
                        for p in paperData[inst] if p["conf"] in conflist and p["year"] in pubyears])
        cite[inst] = sum([c["citeCount"] for c in citationData[inst] if c["conf"] in conflist and c["year"] in cityears])

    # sum by alias name
    rlist = {}
    for v in instName:
        if wpub[v] > 0 or cite[v] > 0:
            name, type = findInstitution(v)
            if name in rlist:
                rlist[name][0] += wpub[v]
                rlist[name][1] += cite[v]
            else:
                rlist[name] = [wpub[v], cite[v], type]

    return [{"name": instInfo[k]["fullname"], "type": gridMap[instInfo[k]["grid"]] if instInfo[k]["grid"] in gridMap else "other",
            "wpub": v[0], "cite": v[1],
            "url": instInfo[k]["url"] if instInfo[k]["url"] != "" else instInfo[k]["wiki"]
        } for k, v in rlist.items()]
