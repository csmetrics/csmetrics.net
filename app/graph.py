import os, json, csv, sys
import itertools
import networkx as nx
from operator import itemgetter

cur_path = os.path.dirname(os.path.abspath(__file__))
def create_citation_graph(f, center, ntype, num):
    G = nx.DiGraph()
    csv.field_size_limit(sys.maxsize)
    reader = csv.reader(f, delimiter=';')
    next(reader) # skip the first line
    for r in reader:
        G.add_edge(r[0], r[1], weight=r[2])

    G_nodes = []
    G_links = []
    n_from = 0
    n_to = num

    if ntype > 0:
        center_node = None
        for n in G:
            if n == center:
                center_node = n
        if center_node == None:
            raise Exception("Error: cannot find center node")

        Egograph = nx.ego_graph(G, center_node)
        to_keep = []
        for s, t, w in sorted(Egograph.edges(data='weight'),key=itemgetter(2),reverse=True):
            if ntype == 1 and t == center:
                to_keep.append((s, w))
            if ntype == 2 and s == center:
                to_keep.append((t, w))
        sorted_nodes = [n for n,v in sorted(to_keep,key=itemgetter(1),reverse=True)]
        Subgraph = Egograph.subgraph(sorted_nodes[n_from:n_to])

    else:
        to_keep = [k for k, d in sorted(G.in_degree(weight=True),key=itemgetter(1),reverse=True)]
        Subgraph = G.subgraph(to_keep[n_from:n_to])

    for n, d in Subgraph.nodes(data=True):
        if n == center and ntype == 0:
            G_nodes.append({"name": n, "group": 0, "degree": G.degree(n)})
        elif n == center and ntype > 0:
            G_nodes.append({"name": n, "group": 0, "degree": G.degree(n), "fixed": True})
        else:
            G_nodes.append({"name": n, "group": 1, "degree": G.degree(n)})
    names = [n["name"] for n in G_nodes]
    for s, t, v in Subgraph.edges(data="weight", default=1):
        G_links.append({"source": names.index(s), "target": names.index(t), "value": float(v)})

    # print(G_nodes)
    # print(G_links)
    datafile = "graph/network-{}-{}.json".format(n_from, n_to)
    network = { "nodes": G_nodes, "links": G_links }
    # print(os.path.join(cur_path, "static", datafile))
    with open(os.path.join(cur_path, "static", datafile), 'w') as outfile:
        json.dump(network, outfile)

    return datafile


def create_coauthor_graph(f, center):
    Inst_set = set()
    Author_set = {}
    Papers = {}
    reader = csv.reader(f, delimiter=',')
    for r in reader:
        if r[0] in Papers:
            Papers[r[0]]["authors"].append({
                "name": r[1],
                "inst": r[3]
            })
        else:
            Papers[r[0]] = {
                "authors": [{
                    "name": r[1],
                    "inst": r[3]
                }],
                "venue": r[4]
            }
        Inst_set.add(r[3])
        Author_set[r[1]] = ""

    author_file = open(os.path.join(cur_path, "coauthor/Authors_ANU.txt"), "r")
    for line in author_file:
        key, author = line.split('\t')
        if key in Author_set:
            Author_set[key] = author.strip()

    # print(Author_set)
    Inst_list = list(Inst_set)

    G = nx.Graph()
    for k, v in Papers.items():
        for x,y in itertools.combinations(v["authors"], 2):
            G.add_node(Author_set[x["name"]] if Author_set[x["name"]] != "" else x["name"], type=x["inst"])
            G.add_node(Author_set[y["name"]] if Author_set[y["name"]] != "" else y["name"], type=y["inst"])
            G.add_edge(Author_set[x["name"]] if Author_set[x["name"]] != "" else x["name"],\
                        Author_set[y["name"]] if Author_set[y["name"]] != "" else y["name"], conf=v["venue"])

    G_nodes = []
    G_links = []
    for n, d in G.nodes(data=True):
        if n == center:
            G_nodes.append({"name": n, "group_idx": -1, "fixed": True,\
                            "group": d["type"] if d["type"] != "" else "None", "degree": G.degree(n)})
        else:
            G_nodes.append({"name": n, "group_idx": Inst_list.index(d["type"]),\
                            "group": d["type"] if d["type"] != "" else "None", "degree": G.degree(n)})
    names = [n["name"] for n in G_nodes]
    for s, t, v in G.edges(data="conf", default=1):
        G_links.append({"source": names.index(s), "target": names.index(t), "value": v})

    datafile = "graph/coauthor.json"
    network = { "nodes": G_nodes, "links": G_links }
    # print(os.path.join(cur_path, "static", datafile))
    with open(os.path.join(cur_path, "static", datafile), 'w') as outfile:
        json.dump(network, outfile)

    return datafile
