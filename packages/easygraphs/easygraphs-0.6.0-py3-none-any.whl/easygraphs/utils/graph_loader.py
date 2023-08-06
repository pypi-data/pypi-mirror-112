'''

Author: Zeng Siwei
Date: 2020-09-30 13:51:45
LastEditors: Zeng Siwei
LastEditTime: 2021-04-13 12:00:53
Description: 

'''

import pandas as pd
import logging, os, re
import networkx as nx
import scipy
import numpy as np
from ..global_context import *
from .utils import get_abspath, strip_postfix
from .io_utils import load_graph
from .graph import *
from .dataset import Dataset

logging.basicConfig(level=logging.NOTSET)

class GraphLoader(object):
    """
    Load one static graph and provide dir control for futher tasks like analyzing.
    
    Usage:
        Pass this object to analysis functions with output_path and the graph.

    """
    def __init__(self, *args, **kwargs):
        if args:
            if isinstance(args[0], Dataset):
                self._init_by_dataset(*args, **kwargs)
            elif isinstance(args[0], str):
                self._init_by_filename(*args, **kwargs)
            else:
                self._init_by_graph(*args, **kwargs)
        else:
            raise ValueError("Non valid arguments.")

        logging.info("graph Loaded.")

    def _init_by_graph(self, graph, netname, **kwargs):
        '''
        Args: 
            filename: Read this file to get graph.
            netname: Name this graph.
            identifier: Add an identifier at the end of netname.
		
        '''
        ## set netname
        ## init args
        self._init_default_args(netname=netname, **kwargs)
        
        ## get graph in edgelist format
        if self.subnodes:
            graph = graph.subgraph(self.subnodes)
        self.graph = graph.to_edgelist()
        if isinstance(graph, scipy.sparse.csr_matrix):
            self._csr = graph
        else:
            self._csr = None
            

    def _init_by_dataset(self, dataset, netname=None, **kwargs):
        dataset_name, graph, n_features, n_classes, features, labels, train_mask, val_mask, test_mask = dataset.get_graph()
        
        ## set netname
        if netname == None:
            netname = dataset_name.lower()
        
        ## init args
        self._init_default_args(netname=netname, features=features, labels=labels,**kwargs)
        
        ## get graph in edgelist format
        if self.subnodes:
            graph = graph.subgraph(self.subnodes)
        self.graph = Edgelist(graph)
        if isinstance(graph, scipy.sparse.csr_matrix):
            self._csr = graph
        else:
            self._csr = None


    def _init_by_filename(self, filename, netname=None, **kwargs):
        ## set netname
        if netname == None:
            netname = strip_postfix(filename)

        ## init args
        self._init_default_args(netname=netname, **kwargs)

        ## read graph from file
        filepath_net = self.dir_input + filename
        if not os.path.exists(filepath_net):
            logging.info("file %s does not exist." % filepath_net)
            filepath_net = filepath_net + ".txt"
            logging.info("try to open file: %s." % filepath_net)
        self._filepath_net = filepath_net
        if not self.subnodes:
            self.graph = load_graph(self._filepath_net)
        else:
            self.graph = load_graph(self._filepath_net, subnodes=self.subnodes)
        

    def _init_default_args(self, subnodes=None, identifier=None, netname=None, dir_input="./input/", dir_output="./output/", features=None, labels=None):
        self.netname = netname
        if identifier:
            self.netname += "_" + identifier
        elif subnodes:
            self.netname += "_subnodes_" + str(len(subnodes))
        
        self.dir_input = dir_input # the relative path to the main (calling) file
        self.dir_output = dir_output + self.netname + "/" # the relative path to the main (calling) file
        self.subnodes = subnodes
        self.features = features
        self.labels = labels
        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)
        
        ## to accelarate big file opening
        # if subnodes:
        #     filepath_output = self.dir_output + self.netname + ".txt"
        #     self.graph.save(filepath_output)
        #     logging.info("saving subgraph file to: %s." % filepath_output)

    def data(self):
        return self.graph

    def csr(self):
        if self._csr == None:
            self._csr = self.graph.to_csr()
        return self._csr

    def subgraph(self):
        #TODO
        pass
    
    def is_undirected(self):
        #TODO
        pass
        # graph = self._csr()
        # for node in graph.keys():
            # if

    def to_simple(self):
        #TODO
        pass

    def to_bidirected(self, replace=False):
        # TODO
        pass
        # return GraphLoader()
    
    def remove_graph(self):
        #TODO
        pass

    def add_self_loop(self, replace=False):
        # TODO
        pass

    def remove_self_loop(self, replace=False):
        # TODO
        pass

    def reverse(self, replace=False):
        # TODO
        pass
