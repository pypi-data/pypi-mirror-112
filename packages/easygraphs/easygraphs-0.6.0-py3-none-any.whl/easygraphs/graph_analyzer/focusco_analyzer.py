'''
Author: Zeng Siwei
Date: 2021-04-01 16:36:24
LastEditors: Zeng Siwei
LastEditTime: 2021-04-13 11:50:31
Description: 
'''

import logging
import os
import numpy as np
import scipy.sparse as sp
from ..utils.io_utils import save_graph, save_matrix 
from ..utils.utils import get_abspath

class FocusCOAnalyzer():
    """
    Save graph and featrues for Java Code.
    
    Java Code: 
        www.github.com/phanein/focused-clustering
        git@github.com:phanein/focused-clustering.git
    Java Implementation of [Focused Clustering and Outlier Detection in Large Attributed Graphs](https://dl.acm.org/doi/abs/10.1145/2623330.2623682)

    Usage:
        from easygraphs.graph_analyzer.focusco_analyzer import FocusCOAnalyzer
        fa = FocusCOAnalyzer(gl)
        fa.run()

        # run matlab
        focusco.bat weibosdataset_graph_matlab.txt weibosdataset_features_matlab.txt weibosdataset_similar_matlab.txt
        
        # run java
        -input focusco.out.weighted.edges -output_directory ./
    """
    def __init__(self, graphloader):
        self.graphloader = graphloader
        self.dir_output = get_abspath("../output/" + self.graphloader.netname + "/FocusCOAnalyzer/")

        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)
        
    def run(self, *args, **kwargs):
        return self.run_algorithm(self.graphloader.data(), self.graphloader.features, self.graphloader.labels,
                    self.graphloader.netname, self.dir_output, *args, **kwargs)

    @classmethod
    def _get_k_similar_pair_from_each_communities(cls, labels, k):
        assert np.max(labels) == 1
        sort_index = np.argsort(labels)
        nodelist = sort_index[:k]
        pair_list = []
        for i in range(1, len(nodelist)):
            pair_list.append((nodelist[i-1], nodelist[i]))

        nodelist = sort_index[-k:]
        for i in range(1, len(nodelist)):
            pair_list.append((nodelist[i-1], nodelist[i]))
        return pair_list


    @classmethod
    def run_algorithm(cls, graph, features, labels, netname, dir_output, k=15):
        filepath_graph = dir_output+netname+"_graph_java.txt"
        filepath_graph_mat = dir_output+netname+"_graph_matlab.txt"
        filepath_features = dir_output+netname+"_features_matlab.txt"
        filepath_similar = dir_output+netname+"_similar_matlab.txt"

        # graph.save(filepath_graph, with_shape=False)
        graph.save(filepath_graph_mat, with_shape=False, with_weight=False, sep=" ", start_index=1)
        save_matrix(features, filepath_features, save_as_edges=False, with_shape=False, sep=' ', start_index=1)

        pair_list = cls._get_k_similar_pair_from_each_communities(labels, k)
        with open(filepath_similar, "w") as wfp:
            for item in pair_list:
                    wfp.write(" ".join([str(x+1) for x in item])+"\n")
    
    def evaluate(self):
        pass

    def evaluate_result(self, filepath):
        from sklearn.metrics import classification_report, roc_auc_score
        from ..utils.math import scale
        from ..utils.evaluate_utils import plot_roc_curve
        import pandas as pd
        
        focusco_cluster = pd.read_csv(filepath, header=None, sep=" ", dtype=int)

        focusco_labels = focusco_cluster[1] != 4
        focusco_labels = [1 if x else 0 for x in focusco_labels]

        AUC = roc_auc_score(self.graphloader.labels, focusco_labels)
        print("AUC", AUC)
        plot_roc_curve(self.graphloader.labels, focusco_labels, self.dir_output, identifier=self.graphloader.netname+"_"+str(AUC))

        print(sum(focusco_labels))
        print(classification_report(self.graphloader.labels, focusco_labels))