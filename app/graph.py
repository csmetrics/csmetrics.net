import os, json, csv, sys
import networkx as nx
from operator import itemgetter

cur_path = os.path.dirname(os.path.abspath(__file__))
def create_graph(f, center, ntype, num):
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
        to_keep = [k for k, d in sorted(G.degree(weight=True),key=itemgetter(1),reverse=True)]
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
