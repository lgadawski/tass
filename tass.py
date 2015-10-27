import networkx as nx
import pylab as plt


def draw_graph(g, out_filename):
    nx.draw(g)
    nx.draw_random(g)
    nx.draw_circular(g)
    nx.draw_spectral(g)

    plt.savefig(out_filename)


def read_graph(graph_filename):
    g = nx.read_graphml(graph_filename)

    # print short summary about read graph
    print nx.info(g)
    print "Is directed: ", g.is_directed()

    return g


if __name__ == "__main__":
    # http://nexus.igraph.org/api/dataset_info?id=14&format=html
    multi_di_graph = read_graph("celegansneural.GraphML")

    # convert MultiDiGraph to Graph representation
    print "\n"
    print "Converting graph from MultiDiGraph (directed graph " \
          "that can store multiedges) to Graph."
    print "\n"

    graph = nx.Graph(multi_di_graph)

    print nx.info(graph)
    print "Is directed: ", graph.is_directed()