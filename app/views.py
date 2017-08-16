from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .wordcloud import createWordcloud, getVenueList
from .utils import *

@csrf_exempt
def updateTable(request):
    syear = int(request.POST.get("syear"))
    eyear = int(request.POST.get("eyear"))
    conflist = request.POST.get("conflist")
    print(conflist, syear, eyear)
    data = getPaperScore(conflist.split(' '), syear, eyear)
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
    data = getExampleScore()
    tags = createWordcloud()
    return render(request, "main.html", {"data": data, "tags": tags})
