import os
import json
import csv

cur_path = os.path.dirname(os.path.abspath(__file__))
file_venue_weight = os.path.join(cur_path, "data/venue_weight.csv")
file_inst_full = os.path.join(cur_path, "data/inst_full_clean.csv")

file_venue = os.path.join(cur_path, "data/venue_list.csv")
dir_raw_data = os.path.join(cur_path, "../data/scores")

venue_name = {}
venue_category = {}
category_set = {}
inst_name = set()

# only load once
inst_info = None
venue_weight = None
paper_data = None
citation_data = None

continent_ordered = [
    "All",
    "Asia",
    "Africa",
    "Europe",
    "North America",
    "South America",
    "Oceania",
    "Other"
]


def read_venue_name():
    global venue_name
    venue_fullname = open(file_venue)
    reader = csv.reader(venue_fullname, delimiter=',')
    next(reader)  # skip the first line
    for r in reader:
        if not r[0]:
            continue
        topic_list = list({
            *[token.strip() for token in r[2].split(',') if token],
            *[token.strip() for token in r[3].split(',') if token]
        })
        venue_name[r[0]] = dict(
            abbr=r[1],
            full=r[5],
            link=r[6],
            topic=topic_list if topic_list else ['other']
        )


def read_paper_count():
    global paper_data, inst_name, citation_data
    if paper_data is not None:
        return
    try:
        paper_data = {}
        citation_data = {}
        for cfile in os.listdir(dir_raw_data):
            conf_name, year, file_type = os.path.splitext(cfile)[0].split('_')
            if file_type == "author":  # only consider affil for now
                continue
            cf_list = json.load(open(os.path.join(dir_raw_data, cfile), "r"))
            for k, v in cf_list.items():
                # inst, conf_name, year
                if k not in paper_data:
                    paper_data[k] = []
                paper_data[k].append({"conf": conf_name, "year": int(year), "pubCount": v["Publication Count"],
                                      "wPubCount": venue_weight[conf_name] * v["Publication Count"]})
                if k not in citation_data:
                    citation_data[k] = []
                citation_data[k].append({"conf": conf_name, "year": int(year), "citeCount": v["Citation Count"]})
                inst_name.add(k)
    except Exception as e:
        print(e)


def load_inst_data():
    global inst_info

    # load inst_fullname
    if inst_info is not None:
        return
    inst_info = dict()
    info_list = open(file_inst_full)
    reader = csv.reader(info_list)
    next(reader)  # skip the first line
    for r in reader:
        inst_info[r[1].strip()] = {
            "fullname": r[1].strip(),
            "type": r[2].strip(),
            "continent": r[3].strip(),
            "country": r[4].strip() if r[4].strip() != "No data" else "",
            "url": r[5].strip()
        }


def load_venue_weight():
    global venue_weight
    if venue_weight is None:
        weight_file = open(file_venue_weight)
        reader = csv.reader(weight_file)
        next(reader)  # skip the first line
        # r[1]: Arithmetic Mean of Citations/Paper
        # r[2]: Geometric Mean of Citations/Paper
        venue_weight = dict((r[0], float(r[2])) for r in reader)


def load_data():
    load_venue_weight()
    read_paper_count()
    load_inst_data()


def get_venue_weight(venue):
    global venue_weight
    if venue in venue_weight:
        return venue_weight[venue]
    else:
        return 0.0


def get_venue_type(venue):
    global venue_category
    return venue_category[venue]["type"]


def create_category_cloud():
    global venue_category, category_set
    read_venue_name()
    venues_data = open(file_venue)
    reader = csv.reader(venues_data, delimiter=',')
    next(reader)  # skip the first line
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
            if topic in category_set:
                category_set[topic].append(r[0])
            else:
                category_set[topic] = [r[0]]
        venue_category[r[0]] = {"topic1": topic_1, "topic2": topic_2, "type": r[4]}

    word_set = sorted(list(category_set.keys()))
    word_set.remove("other")  # move other to the end
    return word_set + ["other"]


def get_venue_list(keywords=None):
    global venue_name, category_set
    if keywords:
        keyword_vlist = set()
        for k in keywords:
            keyword_vlist.update(set(category_set[k.lower()]))
        vlist = [(
            venue_name[v]["abbr"],
            venue_name[v]["full"],
            get_venue_weight(v),
            get_venue_type(v),
            venue_name[v]["link"],
            venue_name[v]["topic"]) for v in keyword_vlist
        ]
    else:
        vlist = [(
            venue_name[v]["abbr"],
            venue_name[v]["full"],
            get_venue_weight(v),
            get_venue_type(v),
            venue_name[v]["link"],
            venue_name[v]["topic"]) for v in venue_name
        ]
    return vlist


def get_paper_score(conflist_name, pub_range, cit_range, weight):
    global inst_name, venue_name, venue_category, paper_data, citation_data

    cite = {}
    wpub = {}
    conf_list = [k for k, v in venue_name.items() if v["abbr"] in conflist_name]
    pub_years = range(pub_range[0], pub_range[1] + 1, 1)
    cit_years = range(cit_range[0], cit_range[1] + 1, 1)

    for inst in inst_name:
        paper_list = paper_data.get(inst, [])
        citation_list = citation_data.get(inst, [])

        # Calculate weighted publication count
        wpub[inst] = sum(
            p["wPubCount"] if weight else p["pubCount"]
            for p in paper_list
            if p["conf"] in conf_list and p["year"] in pub_years
        )

        # Calculate citation count
        cite[inst] = sum(
            c["citeCount"]
            for c in citation_list
            if c["conf"] in conf_list and c["year"] in cit_years
        )

    # sum by openalex key
    rlist = {}
    for v in inst_name:
        if v not in inst_info:
            continue

        if wpub[v] > 0 or cite[v] > 0:
            name = v
            inst_type = inst_info[v]["type"]
            if name in rlist:
                rlist[name][0] += wpub[v]
                rlist[name][1] += cite[v]
            else:
                rlist[name] = [wpub[v], cite[v], inst_type]

    return [{"name": inst_info[k]["fullname"],
             "type": inst_info[k]["type"],
             "continent": inst_info[k]["continent"],
             "country": inst_info[k]["country"],
             "wpub": v[0], "cite": v[1],
             "url": inst_info[k]["url"]
             } for k, v in rlist.items()]
