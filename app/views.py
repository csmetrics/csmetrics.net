import os
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import template
from operator import itemgetter
from .utils import *
from .graph import *

TITLE = "Institutional Publication Metrics for Computer Science"

@csrf_exempt
def updateTable(request): # /update
    pub_s = int(request.POST.get("pub_syear"))
    pub_e = int(request.POST.get("pub_eyear"))
    cit_s = int(request.POST.get("cit_syear"))
    cit_e = int(request.POST.get("cit_eyear"))
    weight = request.POST.get("weight")
    conflist = request.POST.get("conflist")
    # print(conflist, [pub_s, pub_e], [cit_s, cit_e], weight)
    data = getPaperScore(conflist.split(','), [pub_s, pub_e], [cit_s, cit_e], weight!="equal")
    return JsonResponse(data, safe=False)


@csrf_exempt
def selectKeyword(request): # /select
    keywords = request.POST.get("keyword")

    conf = []
    for key in keywords.split(','):
        conf.extend(getVenueList(key.lower()))
    set_conf = list(set(conf))
    sorted_conf = sorted(set_conf, key=lambda s: s[0].lower(), reverse=False)
    return JsonResponse(sorted_conf, safe=False)


register = template.Library()
@register.simple_tag
def openMDDocs(request, html, alt_link, alt_title):
    try:
        template.loader.get_template(html)
        return render(request, "doc.html", {"exist":True,
            "template":html, "words":{"title":TITLE}})
    except template.TemplateDoesNotExist:
        return render(request, "doc.html", {"exist":False,
            "alt_link":alt_link, "alt_title":alt_title, "words":{"title":TITLE}})


def overview(request):
    return openMDDocs(request, "overview_generated.html",
        "https://github.com/csmetrics/csmetrics.org/blob/master/docs/Overview.md",
        "motivation and methodology")

def acks(request):
    return openMDDocs(request, "acks_generated.html",
        "https://github.com/csmetrics/csmetrics.org/blob/master/docs/Acks.md",
        "Acknowledgements")

def faq(request):
    return openMDDocs(request, "faq_generated.html",
        "https://github.com/csmetrics/csmetrics.org/blob/master/docs/FAQ.md",
        "FAQ")


def main(request):
    loadData()
    tags = createCategorycloud()
    return render(request, "main.html", {
        "words": {
            "title": TITLE,
            "label_year": "Year",
            "label_category": "Category",
            "label_venueweight": "Venue Weight",
            "label_venuelist": "Venue List",
            "slider_desc": "Year of publication",
            "forward": "Predicted",
            "forward_tooltip": "The prediction metric counts papers in the year range.",
            "backward": "Measured",
            "backward_tooltip": "The measured metric uses citation counts and includes all citations at anytime to papers published in the year range.",
            "ctable_label_0": "Abbr.",
            "ctable_label_1": "Conference",
            "ctable_label_2": "Weight",
            "ctable_label_2_tooltip": "A venue weight of one values all venues equally. The geometric mean venue weight assigns each venue the geometric mean of citations to papers.",
            "select_weight_option_equal": "Equal",
            "select_weight_option_geo": "Geo Mean",
            "rank_button": "Go",
            "default_alpha": 0.3,
            "select_region_all": "all",
            "select_region_cra_all": "CRA All",
            "select_region_cra_academic": "CRA Academic",
            "msg_empty_table": "Configure parameters and select Go button",
            "rtable_label_0": "Rank",
            "rtable_label_1": "Institution",
            "rtable_label_2": "Measured",
            "rtable_label_3": "Predicted",
            "rtable_label_4": "Combined",
        },
        "tags": tags
    })


cur_path = os.path.dirname(os.path.abspath(__file__))
def citingflow(request):
    typelist = ["full graph", "egograph_in", "egograph_out"]
    numlist = [10, 20, 50, 100, 200]
    datalist = ["select venue data"]
    datadir = os.path.join(cur_path, "citing_flow")
    for f in os.listdir(datadir):
        fname = f.split(".")
        if fname[0] == "citing_flow_edge" and fname[-1] == "csv":
            datalist.append(f)

    topnum = 50
    errormsg = ""
    ntype = None
    center = None
    selectfile = None
    datafile = None
    if "draw" in request.GET:
        selectfile = request.GET.get("venue")
        center = request.GET.get("center")
        ntype = request.GET.get("type")
        topnum = int(request.GET.get("topnum"))
        print("selected:", selectfile)
        print("Institution of instrest:", center)
        print("network type:", ntype)
        print("top number:", topnum)

        try:
            path = os.path.join(datadir, selectfile)
            if not os.path.exists(path):
                raise Exception("Error: venue file not exists")
            f = open(path)
            datafile = create_citation_graph(f, center, typelist.index(ntype), topnum)
        except Exception as e:
            errormsg = e
            print(errormsg)

    # print(datalist)
    return render(request, "graph.html", {
                "error":errormsg,
                "sfile":selectfile,
                "scenter":center,
                "stype":ntype,
                "stopnum":topnum,
                "numlist":numlist,
                "typelist":typelist,
                "datalist":datalist,
                "datafile":datafile
            });


def coauthor(request):
    datalist = []
    datadir = os.path.join(cur_path, "coauthor")
    for f in os.listdir(datadir):
        fname = f.split("_")
        if fname[0] == "anu":
            datalist.append(f)

    errormsg = ""
    selectfile = None
    datafile = None
    center = None
    if "draw" in request.GET:
        selectfile = request.GET.get("selectfile")
        center = request.GET.get("center")
        print("selected:", selectfile)
        print("center:", center)

        try:
            path = os.path.join(datadir, selectfile)
            if not os.path.exists(path):
                raise Exception("Error: selected file not exists")
            f = open(path)
            datafile = create_coauthor_graph(f, center)
        except Exception as e:
            errormsg = e
            print(errormsg)

    # print(datalist)
    return render(request, "coauthor.html", {
                "error":errormsg,
                "sfile":selectfile,
                "scenter":center,
                "datalist":sorted(datalist),
                "datafile":datafile
            });
