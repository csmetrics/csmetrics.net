from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os, json
from random import randint
from .wordcloud import createWordcloud, getVenueList

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

@csrf_exempt
def selectKeyword(request):
    keywords = request.POST.get("keyword")
    # print(keywords)
    conf = []
    for key in keywords.split(','):
        conf.extend(getVenueList(key.lower()))
    set_conf = set(conf)
    return JsonResponse(list(set_conf), safe=False)

def main(request):
    rawdata = open(os.path.join(cur_path, "data/aamas2007affil.txt"))
    lines = rawdata.readlines()
    data = []
    for i in range(2, len(lines), 3):
        uname = lines[i].split(' ', 1)[1].strip()
        citation = float(lines[i+1].split(' ', 1)[1].strip())
        data.append((findInstitution(uname), randint(10, 400), citation, 0))

    tags = createWordcloud()
    return render(request, "main.html", {"data": data, "tags": tags})
