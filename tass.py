import networkx as nx
import pylab as plt
import numpy as np


def draw_graph(g, out_filename):
    nx.draw(g)
    nx.draw_random(g)
    nx.draw_circular(g)
    nx.draw_spectral(g)

    plt.savefig(out_filename)


def get_clique_range_dict(list_of_cliques):
    sorted_cliques = sorted(list_of_cliques,
                            key=lambda n: -len(n))
    clique_dict = {}
    for clique in sorted_cliques:
        clique_size = len(clique)
        if clique_size in clique_dict:
            prev_val = clique_dict[clique_size]
        else:
            prev_val = 0
        clique_dict[clique_size] = prev_val + 1

    # fill zeros if no range
    for i in range(0, len(sorted_cliques[0])):
        if i in clique_dict:
            continue
        else:
            clique_dict[i] = 0

    return clique_dict


def draw_cliques_rank_plt(dictionary, out_filename):
    print dictionary

    ind = np.arange(len(dictionary))
    plt.bar(ind,
            dictionary.values(),
            align='center',
            width=0.2,
            color='green')
    plt.xticks(ind, dictionary.keys())
    plt.ylim(0, max(dictionary.values()) + 20)
    plt.title("All maximal cliques ")
    plt.xlabel("Range")
    plt.ylabel("Number of cliques")

    plt.savefig(out_filename)


def read_graph(graph_filename):
    g = nx.read_graphml(graph_filename)

    # print short summary about read graph
    print nx.info(g)
    print "Is directed: ", g.is_directed()

    return g


def top_5_map_entry_sorted_by_val(in_map):
    sorted_map = sorted(in_map.iteritems(),
                        key=lambda n: -n[1])

    return sorted_map[0:5]


if __name__ == "__main__":
    # http://nexus.igraph.org/api/dataset_info?id=14&format=html
    multi_di_graph = read_graph("celegansneural.GraphML")

    # convert MultiDiGraph to Graph representation
    print "\nConverting graph from MultiDiGraph (directed graph " \
          "that can store multiedges) to Graph.\n"

    graph = nx.Graph(multi_di_graph)

    # save graph to pajek format
    nx.write_pajek(graph, 'celegansneural_in_pajek.net')

    print nx.info(graph)
    print "Is directed: ", graph.is_directed(), "\n"

    print "Number of connected components: ", nx.number_connected_components(graph)

    # max(nx.connected_components(graph), key=len)
    largest_cc = nx.connected_component_subgraphs(graph)[0]
    print "Size (edges) of largest connected components: ", largest_cc.number_of_edges(), " edges"
    print "Range (nodes) of largest connected component: ", largest_cc.number_of_nodes(), " nodes"

    # posrednictwo*
    top_bet = top_5_map_entry_sorted_by_val(nx.betweenness_centrality(largest_cc))

    # bliskosc
    top_clos = top_5_map_entry_sorted_by_val(nx.closeness_centrality(largest_cc))

    # ranga
    top_rank = top_5_map_entry_sorted_by_val(nx.pagerank(largest_cc))

    print top_bet
    print top_clos
    print top_rank

    max_cliques = list(nx.find_cliques(largest_cc))

    draw_cliques_rank_plt(get_clique_range_dict(max_cliques), "kliki.png")

    print "Number of max cliques in graph: ", len(max_cliques)
