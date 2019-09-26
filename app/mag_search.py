import os, json, requests, time, csv
import http.client, urllib.request, urllib.parse, urllib.error, base64

cur_path = os.path.dirname(os.path.abspath(__file__))
MAS_URL_PREFIX = "https://api.labs.cognitive.microsoft.com"
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '' # api key required
}

def query_academic_search(type, url, query):
    if type == "get":
        response = requests.get(url, params=urllib.parse.urlencode(query), headers=headers)
    elif type == "post":
        response = requests.post(url, json=query, headers=headers)
    if response.status_code != 200:
        print("return statue: " + str(response.status_code))
        print("ERROR: problem with the request.")
        print(response.content)
        #exit()
    return json.loads((response.content).decode("utf-8"))


def get_instituion(instname):
    url = os.path.join(MAS_URL_PREFIX, "academic/v1.0/interpret")
    data = query_academic_search("get", url, {"query": instname})
    # print(data)
    interpret_expr = data["interpretations"][0]["rules"][0]["output"]["value"]
    # print(interpret_expr)
    normalized_name = interpret_expr.split("\'")[-2]
    # print(instname, normalized_name)
    return normalized_name


def replaceParentGrid():
    old_inst_file = os.path.join(cur_path, "data/inst_fullname.csv")
    new_inst_file = os.path.join(cur_path, "data/inst_fullname_grid.csv")
    grid_rel_file = os.path.join(cur_path, "data/parent_relations.csv")

    reader = csv.reader(open(grid_rel_file))
    next(reader) # skip the first line
    grid_relations = {r[0]:r[2] for r in reader}

    reader = csv.reader(open(old_inst_file))
    writer = csv.writer(open(new_inst_file, "w"))

    for r in reader:
        print(r, len(r))
        if len(r) < 3:
            writer.writerow([r[0], r[1], "", "", ""])
        else:
            writer.writerow([r[0], r[1], grid_relations[r[2]] if r[2] in grid_relations else r[2], r[3] if len(r) > 3 else "", r[4] if len(r) > 4 else ""])


def merge_grid_institutions():
    gridMap = dict()
    reader = csv.reader(open("data/grid.csv"))
    next(reader) # skip the first line
    gridMap = {r[0].strip():(r[1].strip(),r[2].strip()) for r in reader}

    reader = csv.reader(open("data/grid_types.csv"))
    next(reader)
    gridType = {r[0]:r[1] for r in reader}

    instInfo = {}
    csvfile = open('data/inst_full_clean.csv', 'w', newline='')
    spamwriter = csv.writer(csvfile, delimiter=',')

    reader = csv.reader(open("data/inst_fullname_grid.csv"))
    next(reader)
    for r in reader:
        instInfo[r[0]] = {
            "fullname": r[1].strip(),
            "grid": r[2].strip(),
            "url": r[3].strip(),
            "wiki": r[4].strip()
        }
        grid = instInfo[r[0]]["grid"]
        # print(r[0], instInfo[r[0]]["grid"], gridType[instInfo[r[0]]["grid"]])
        instInfo[r[0]]["country"] = gridMap[grid][0] if grid in gridMap else ""
        instInfo[r[0]]["continent"] = gridMap[grid][1] if grid in gridMap else "Other"
        instInfo[r[0]]["type"] = gridType[grid] if grid in gridType else "Other"

    for k,v in instInfo.items():
        spamwriter.writerow([k] + [v["fullname"],v["type"],v["continent"],v["country"],v["url"] if v["url"] != "" else v["wiki"]])


def clean_inst():
    # inst_alias clean
    # instfile = open("inst_alias.csv")
    # reader = csv.reader(instfile, delimiter=',')
    # with open('inst_alias_clean.csv', 'w', newline='') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=',')
    #     for r in reader:
    #         if len(r) == 2:
    #             spamwriter.writerow(r)
    #         else:
    #             spamwriter.writerow([r[0], "{}".format(','.join(r[1:]))])

    # change csv format for inst_fullname
    instfile = open("data/inst_fullname")
    reader = csv.reader(instfile, delimiter='\t')
    with open('data/inst_fullname.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for r in reader:
            spamwriter.writerow(r)


def gen_inst_alias(instName):
    instNameAlias = {}
    # print("instName", sorted(list(instName))[:300])
    ind = 1
    for n in sorted(list(instName)):
        try:
            key = get_instituion(n)
            print(n, "-->", key, "{}/{}".format(ind, len(instName)))
            if key in instNameAlias:
                instNameAlias[key].append(n)
            else:
                instNameAlias[key] = [n]
            time.sleep(0.5)
        except Exception as exct:
            print("           ERROR:", n)
        ind += 1
    with open('inst_alias.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for k, v in instNameAlias.items():
            spamwriter.writerow([k] + [alias for alias in v])


if __name__ == '__main__':
    # clean_inst()
    replaceParentGrid()
    merge_grid_institutions()
