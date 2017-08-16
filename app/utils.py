import os, json, numpy, pickle
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

def getPaperScore(conflist, pubrange, citrange):
    pub = {}
    cite = {}
    for confname in conflist:
        fpath = os.path.join(cur_path, "../score_data/"+confname+".pkl")
        if not os.path.exists(fpath):
            print(confname + " not exists")
            continue
        cflist = pickle.load(open(fpath, "rb"))
        # print(cflist.keys())
        for k, v in cflist["count_score"].items():
            # print(k[0], k[1], v)
            if type(k[0]).__name__ == 'str'\
                and pubrange[0] <= k[1] and k[1] <= pubrange[1]:
                if k[0] in pub:
                    pub[k[0]] += v
                else:
                    pub[k[0]] = v

        for k, v in cflist["cited_score_dict"].items():
            # print(k[0], k[1], v)
            if type(k[0]).__name__ == 'str'\
                and citrange[0] <= k[1] and k[1] <= citrange[1]:
                if k[0] in cite:
                    cite[k[0]] += v
                else:
                    cite[k[0]] = v

    # print([(findInstitution(v[0]), v[1], cite[v[0]] if v[0] in cite else 0, 0) for v in pub.items()])
    return [(findInstitution(v[0]), v[1], cite[v[0]] if v[0] in cite else 0, 0) for v in pub.items()]
