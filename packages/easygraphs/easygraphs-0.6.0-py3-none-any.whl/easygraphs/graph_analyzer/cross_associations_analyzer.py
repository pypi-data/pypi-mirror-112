import logging
import os
import pandas as pd
import numpy as np
import pickle

from ..utils.utils import get_abspath
from ..utils import graph_ops, graph, graph_loader
from ..utils import plot_utils
from ..utils.graph import Edgelist

class CrossAssociationsAnalyzer():
    """
    use CrossAssociations Algorithm to analyze network
    """
    def __init__(self, graphloader):
        self.graphloader = graphloader
        self.dir_output =  self.graphloader.dir_output + "CrossAssociationsAnalyzer/"
        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)

    def run(self):
        highlight_node = np.squeeze(np.nonzero(self.graphloader.labels==1))
        return self.run_algorithm(self.graphloader.data().to_df(), self.graphloader.netname, self.dir_output, highlight_node)

    @classmethod
    def run_algorithm(cls, data_network, netname, dir_output, highlight_node = None):
        """
        
        """
        logging.info("Network analyzer: Cross Associations starts.")

        filepath_data = dir_output + "reorder_network.txt"
        filepath_reorder_dict = dir_output + "reorder_dict.pkl"
        filepath_cluster_index = dir_output + "cluster_index.txt"
        filepath_ca = dir_output + "ca_network.pkl"
        filepath_ca_dict = dir_output + "ca_dict.pkl"

        if not os.path.exists(filepath_data):
            data_relabel, dict_relabel = graph_ops.relabel_node(data_network)
            data_relabel.to_csv(filepath_data, header = None, index= False, sep = "\t")
            with open(filepath_reorder_dict, "wb") as f:
                pickle.dump(dict_relabel, f)
        else :
            logging.info("reorder File exists: " + filepath_data)
            with open(filepath_reorder_dict, "rb") as f:
                dict_relabel = pickle.load(f)

        if not os.path.exists(filepath_ca):
            cls.get_vertex_cluster_index(filepath_data, filepath_cluster_index)
            data_reorder, dict_reorder = cls.reorder_vertex(filepath_data, filepath_cluster_index)
            with open(filepath_ca, "wb") as f:
                pickle.dump(data_reorder, f)
            with open(filepath_ca_dict, "wb") as f:
                pickle.dump(dict_reorder, f)
        else :
            logging.info("cluster File exists: " + filepath_ca)
            with open(filepath_ca, "rb") as f:
                data_reorder = pickle.load(f)
            with open(filepath_ca_dict, "rb") as f:
                dict_reorder = pickle.load(f)

        if highlight_node is not None:
            ## Note: here're two reorder(relabel) process
            ## so have to convert input index into the index after reorder
            highlight_node_relabel = cls.get_plot_ids(highlight_node, dict_reorder, dict_relabel)

        plot_utils.plot_spy(graph.df2csr(data_reorder), dir_output, highlight_ids = highlight_node_relabel)
        logging.info("Network analyzer: Cross Associations finished")

    @classmethod
    def get_plot_ids(cls, ids, dict_reorder, dict_relabel):
        plot_ids = []
        for x in ids:
            tmp = dict_relabel[x]
            plot_ids.append(dict_reorder[tmp])
        return plot_ids

    @classmethod
    def get_origin_ids(cls, ids, dict_reorder, dict_relabel):
        origin_ids = []
        reorder2relabel = dict()
        for key, value in dict_reorder.items():
            reorder2relabel[value] = key

        relabel2origin = dict()
        for key, value in dict_relabel.items():
            relabel2origin[value] = key
        
        for x in ids:
            relabel_id = reorder2relabel[x]
            origin_ids.append(relabel2origin[relabel_id])
        return origin_ids

    @classmethod
    def get_vertex_cluster_index(cls, filepath_data, filepath_output, force_override = False):
        import matlab
        import matlab.engine

        filepath_code = get_abspath("../resource/CrossAssociations/")

        eng = matlab.engine.start_matlab()
        # eng.eval("",nargout=0)

        eng.workspace['filename_input'] = filepath_data
        eng.workspace['filename_output'] = filepath_output
        eng.workspace['dir_code'] = filepath_code
        eng.eval("s=dlmread(filename_input);", nargout=0)
        eng.eval("s(:,3) = 1;", nargout=0)
        eng.eval("s(:,1) = s(:,1)+1;", nargout=0)
        eng.eval("s(:,2) = s(:,2)+1;", nargout=0)
        eng.eval("A=spconvert(s);", nargout=0)
        eng.eval("isSelfGraph = true;", nargout=0)
        eng.eval("addpath(dir_code);", nargout=0)
        eng.eval("[k,l,Nx,Ny,Qx,Qy,Dnz] = cc_search(A,'hellscream',isSelfGraph);", nargout=0)

        ## save data into file
        eng.eval("fid = fopen(filename_output,'W');", nargout=0)
        eng.eval("for i=1:length(Qx);fprintf(fid,'%d\\n',Qx(i));end;", nargout=0)
        eng.eval("fclose(fid);", nargout=0)

        eng.quit()

        '''
        filename = 'cross associations 20k stage'
        s=dlmread(filename); s(:,3)=1; A=spconvert(s);
        isSelfGraph = true;
        [k,l,Nx,Ny,Qx,Qy,Dnz] = cc_search(A,'hellscream',isSelfGraph);
        fid = fopen([filename,' output_row_clusters'],'W');
        for i=1:length(Qx);
        fprintf(fid,'%d\n',Qx(i));
        end
        fclose(fid)
        '''

    @classmethod
    def get_ca_cluster(cls, filepath_cluster_index):
        """
        load ca cluster output
        """

        data_ca_cluster = pd.read_table(filepath_cluster_index, header=None)
        n_element = data_ca_cluster.shape[0]

        n_ca_cluster = data_ca_cluster.max()[0]
        logging.debug("Here're " + str(n_ca_cluster) + " clusters")

        x_ca_output = np.zeros((n_ca_cluster, n_element), dtype="int")
        x_ca_cnt = np.zeros((n_ca_cluster, ), dtype="int")

        for i in range(data_ca_cluster.shape[0]):
            cluster = (int)(data_ca_cluster.iat[i, 0] - 1)
            x_ca_output[cluster][x_ca_cnt[cluster]] = i + 1
            x_ca_cnt[cluster] = x_ca_cnt[cluster] + 1
        logging.debug("#element: " + str(x_ca_cnt.sum()))

        return n_ca_cluster, x_ca_cnt, x_ca_output, n_element

    @classmethod
    def get_dict_ca_reorder(cls, filepath_cluster_index):
        """
        load cluster A_svd_result by function get_ca_cluster(stage)
        """

        n_ca_cluster, x_ca_cnt, x_ca_output, n_element = cls.get_ca_cluster(filepath_cluster_index)
        dict_ca_reorder = {}
        cnt = 0
        for i in range(n_ca_cluster):
            for j in range(x_ca_cnt[i]):
                cnt = cnt +1
                dict_ca_reorder[x_ca_output[i][j]-1] = n_element - cnt
        while cnt < n_element:
            cnt += 1
            dict_ca_reorder[cnt] = n_element - cnt
        logging.debug("Len of dict_reorder: " + str(len(dict_ca_reorder)))

        return dict_ca_reorder, n_element

    @classmethod
    def reorder_vertex(cls, filepath_data, filepath_cluster_index):
        """
        use dict_ca_reorder to reorder the vertexes in stage
        get processed data by get_dict_ca_reorder(stage)

        Args:
            by : "pairs" means the vertexes of one stage will be reorder by the cluster network_info of the same stage.
                You can also input a int number to use the cluster network_info of one stage reordering of all stages.

        Returns:
            A_svd_result: a dict contains argument "by" and a list of ndarray type data needed to be spy


        """
        logging.info("Cross Associations: reordering vertexes")
        src, dst, val = graph_loader.load_graph(filepath_data)
        edgelist = Edgelist(src, dst, val)
        data_network = edgelist.to_df()

        dict_ca_reorder, _ = cls.get_dict_ca_reorder(filepath_cluster_index)

        x_reorder = np.zeros((data_network.shape[0], 3))
        for i in range(data_network.shape[0]):
            x_reorder[i][0] = dict_ca_reorder[(int)(data_network.iat[i, 0])]
            x_reorder[i][1] = dict_ca_reorder[(int)(data_network.iat[i, 1])]
            x_reorder[i][2] = data_network.iat[i, 2]

        data_reorder = pd.DataFrame(x_reorder)

        logging.info("Cross Associations: vertexes are reordered")

        return data_reorder, dict_ca_reorder
  
    def evaluate_result(self, plot_ids):
        filepath_reorder_dict = self.dir_output + "reorder_dict.pkl"
        filepath_ca_dict = self.dir_output + "ca_dict.pkl"
        with open(filepath_reorder_dict, "rb") as f:
                dict_relabel = pickle.load(f)
        with open(filepath_ca_dict, "rb") as f:
            dict_reorder = pickle.load(f)
        origin_ids = self.get_origin_ids(plot_ids, dict_reorder, dict_relabel)

        from sklearn.metrics import classification_report, roc_auc_score
        from ..utils.math import scale
        from ..utils.evaluate_utils import plot_roc_curve

        ca_labels = np.zeros(self.graphloader.data().number_of_nodes()).astype(int)
        ca_labels[origin_ids] = 1

        AUC = roc_auc_score(self.graphloader.labels, ca_labels)
        print("AUC", AUC)
        plot_roc_curve(self.graphloader.labels, ca_labels, self.dir_output, identifier=self.graphloader.netname+"_"+str(AUC))
        
        print(sum(ca_labels))
        print(classification_report(self.graphloader.labels, ca_labels))
        return origin_ids
