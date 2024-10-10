from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import template
from django.contrib import messages
from urllib.parse import unquote
from .utils import *

URL_BASE = "http://csmetrics.net/shareable"
TITLE = "Institutional Publication Metrics for Computer Science"

labels = {
    "url_base": URL_BASE,
    "title": TITLE,
    "label_year": "Year",
    "label_category": "Category",
    "label_venueweight": "Venue Weight",
    "label_venuelist": "Venue List",
    "slider_desc": "Year of publication",
    "forward": "Predicted",
    "forward_tooltip": "The prediction metric counts papers in the year range.",
    "backward": "Measured",
    "backward_tooltip": "The measured metric uses citation counts and includes all citations at any time to papers published in the year range.",
    "ctable_label_0": "Abbr.",
    "ctable_label_1": "Type",
    "ctable_label_2": "Fullname",
    "ctable_label_3": "Weight",
    "weight_option_tooltip": "A venue weight of one values all venues equally. The geometric mean venue weight assigns each venue the geometric mean of citations to papers.",
    "select_weight_option_equal": "Equal",
    "select_weight_option_geo": "Geo Mean",
    "rank_button": "Go",
    "select_inst_types": ["All", "Education", "Company", "Government", "Facility", "Nonprofit", "Healthcare", "Archive", "Other"],
    "select_inst_regions": continent_ordered,
    "msg_empty_table": "Calculating the Ranking...",
    "rtable_label_0": "Rank",
    "rtable_label_1": "Institution",
    "rtable_label_2": "Measured",
    "rtable_label_3": "Predicted",
    "rtable_label_4": "Combined",
}


@csrf_exempt
def update_table(request):  # /update
    pub_s = int(request.POST.get("pub_syear"))
    pub_e = int(request.POST.get("pub_eyear"))
    cit_s = int(request.POST.get("cit_syear"))
    cit_e = int(request.POST.get("cit_eyear"))
    weight = request.POST.get("weight")
    conflist = request.POST.get("conflist")
    
    data = get_paper_score(conflist.split(','), [pub_s, pub_e], [cit_s, cit_e], weight != "equal")
    return JsonResponse(data, safe=False)


@csrf_exempt
def venue_list(request):  # /venue
    return JsonResponse(get_venue_list(), safe=False)


def get_venue_list_from_keywords(keywords):
    conf = get_venue_list(keywords)
    sorted_conf = sorted(conf, key=lambda s: s[0].lower(), reverse=False)
    return sorted_conf


register = template.Library()

@register.simple_tag
def open_md_docs(request, html, alt_link, alt_title):
    try:
        template.loader.get_template(html)
        return render(request, "doc.html", {"exist": True, "template": html, "words": {"title": TITLE}})
    except template.TemplateDoesNotExist:
        return render(request, "doc.html", {"exist": False, "alt_link": alt_link, "alt_title": alt_title, "words": {"title": TITLE}})


def overview(request):
    return open_md_docs(request, "overview_generated.html", 
                        "https://github.com/csmetrics/csmetrics.net/blob/master/docs/Overview.md", 
                        "motivation and methodology")


def acks(request):
    return open_md_docs(request, "acks_generated.html",
                        "https://github.com/csmetrics/csmetrics.net/blob/master/docs/Acks.md",
                        "Acknowledgements")


def faq(request):
    return open_md_docs(request, "faq_generated.html",
                        "https://github.com/csmetrics/csmetrics.net/blob/master/docs/FAQ.md",
                        "FAQ")


def shareable(request):
    load_data()
    tags = create_category_cloud()
    year_range = [2007, 2023]
    try:
        pub = unquote(request.GET.get("pub"))
        cit = unquote(request.GET.get("cit"))
        weight = request.GET.get("weight")
        alpha = request.GET.get("alpha")
        keywords = unquote(request.GET.get("keywords"))
        conflist = unquote(request.GET.get("venues"))
        inst_type = request.GET.get("type")
        inst_region = request.GET.get("region")
        inst_country = request.GET.get("country")

        pub_s, pub_e = [int(x) for x in pub.split(',')]
        cit_s, cit_e = [int(x) for x in cit.split(',')]

        values = {
            "yearRange": year_range,
            "pubYears": [max(year_range[0], pub_s), min(year_range[1], pub_e)],
            "citYears": [max(year_range[0], cit_s), min(year_range[1], cit_e)],
            "lockedState": str(pub_s - 1 == cit_e),
            "weight": weight,
            "alpha": alpha,
            "keywords": keywords.split(',') if keywords else [],
            "venues": conflist.split(',') if conflist else [],
            "inst_type": inst_type if inst_type else "All",
            "inst_region": inst_region if inst_region else "All",
            "inst_country": inst_country if inst_country else "",
        }

        messages.info(request, "Ranking generated from shareable link.")
        return render(request, "main.html", {
            "default": values,
            "words": labels,
            "tags": tags
        })

    except Exception as e:
        messages.error(request, "Invalid link. Returning to default settings.")
        return render(request, "main.html", {
            "default": {
                "yearRange": year_range,
                "pubYears": [2021, 2023],
                "citYears": [2007, 2020],
                "lockedState": "True",
                "weight": "geomean",
                "alpha": str(0.3),
                "keywords": tags,
                "venues": [t[0] for t in get_venue_list_from_keywords(tags)],
                "inst_type": "All",
                "inst_region": "All",
                "inst_country": "",
            },
            "words": labels,
            "tags": tags
        })


def main(request):
    load_data()
    tags = create_category_cloud()
    year_range = [2007, 2023]
    default_values = {
        "yearRange": year_range,
        "pubYears": [2021, 2023],
        "citYears": [2007, 2020],
        "lockedState": "True",
        "weight": "geomean",
        "alpha": str(0.3),
        "keywords": tags,
        "venues": [t[0] for t in get_venue_list_from_keywords(tags)],
        "inst_type": "All",
        "inst_region": "All",
        "inst_country": "",
    }
    return render(request, "main.html", {
        "default": default_values,
        "words": labels,
        "tags": tags
    })
