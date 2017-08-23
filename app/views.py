from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter
from .wordcloud import *
from .utils import *

@csrf_exempt
def updateTable(request):
    pub_s = int(request.POST.get("pub_syear"))
    pub_e = int(request.POST.get("pub_eyear"))
    cit_s = int(request.POST.get("cit_syear"))
    cit_e = int(request.POST.get("cit_eyear"))
    weight = request.POST.get("weight")
    conflist = request.POST.get("conflist")
    # print(conflist, [pub_s, pub_e], [cit_s, cit_e], weight)
    data = getPaperScore(conflist.split(' '), [pub_s, pub_e], [cit_s, cit_e], weight=="GEOMEAN")
    return JsonResponse(data, safe=False)

@csrf_exempt
def selectKeyword(request):
    keywords = request.POST.get("keyword")

    conf = []
    for key in keywords.split(','):
        conf.extend(getVenueList(key.lower()))
    set_conf = list(set(conf))
    sorted_conf = sorted(set_conf, key=itemgetter(2), reverse=True)
    return JsonResponse(sorted_conf, safe=False)

def main(request):
    loadData()
    # data = getExampleScore()
    # tags = createWordcloud()
    tags = createCategorycloud()
    return render(request, "main.html", {
        "words": {
            "title": "TITLE",
            "forward": "Estimated",
            "forward_tooltip": "Estimated impact is calculated by the number of publication",
            "backward": "Measured",
            "backward_tooltip": "Measured impact is calculated by the number of citations",
            "ctable_label_0": "Abbr.",
            "ctable_label_1": "Conference",
            "ctable_weight_option_equal": "Equal",
            "ctable_weight_option_geo": "Geo Mean",
            "rank_button": "Rank",
            "rtable_label_0": "Rank",
            "rtable_label_1": "Institution",
            "rtable_label_2": "Meas",
            "rtable_label_3": "w.Meas",
            "rtable_label_4": "Est",
            "rtable_label_5": "w.Est",
            "rtable_label_6": "Combined",
        },
        "tags": tags
    })
