import os, numpy, pickle
import json, csv
import itertools
from random import randint

cur_path = os.path.dirname(os.path.abspath(__file__))

paperData = {}
citationData = {}
instname = set()
def loadData():
    global paperData, citationData, instname
    fpath = os.path.join(cur_path, "../score_data")
    try:
        for cfile in os.listdir(fpath):
            confname = cfile.split('.')[0]
            cflist = pickle.load(open(os.path.join(fpath, cfile), "rb"))
            for k, v in cflist["count_score"].items():
                if type(k[0]).__name__ == 'str':
                    paperData[(confname, k[0], k[1])] = v
                    instname.add(k[0])
            for k, v in cflist["cited_score_dict"].items():
                if type(k[0]).__name__ == 'str':
                    citationData[(confname, k[0], k[1])] = v
                    instname.add(k[0])
    except Exception as e:
        print(e)
        print(confname, k, v)


instmap = None
def findInstitution(inst):
    global instmap
    if instmap == None:
        instmap = {}
        memberlist = open(os.path.join(cur_path, "data/Member_List.txt"))
        for l in memberlist.readlines():
            name, key = l.split('\t')
            instmap[key.strip()] = name.strip('"')
    if inst in instmap:
        return instmap[inst]
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

def getPaperScore(conflist, pubrange, citrange):
    global paperData, citationData, instname

    pub = dict(zip(instname, [0 for col in range(len(instname))]))
    cite = dict(zip(instname, [0 for col in range(len(instname))]))
    pubyears = range(pubrange[0], pubrange[1]+1, 1)
    cityears = range(citrange[0], citrange[1]+1, 1)
    for t in itertools.product(*[conflist, list(instname), pubyears]):
        if t not in paperData: continue
        pub[t[1]] += paperData[t]
    for t in itertools.product(*[conflist, list(instname), cityears]):
        if t not in citationData: continue
        cite[t[1]] += citationData[t]
    # print([(findInstitution(v), pub[v], cite[v], 0) for v in instname if pub[v]>0 or cite[v]>0])
    return [(findInstitution(v), pub[v], cite[v], 0) for v in instname if pub[v]>0 or cite[v]>0]
