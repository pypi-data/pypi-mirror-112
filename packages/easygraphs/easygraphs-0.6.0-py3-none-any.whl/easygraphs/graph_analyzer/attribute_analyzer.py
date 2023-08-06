import logging
import os
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import dgl
import torch

from ..utils.utils import get_abspath
from ..utils import graph_utils
from ..utils import plot_utils

class AttributeAnalyzer():
    """
    use package networkx to get preliminary network_info of this static graph:
    1. degree info
    2. density info
    3. degree histogram
    
    Usage:
        from easygraphs.graph_analyzer.attribute_analyzer import AttributeAnalyzer
        aa = AttributeAnalyzer(gl)
        aa.run()
        gc.collect()
    """
    def __init__(self, graphloader):
        self.graphloader = graphloader

        self.dir_output = self.graphloader.dir_output + "AttributeAnalyzer/"
        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)


    def run(self):
        return self.run_algorithm(self.graphloader.data(), self.graphloader.netname, self.dir_output, labels=self.graphloader.labels)


    @classmethod
    def run_algorithm(cls, graph, netname, dir_output, labels=None):
        logging.info("Network analyzer: Attribute Analyzer starts.")
        # graph = graph.to_dglgraph()
        
        cls.analyze_graph(graph, netname, dir_output, labels)
        if labels is not None:
            n_labels = np.max(labels)
            for i in range(n_labels+1):
                classi = np.squeeze(np.nonzero(labels==i))
                g_i = graph.subgraph(classi)
                cls.analyze_graph(g_i, netname+"_label%s" % i, dir_output)

        logging.info("Network analyzer: Attribute Analyzer finished.")


    @classmethod
    def analyze_graph(cls, graph, netname, dir_output, labels=None):
        # graph = dgl.transform.compact_graphs(graph)
        graph = graph.compact()
        if labels is not None:
            id_mapper = graph.get_nid_mapper()
            labels = labels[id_mapper]

        list_info = []
        print() 
        info_graph_name = "Graph name: " + netname

        print(info_graph_name)
        list_info.append(info_graph_name)

        n_node = graph.number_of_nodes()
        n_edge = graph.number_of_edges()
        info_n_node = "Number of nodes: %d" % n_node
        info_n_edge = "Number of edges: %d" % n_edge
        print(info_n_node)
        print(info_n_edge)
        list_info.append(info_n_node)
        list_info.append(info_n_edge)

        
        # info_is_directed = "Graph is directed: " + str(not is_undirected)
        # print(info_is_directed)
        # list_info.append(info_is_directed)


        density = 1.0 * n_edge / n_node / (n_node-1)
        info_density = "Volume Density: " + str(density)
        print(info_density)
        list_info.append(info_density)


        in_degree = graph.in_degrees()
        average_degree = n_edge / n_node
        max_in_degree = np.max(in_degree)

        info_average_degree = "Average degree: " + str(average_degree)
        info_max_degree = "Max degree: " + str(max_in_degree)
        print(info_average_degree)
        print(info_max_degree)
        list_info.append(info_average_degree)
        list_info.append(info_max_degree)

        # cross class analyze
        if labels is not None:
            if np.max(labels) == 1:
                src, dst = graph.edges_between(np.nonzero(labels==0)[0], np.nonzero(labels==1)[0])
                n_cross_edges = len(src)
                info_n_cross_edges = "Cross class edges: " + str(n_cross_edges)
                print(info_n_cross_edges)
                list_info.append(info_n_cross_edges)

        with open(dir_output+netname+"_info.txt", "w") as wfp:
            for info in list_info:
                wfp.write(info+"\n")

        plot_utils.plot_data(in_degree, dir_output+"degree_scatter.png", title=netname, marker="o", labels=labels, alpha=0.3)
        plot_utils.plot_dist(in_degree, dir_output+"degree_log.png", title=netname, marker="o", labels=labels, alpha=0.3, scale_type="log")
        # graph_plot_utils.plot_spy(graph.to_csr(), dir_output, title_prefix=netname)

         # is_connected = nx.algorithms.components.is_connected(g_input)
        # info_is_connected = "Graph is connected: " + str(is_connected)
        # print(info_is_connected)
        # list_info.append(info_is_connected)

        # data_biggest_subgraph = None

        # if not is_connected:
        #     ## nx.connected_components(g_input) can only be used once
        #     n_cc = sum(1 for cc in nx.connected_components(g_input))
        #     print("Number of connnected components:", n_cc)
        #     list_cc_size = [len(c) for c in sorted(nx.connected_components(g_input), key=len, reverse=True)]
        #     print(list_cc_size)
        #     if analyze_subgraph:
        #         cnt = 0
        #         for c in nx.connected_components(g_input):
        #             if list_cc_size[cnt] < 10:
        #                 continue
        #             cnt += 1
        #             print("analyze subgraph", cnt)
        #             g_subgraph = (g_input.subgraph(c)).copy()
        #             data_subgraph = graph_utils.g2df(g_subgraph)
        #             if list_cc_size[0] == len(c):
        #                 data_biggest_subgraph = data_subgraph
        #             cls.run_algorithm(data_subgraph, net_name, dir_output, cnt)


        # if not is_connected:
        #     # data_biggest_subgraph.to_csv("biggest component.txt", header = None, index = False, sep = "\t")
        #     return data_biggest_subgraph
        # else :
        #     return data_network