'''
Author: Zeng Siwei
Date: 2021-03-29 16:43:14
LastEditors: Zeng Siwei
LastEditTime: 2021-04-02 16:23:56
Description: 
'''

import pandas as pd
import numpy as np
import logging
from collections import defaultdict

def k_hop_neighbors(graph_adm, nodes, k=1, return_seperatly=False):
    '''
    Return:
        dict_neighbor: 
            To get k hop neighbors of node i, use dict_nei[k][i]
            Type of dict_nei[k][i] is list of tuple: [(u1, w1)]

    Time Complexity:
        If return_seperatly=False, quite fast.
        Else, for worst case function "neighbors" is O(n) so O(n^(2k-1))
		
    '''
    # To make sure function is efficient.
    # dict_neighbor = dict()
    for i in range(1, k+1):
        if return_seperatly == True and isinstance(nodes, defaultdict):
            dict_tmp = defaultdict(set)
            for key in nodes.keys():
                nodes_list = nodes[key]
                dict_tmp[key] = neighbors(graph_adm, nodes_list, False)
            nodes = dict_tmp
        else:
            nodes = neighbors(graph_adm, nodes, return_seperatly)
        # dict_neighbor[i] = nodes
    # return dict_neighbor
    return nodes

def neighbors(graph, *args, **kwargs):
    return graph.neighbors(*args, **kwargs)


def relabel_node(data_network):
    logging.debug("before relabeling: " + str(data_network.iloc[0]))
    dict_relabel = {}
    cnt = 0

    data_relabel = data_network.copy(deep=True)

    for i in range(data_relabel.shape[0]):
        if not data_relabel.iat[i, 0] in dict_relabel.keys():
            dict_relabel[data_relabel.iat[i, 0]] = cnt
            cnt += 1
        if not data_relabel.iat[i, 1] in dict_relabel.keys():
            dict_relabel[data_relabel.iat[i, 1]] = cnt
            cnt += 1
        data_relabel.iat[i, 0] = dict_relabel[data_relabel.iat[i, 0]]
        data_relabel.iat[i, 1] = dict_relabel[data_relabel.iat[i, 1]]
    logging.debug("after relabeling: " + str(data_relabel.iloc[0]))
    logging.debug("#relabel node: " + str(cnt))
    logging.debug("max index before: " + str(np.max(list(dict_relabel.keys()))))

    return data_relabel, dict_relabel

def subgraph(edgelist, nodes):
    src, dst, val = edgelist
    list_src, list_dst, list_val = [], [], []
    nodes = set(nodes)
    for i in range(data_network.shape[0]):
        a = src[i]
        b = dst[i]
        if a in set_node and b in set_node: # if here is "or" then get in_subgraph()
            list_src.append(a)
            list_dst.append(b)
            list_val.append(val[i])
    return (list_src, list_dst, list_val)

def in_subgraph(edgelist, nodes):
    src, dst, val = edgelist
    list_src, list_dst, list_val = [], [], []
    nodes = set(nodes)
    for i in range(data_network.shape[0]):
        a = src[i]
        b = dst[i]
        if a in set_node or b in set_node:
            list_src.append(a)
            list_dst.append(b)
            list_val.append(val[i])
    return (list_src, list_dst, list_val)




def graph_minus(g1, g2, only_pos = 0, net_type = "nx"):
    """
    If want to get edges in g1 and not in g2, only_pos = -1
    If want to get edges in g2 and not in g1, only_pos = 1
    """
    edge_list = []
    if net_type == "nx":
        nodes1 = g1.nodes()
        nodes2 = set(g2.nodes())
    elif net_type == "adm":
        nodes1 = list(g1.keys())
        nodes2 = set(g2.keys())
        
    for node in nodes1:
        neighbors2 = set()
        if net_type == "nx":
            neighbors1 = set(g1.neighbors(node))
            if node in nodes2:
                neighbors2 = set(g2.neighbors(node))
        elif net_type == "adm":
            neighbors1 = g1[node]
            neighbors2 = g2[node]

        if only_pos != 1:
            for neighbor in neighbors1:
                if neighbor not in neighbors2:
                    edge_list.append((node, neighbor))
        if only_pos != -1:
            for neighbor in neighbors2:
                if neighbor not in neighbors1:
                    edge_list.append((node, neighbor))
    return edge_list

def csr_to_bidirected():
    # make sure the graph is undirected
    A = A.maximum(A.T)

    # remove singleton nodes (without any edges)
    filter_singletons = A.sum(1).A1 != 0
    A = A[filter_singletons][:, filter_singletons]
    X = X[filter_singletons]
    z = z[filter_singletons]

    # (optionally) make sure the graph has a single connected component
    cc = sp.csgraph.connected_components(A)[1]
    cc_filter = cc == np.bincount(cc).argmax()
    return A

def dglgraph_to_bidirected(graph):
    import dgl
    graph = dgl.remove_self_loop(graph)
    graph =  dgl.to_bidirected(graph) # to_bidirected will call to_simple
    return graph


if __name__ == '__main__':
    # g1 = nx.from_edgelist([(1, 0)])
    # g2 = nx.from_edgelist([(2, 0)])
    # g3 = graph1_minus_graph2(g1, g2, only_pos=1)
    # print(list(g3.edges()))

    g = Edgeslist()