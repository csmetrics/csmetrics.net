from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .wordcloud import createWordcloud, getVenueList
from .utils import *

@csrf_exempt
def updateTable(request):
    pub_s = int(request.POST.get("pub_syear"))
    pub_e = int(request.POST.get("pub_eyear"))
    cit_s = int(request.POST.get("cit_syear"))
    cit_e = int(request.POST.get("cit_eyear"))
    conflist = request.POST.get("conflist")
    # print(conflist, [pub_s, pub_e], [cit_s, cit_e])
    data = getPaperScore(conflist.split(' '), [pub_s, pub_e], [cit_s, cit_e])
    return JsonResponse(data, safe=False)

@csrf_exempt
def selectKeyword(request):
    keywords = request.POST.get("keyword")

    conf = []
    for key in keywords.split(','):
        conf.extend(getVenueList(key.lower()))
    set_conf = list(set(conf))
    return JsonResponse(set_conf, safe=False)

def main(request):
    # data = getExampleScore()
    tags = createWordcloud()
    return render(request, "main.html", {"tags": tags})
