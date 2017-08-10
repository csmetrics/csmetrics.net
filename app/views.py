from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .wordcloud import createWordcloud, getVenueList
from .utils import *

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
    data = getExampleScore()
    tags = createWordcloud()
    return render(request, "main.html", {"data": data, "tags": tags})
