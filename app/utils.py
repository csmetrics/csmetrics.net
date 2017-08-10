import os, json, pickle
from random import randint

cur_path = os.path.dirname(os.path.abspath(__file__))

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

def getPaperScore(syear, eyear):
    cflist = pickle.load( open(os.path.join(cur_path, "../score_data/CCCG.pkl"), "rb" ) )
    for k, v in cflist["count_score"].items():
        print(k, v)
