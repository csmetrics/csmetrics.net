import os, json, requests, time, csv
import http.client, urllib.request, urllib.parse, urllib.error, base64

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


def clean_inst(filename):
    # inst_alias clean
    # instfile = open(filename)
    # reader = csv.reader(instfile, delimiter=',')
    # with open('inst_alias_clean.csv', 'w', newline='') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=',')
    #     for r in reader:
    #         if len(r) == 2:
    #             spamwriter.writerow(r)
    #         else:
    #             spamwriter.writerow([r[0], "{}".format(','.join(r[1:]))])

    # change csv format for inst_fullname
    instfile = open(filename)
    reader = csv.reader(instfile, delimiter='\t')
    with open('inst_full_clean.csv', 'w', newline='') as csvfile:
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
