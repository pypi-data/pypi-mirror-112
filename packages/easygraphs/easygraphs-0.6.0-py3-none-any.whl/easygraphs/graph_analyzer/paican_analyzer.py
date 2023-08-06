'''

Author: Zeng Siwei
Date: 2021-03-23 11:38:43
LastEditors: Zeng Siwei
LastEditTime: 2021-07-13 00:46:29
Description: 

'''

import logging
import os
import numpy as np
import scipy.sparse as sp
from ..utils.io_utils import save_matrix
from ..utils.utils import get_abspath

class PAICANAnalyzer():
    """
    use PAICAN Algorithm to analyze network

    Usage:
        from easygraphs.graph_analyzer.paican_analyzer import PAICANAnalyzer
        pa = PAICANAnalyzer(gl)
        z, ca, cx = pa.run()
        gc.collect()
    """
    def __init__(self, graphloader):
        self.graphloader = graphloader
        self.dir_output = self.graphloader.dir_output + "PAICANAnalyzer/"

        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)
        
    def run(self, **kwargs):
        return self.run_algorithm(self.graphloader.data().to_csr(), self.graphloader.features, 
                    self.graphloader.labels, self.graphloader.netname, self.dir_output, **kwargs)

    @classmethod
    def run_algorithm(cls, graph_csr, features, labels, netname, dir_output, **kwargs):
        
        """
        A(graph_csr)  must be simple and bidirected in crs format. X(features) and Z(labels) are matrix.

        Returns:
            z: labels by predicting.
            ca: Structural anomaly labels.
            cx: Attribute anomaly labels.

        Example:
            import scipy.io as sio
            path = 'data/parliament/'

            A = sio.mmread(os.path.join(path, 'A.mtx')).tocsr()
            X = sio.mmread(os.path.join(path, 'X.mtx')).tocsr()
            z = np.load(os.path.join(path, 'z.npy'))
        """
        from ..resource.paican.paican import PAICAN
        
        logging.info("Graph analyzer: PAICANAnalyzer starts.")
        features = sp.csr_matrix(features)
        K = len(np.unique(labels))
        print(graph_csr.shape, features.shape, K)

        paican = PAICAN(graph_csr, features, K, verbose=True, **kwargs)
        z, ca, cx = paican.fit_predict()

        filepath_z = dir_output + netname + "_z.txt"
        filepath_ca = dir_output + netname + "_str.txt"
        filepath_cx = dir_output + netname + "_attr.txt"
        save_matrix(z, filepath_z)
        save_matrix(ca, filepath_ca)
        save_matrix(cx, filepath_cx)

        logging.info("Graph analyzer: PAICANAnalyzer finished.")
        return z, ca, cx

    def evaluate_result(self):
        from sklearn.metrics import classification_report, roc_auc_score
        from ..utils.math import scale
        from ..utils.evaluate_utils import plot_roc_curve
        import pandas as pd
        
        result_paican_z = self.dir_output + self.graphloader.netname + "_z.txt"
        result_paican_str = self.dir_output + self.graphloader.netname + "_str.txt"
        result_paican_attr = self.dir_output + self.graphloader.netname + "_attr.txt"
        data_paican_z = pd.read_csv(result_paican_z, header=None, sep="\t")
        # data_paican_attr = pd.read_csv(result_paican_attr, header=None, sep="\t")
        # data_paican_str = pd.read_csv(result_paican_str, header=None, sep="\t")
        # print(sum(data_paican_z[0]))
        # print(sum(data_paican_z[1])) # sus
        # print(sum(data_paican_attr[0]))
        # print(sum(data_paican_attr[1]))
        # print(sum(data_paican_str[0]))
        # print(sum(data_paican_str[1]))

        paican_scores = np.array(data_paican_z[0])
        print("score", paican_scores)
        AUC = roc_auc_score(self.graphloader.labels, paican_scores)
        print("AUC", AUC)
        plot_roc_curve(self.graphloader.labels, paican_scores, self.dir_output, identifier=self.graphloader.netname+"_"+str(AUC))

        paican_labels = data_paican_z[0] > data_paican_z[1]
        paican_labels = [1 if x else 0 for x in paican_labels]

        # print(paican_labels)
        print(sum(paican_labels))
        print(classification_report(self.graphloader.labels, paican_labels))