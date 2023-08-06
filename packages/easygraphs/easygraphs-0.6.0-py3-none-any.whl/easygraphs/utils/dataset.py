'''
Author: Zeng Siwei
Date: 2021-03-29 20:24:55
LastEditors: Zeng Siwei
LastEditTime: 2021-07-13 01:09:15
Description: 
'''

from .graph_utils import generate_random_mask
from .graph import Edgelist, dglgraph2edges
from .utils import load_function_by_reflection, get_abspath
from .io_utils import load_graph, Downloader
from .graph_ops import dglgraph_to_bidirected
import logging
import sys, os
import pickle
import numpy as np

def read_line(filename):
    list_node = []
    with open(filename) as fp:
        for line in fp:
            line = line.strip()
            if line:
                node = int(line)
                list_node.append(node)
    return list_node


class Dataset(object):
    '''
    Usage:
        from dataset_utils import CoraDataset, RedditDataset, PubmedDataset, CoraFullDataset, 
                                    GeneDataset, YelpDataset, EpinionsDataset, StackOverflowDataset,
                                    GooglePlusDataset, DBLPDataset
        dataset = GeneDataset()
        dataset_name, in_feats, g, n_classes, features, labels, train_mask, val_mask, test_mask = dataset.get_graph()
        
    '''
    CLASS_MAP = {"CoraDataset": "dgl.data.CoraGraphDataset", "RedditDataset": "dgl.data.RedditDataset", 
                "PubmedDataset": "dgl.data.PubmedGraphDataset", "CiteseerDataset": "dgl.data.CiteseerGraphDataset",
                "CoraFullDataset": "dgl.data.CoraFullDataset", 
                }


    def __init__(self, n_features = 128, is_supervised = False, to_bidirected = False, graph_task = None, path = get_abspath("../data/")):
        '''

        Args: 
            to_bidirected: wether transform graph to undirected and simple
                        More details: https://docs.dgl.ai/en/latest/generated/dgl.to_bidirected.html
	
        Returns: 
	
        '''
        super(Dataset, self).__init__()
        self.name = self.__class__.__name__
        self.n_features = n_features # GNN embedding dim
        self.is_supervised = is_supervised
        self.graph_task = graph_task
        self.path = path

        self._g = None
        self.graph = self._call_subclass_load_data()

        # For supervised learning
        self.n_classes = None
        self.features = None
        self.labels = None
        self.train_mask = None
        self.test_mask = None
        self.val_mask = None

        if is_supervised:
            self._call_subclass_load_supervised_settings()

        if to_bidirected:
            if self._g is not None:
                self.graph = dglgraph_to_bidirected(self._g)
            else:
                self.graph.to_bidirected(replace=True)
                self.graph.remove_self_loop(replace=True)

    def _call_subclass_load_data(self):
        if self.__class__.__name__ in self.CLASS_MAP.keys():
            # import dgl.data
            dataset = load_function_by_reflection(self.CLASS_MAP[self.__class__.__name__])()
            self._g = dataset[0]
            # return Edgelist(self.g)
            return dglgraph2edges(self._g)

        child_method = getattr(self, '_load_data', None)
        if child_method is not None:
            return child_method()
        else:
            raise NotImplementedError(self.__class__.__name__ + " _load_data not implemented")


    def _call_subclass_load_supervised_settings(self):
        if self.__class__.__name__ in self.CLASS_MAP.keys():
            dataset = load_function_by_reflection(self.CLASS_MAP[self.__class__.__name__])()
            g = dataset[0]
            self.n_classes = dataset.num_classes

            # get node feature
            self.n_features = self.features.shape[1]
            self.features = g.ndata['feat'].numpy()
            
            # get data split
            self.train_mask = g.ndata['train_mask'].numpy()
            self.val_mask = g.ndata['val_mask'].numpy()
            self.test_mask = g.ndata['test_mask'].numpy()

            # get labels
            self.labels = g.ndata['label'].numpy()
            return

        child_method = getattr(self, '_load_supervised_settings', None)
        if child_method is not None:
            child_method()
            return 
        else:
            raise NotImplementedError(self.__class__.__name__ + " _load_supervised_settings not implemented")

    def _show_info(self):
        n_edges = self.graph.number_of_edges()
        n_nodes = self.graph.number_of_nodes()
        logging.info(self.__class__.__name__ + " n_nodes: " + str(n_nodes))
        logging.info(self.__class__.__name__ + " n_edges: " + str(n_edges))
        logging.info(self.__class__.__name__ + " n_features: " + str(self.n_features))

        if self.is_supervised:
            logging.info(self.__class__.__name__ + " n_classes: " + str(self.n_classes))
            logging.info(self.__class__.__name__ + " labels: " + str(self.labels))
            logging.info(self.__class__.__name__ + " features[0, :n_features // 10]: " + str(self.features[0, :self.n_features // 10]))
            logging.info(self.__class__.__name__ + " train_mask: " + str(self.train_mask))
            logging.info(self.__class__.__name__ + " val_mask: " + str(self.val_mask))
            logging.info(self.__class__.__name__ + " test_mask: " + str(self.test_mask))
        
    def get_graph(self):
        self._show_info()
        # if self.is_supervised:
        #     assert torch.is_tensor(self.features)
        #     assert torch.is_tensor(self.labels)

        return self.name, self.graph, self.n_features, self.n_classes, self.features, self.labels, self.train_mask, self.val_mask, self.test_mask

class CoraDataset(Dataset):
    def __init__(self, *args, **kwargs):
        super(CoraDataset, self).__init__(*args, **kwargs)

class WeiboSDataset(Dataset):
    '''
    Anomaly detection dataset used in [Error-Bounded Graph Anomaly Loss for GNNs](http://www.meng-jiang.com/pubs/gal-cikm20/gal-cikm20-paper.pdf)
    Data from paper code: https://github.com/zhao-tong/Graph-Anomaly-Loss/tree/master/data/weibo_s

    Args: 
	
    Returns: 
	
    Usage: 
    

    '''

    def __init__(self, **kargs):
        super(WeiboSDataset, self).__init__(graph_task="anomaly_detection", **kargs)
    
    def _load_data(self):
        filepath = self.path + "weibo_s_graph_u2u.pkl"

        list_src, list_dst = [], []
        with open(filepath, "rb") as f:
            csr_u2u = pickle.load(f)
            for i in range(np.shape(csr_u2u)[0]):
                i_neigh = set(csr_u2u[i,:].nonzero()[1])
                for j in i_neigh:
                    list_src.append(i)
                    list_dst.append(int(j))

        return Edgelist(list_src, list_dst)

    def _load_supervised_settings(self):
        self.n_classes = 2
        with open(self.path + "weibo_s_features_bow.pkl", "rb") as f:
            self.features_bow = pickle.load(f)

        with open(self.path + "weibo_s_features_loc.pkl", "rb") as f:
            self.features_loc = pickle.load(f)

        self.features = np.concatenate([self.features_bow, self.features_loc], axis = -1)
        self.n_features = self.features.shape[1]

        with open(self.path + "weibo_s_labels_u.pkl", "rb") as f:
            self.labels = pickle.load(f).astype(int)

        self.train_mask, self.val_mask, self.test_mask = generate_random_mask(
                                    self.graph.number_of_nodes(), prob_a = 0.8, prob_b = 0.1)