'''

Author: Zeng Siwei
Date: 2021-01-04 16:49:50
LastEditors: Zeng Siwei
LastEditTime: 2021-04-13 01:01:50
Description: 

'''

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import networkx as nx
from collections import defaultdict

from .io_utils import save_graph

'''

transform the data of a graph into different types such as networkx.Graph, ndarray or sparse matrix.

Usage: 
	edgelist = Edgelist(list_src, list_dst) 
    df = edgelist.to_df()
    g = edgelist.to_nxgraph()
    csr_plot = edgelist.to_csr()
'''


def number_of_nodes(src, dst, return_type="all"):
    '''
    Returns number of src and dst nodes = max(src/dst) + 1

    Usage: 

    '''
    if return_type == "all":
        return int(np.max((np.max(src), np.max(dst))) + 1)
    elif return_type == "uv":
        return int(np.max(src)+1), int(np.max(dst)+1)


class BasicGraph(object):
    def __init__(self):
        pass
    
    def number_of_nodes(self):
        raise NotImplementedError

    def data(self):
        '''
        Use this to get data.
        '''
        raise NotImplementedError

class Edgelist(BasicGraph):
    '''
    Edgelist graph type.
    Put code for "load edges and tranform" (shown in Usage) in a function scope for memory usage.

    NOT CHANGABLE.

    Usage: 
        list_src, list_dst = generate_hyperbolic_graph(10)
        edges = Edges(list_src, list_dst) 
        df = edges2df(edges)
    '''
    def __init__(self, *args, **kwargs):
        if args:
            if isinstance(args[0], (list, np.ndarray)):
                self._init_by_uvlist(*args, **kwargs)
            elif isinstance(args[0], Edgelist):
                self._init_by_edgelist(*args, **kwargs)
            elif isinstance(args[0], (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)): 
                self._init_by_nxgraph(*args, **kwargs)
            else: # dgl.DGLGraph
                self._init_by_dglgraph(*args, **kwargs)
        else:
            raise ValueError("Non valid arguments.")


    def _init_by_uvlist(self, src=[], dst=[], val=[]):
        import copy
        self.src = copy.deepcopy(src)
        self.dst = copy.deepcopy(dst)
        self._index = 0

        ## graph shape
        self._is_change = False
        self._n_row = None
        self._n_col = None

        ## graph id mapper
        self._nid = None
        self._eid = None

        ## graph data
        self.ndata = dict()
        self.edata = dict()

        if not val:
            self.val = [1] * len(src)
        else:
            self.val = copy.deepcopy(val)

        if len(self.src) != len(self.val):
            raise RuntimeError("Number of nodes is not equal to number of edge weights.")

    def _init_by_edgelist(self, edgelist):
        src, dst, val = edgelist.data()
        self._init_by_uvlist(src, dst, val)

    def _init_by_nxgraph(self, graph):
        edges = list(graph.edges())
        src, dst = map(list, zip(*edges))
        weight = nx.get_edge_attributes(graph, 'weight')
        val = [weight[edges[i]] for i in range(len(edges))]
        self._init_by_uvlist(src, dst, val)

    def _init_by_dglgraph(self, graph):
        src, dst = graph.edges("uv")
        src = src.numpy()
        dst = dst.numpy()
        val = graph.edata.get("w", None)
        val = val.numpy() if val is not None else val
        self._init_by_uvlist(src, dst, val)


    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < self.number_of_edges():
            u, v, w = self.src[self._index], self.dst[self._index], self.val[self._index]
            self._index += 1
            return u, v, w
        else:
            self._index = 0
            raise StopIteration

    def data(self):
        return self.src, self.dst, self.val

    def get_nid_mapper(self):
        '''
        Return NID mapper

        Usage: 
            id_mapper = graph.get_nid_mapper()
            labels = labels[id_mapper]
        '''

        return self._nid

    def get_eid_mapper(self):
        return self._eid

    def _set_nid_mapper(self, _nid):
        self._nid = _nid.astype(int)

    def _set_eid_mapper(self, _eid):
        self._eid = _eid.astype(int)

    def _update_edata(self):
        for key in self.edata.keys():
            self.edata[key] = self.edata[key][self.get_eid_mapper()]

    def _update_ndata(self):
        for key in self.ndata.keys():
            self.ndata[key] = self.ndata[key][self.get_nid_mapper()]

    def save(self, *arg, **kwarg):
        '''
        Usage:
            graph.save(filepath_graph, with_shape=True)
        '''
        src, dst, val = self.data()
        save_graph(src, dst, *arg, val=val, **kwarg)

    def to_edgelist(self):
        return self

    def to_df(self):
        '''
        Usage: 
                edges = Edges(src, dst) # recommended
                df = edges2df(edges)
            Or:
                df = edges2df((src, dst, [1]*len(src)))
        '''
        src, dst, val = self.data()
        data_network = pd.DataFrame({0: src, 1: dst, 2: val})
        return data_network

    def to_dglgraph(self, graph_type="DGLGraph"):
        import dgl
        import torch
        src, dst, val = self.data()
        g = dgl.graph((src, dst), idtype=torch.int64)
        g.edata['weight'] = torch.tensor(val)
        g = dgl.to_simple(g, copy_edata=True)
        g = dgl.remove_self_loop(g)
        return g

    def to_nxgraph(self):
        src, dst, val = self.data()
        g = nx.Graph()
        g.add_weighted_edges_from(zip(src, dst, val))
        return g

    def to_csr(self):
        src, dst, val = self.data()
        n_row, n_col = self.number_of_nodes("uv")
        csr_input = csr_matrix((val, (src, dst)), shape = (n_row, n_col))
        return csr_input

    def to_adm(self):
        src, dst, val = self.data()
        return AdjMatrix(src, dst, val)

    def to_matrix(self):
        n_row, n_col = self.number_of_nodes("uv")
        m = np.zeros((n_row, n_col))
        for u, v, w in self:
            m[u][v] = w
        return m

    '''
    # 
    #    transform functions
    #
    '''

    def subgraph(self, subnodes, replace=False):
        set_subnodes = set(subnodes)
        src, dst, val = [], [], []
        for u, v, w in self:
            if u in set_subnodes and v in set_subnodes:
                src.append(u)
                dst.append(v)
                val.append(w)
        if replace == True:
            self.src = src
            self.dst = dst
            self.val = val
            self._is_change = True
            return self
        else:
            return Edgelist(src, dst, val)


    def to_simple(self, replace=False):
        dict_edge = dict()
        for u, v, w in self:
            dict_edge[(u, v)] = w
        edges = dict_edge.keys()
        src = [x[0] for x in edges]
        dst = [x[1] for x in edges]
        val = [x for x in dict_edge.values()]
        if replace == True:
            self.src = src
            self.dst = dst
            self.val = val
            self._is_change = True
            return self
        else:
            return Edgelist(src, dst, val)

    def to_bidirected(self, replace=False):
        import copy
        src, dst, val = self.data()
        src_tmp = copy.deepcopy(src)
        dst_tmp = copy.deepcopy(dst)
        src_tmp.extend(dst)
        dst_tmp.extend(src)
        val_tmp = val*2
        if replace == True:
            self.src = src_tmp
            self.dst = dst_tmp
            self.val = val_tmp
            self.to_simple(replace=True)
            self._is_change = True
            return self
        else:
            new_edges = Edgelist(src_tmp, dst_tmp, val_tmp)
            return new_edges.to_simple(replace=True)

    def remove_self_loop(self, replace=False):
        src = []
        dst = []
        val = []
        for u, v, w in self:
            if u == v:
                continue
            src.append(u)
            dst.append(v)
            val.append(w)
        if replace == True:
            self.src = src
            self.dst = dst
            self.val = val
            self._is_change = True
            return self
        else:
            return Edgelist(src, dst, val)

    def remove_edges(self):
        #TODO
        pass

    def add_self_loop(self, replace=False):
        #TODO
        # list_flag = [1] * self.number_of_nodes()
        pass

    def reverse(self, replace=False):
        if replace == True:
            tmp = self.src
            self.src = self.dst
            self.dst = tmp
            self._is_change = True
            return self
        else:
            return Edgelist(self.dst, self.src, self.val)
    
    def compact(self, replace=False):
        from .collection import Incdict
        dict_node = Incdict()
        src, dst, val = [], [], []
        for u, v, w in self:
            src.append(dict_node[u])
            dst.append(dict_node[v])
            val.append(w)
        id_map = np.zeros(len(dict_node))
        for key, value in dict_node.items():
            id_map[value] = key
        if replace == True:
            self.src = src
            self.dst = dst
            self.val = val
            self._set_nid_mapper(id_map)
            self._is_change = True
            return self
        else:
            edgelist = Edgelist(src, dst, val)
            edgelist._set_nid_mapper(id_map)
            return edgelist
    

    '''
    # 
    #    query functions
    #
    '''

    def edges(self):
        return self.src, self.dst, self.val

    def number_of_nodes(self, return_type="all"):
        '''
        Time Complexity:
            O(#edges)
        '''
        if (self._n_row is None) or (self._n_col is None) or self._is_change:
            self._n_row, self._n_col = number_of_nodes(self.src, self.dst, "uv")
        if return_type == "all":
            return np.max((self._n_row, self._n_col))
        else:
            return self._n_row, self._n_col

    def number_of_edges(self):
        '''
        Time Complexity: 
            O(1)
            The complexity of built-in len() is O(1)
        '''
        return len(self.src)

    def is_undirected(self, replace=False):
        #TODO
        pass
        # graph = self._csr()
        # for node in graph.keys():
            # if

    def in_degrees(self):
        return self._degrees(self.dst)

    def out_degrees(self):
        return self._degrees(self.src)

    def _degrees(self, nodes):
        from collections import Counter
        dict_degrees = dict(Counter(nodes))
        degrees = np.zeros(self.number_of_nodes())
        for i in range(self.number_of_nodes()):
            degrees[i] = dict_degrees[i]
        return degrees

    def neighbors(self, nodes, return_seperatly = False):
        from collections import defaultdict
        set_node = set(nodes)

        if return_seperatly:
            dict_neighbor = defaultdict(set)
            for a, b, _ in self:
                if a in set_node:
                    dict_neighbor[a].add(b)
                if b in set_node:
                    dict_neighbor[b].add(a)
            return dict_neighbor
        else:
            set_neighbor = set()
            for a, b, _ in self:
                if a in set_node:
                    set_neighbor.add(b)
                if b in set_node:
                    set_neighbor.add(a)
            return set_neighbor

    def edges_between(self, u, v):
        '''
        Return edges between set_u and set_v

        Args: 
	
        Returns: 
	
        Usage: 
	
        '''

        set_u = set(u)
        set_v = set(v)
        src = []
        dst = []
        for u, v, _ in self:
            if (u in set_u and v in set_v) or (v in set_u and u in set_v):
                src.append(u)
                dst.append(v)
        return src, dst

    
class AdjMatrix(BasicGraph):
    def __init__(self, src, dst, val=[]):
        self.adm = defaultdict(list)
        self.val = defaultdict(list)
        if not val:
            val = [1] * len(src)
        for a, b, v in zip(src, dst, val):
            self.adm[a].append(b)
            # self.adm[b].append(a)
            self.val[a].append(v)
            # self.val[b].append(v)

    def data(self):
        return self.adm

    def neighbors(self, nodes, return_seperatly=False):
        '''
		Time Complexity: O(#edges of given nodes) not O(n)
        '''
        if return_seperatly:
            dict_neighbor = defaultdict(set)
            for node in nodes:
                dict_neighbor[node] = set(self.adm[node])
            return dict_neighbor
        else:
            set_neighbor = set()
            for node in nodes:
                set_neighbor = set_neighbor.union(set(self.adm[node]))
            return set_neighbor

    def to_edges(self):
        raise NotImplementedError

    def to_g(self):
        raise NotImplementedError

    def to_csr(self):
        raise NotImplementedError


# def df2nparray(data_input):
#     """
#     Returns:
#         x_input : shape of ndarray 3 * list_n_edge
#     """
#     x_input = np.array(data_input).T
#     return x_input

def df2csr(data_input):
    n_row, n_col = number_of_nodes(data_input[0], data_input[1], return_type="uv")
    csr_input = csr_matrix((data_input[2], (data_input[0], data_input[1])),
                            shape = (n_row, n_col))
    return csr_input

# def df2g(data_input, use_networkx=False):
#     if use_networkx:
#         g = nx.Graph()
#         for i in range(data_input.shape[0]):
#             g.add_edge(int(data_input.iat[i, 0]), int(data_input.iat[i, 1]))
#     else:
#         import dgl
#         import torch
#         g = dgl.graph((list(data_input[0]), list(data_input[1])), idtype=torch.int64)
#         g = dgl.to_simple(g)
#         g = dgl.remove_self_loop(g)
#     return g

# def df2adm(data):
#     from collections import defaultdict
#     adm = defaultdict(list)
#     for i in range(data.shape[0]):
#         a = data.iat[i, 0]
#         b = data.iat[i, 1]
#         adm[a].append(b)
#         adm[b].append(a)
#     return adm

# def g2df(g_input, is_undirected = True, use_networkx=False):
#     if use_networkx:
#         data_network = nx.to_pandas_edgelist(g_input, source=0, target=1)
#     else:
#         src, dst = g_input.edges()
#         data_network = pd.DataFrame(dict(((0, list(src)), (1, list(dst)))))

#     if data_network.shape[1] == 2:
#         data_network[2] = 1
#     elif data_network.shape[1] == 3:
#         pass
#     else :
#         raise Exception("Graph has so many args.")

#     if is_undirected:
#         data_network = df_directed2undirected(data_network)

#     return data_network

def g2csr(g_input):
    return nx.to_scipy_sparse_matrix(g_input)

def csr2edges(crs_input):
    x_row = np.array(crs_input.tocoo().row)
    x_col = np.array(crs_input.tocoo().col)
    x_val = np.array(crs_input.tocoo().data)
    edges = Edgelist(x_row, x_col, x_val)
    return edges

def dglgraph2edges(graph):
    src, dst = graph.edges("uv")
    src = src.numpy()
    dst = dst.numpy()
    val = graph.edata.get("w", None)
    val = val.numpy() if val is not None else val
    return Edgelist(src, dst, val)
