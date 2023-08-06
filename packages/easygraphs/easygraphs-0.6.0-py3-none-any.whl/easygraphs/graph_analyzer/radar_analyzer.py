'''
Author: Zeng Siwei
Date: 2021-03-31 16:50:46
LastEditors: Zeng Siwei
LastEditTime: 2021-07-13 00:35:54
Description: 
'''

import logging
import os
import numpy as np
import scipy.sparse as sp
from ..utils.io_utils import save_graph, save_matrix, load_table
from ..utils.utils import get_abspath

class RadarAnalyzer():
    """
    [Radar: Residual Analysis for Anomaly Detection in Attributed Networks acc. to J.Li (2017)](http://www.public.asu.edu/~jundongl/paper/IJCAI17_Radar.pdf)

    Run Radar.
    If want run java code, use func "save_graph_for_java"
    
    Matlab Code: (Recommand):
        http://people.virginia.edu/%7Ejl6qk/code/Radar.zip

    Java Code: 
        www.github.com:szumbrunn/radar-java
        git@github.com:szumbrunn/radar-java.git
    
    Usage:
        from easygraphs.graph_analyzer.radar_analyzer import RadarAnalyzer
        ra = RadarAnalyzer(gl)
        ra.run()
    """
    def __init__(self, graphloader):
        self.graphloader = graphloader
        self.dir_output = self.graphloader.dir_output + "RadarAnalyzer/"

        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)
        
    def run(self):
        return self.run_algorithm(self.graphloader.data(), self.graphloader.features, self.graphloader.labels, 
                    self.graphloader.netname, self.dir_output)

    @classmethod
    def run_algorithm(cls, graph, features, labels, netname, dir_output, n_iters=20, alpha=0.5, beta=0.2, gamma=0.2):
        import scipy.io as scio
        # data = scio.loadmat("/Users/endlesslethe/PycharmProjects/easygraphs/resource/Radar/data/Amazon.mat")
        # print(data)
        # # print(type(data['gnd']), data['gnd'])
        # print(data['gnd'].shape)
        # print(data['X'].shape)
        # print(data['A'].shape)
        # print(labels)

        dict_weibo = dict()
        dict_weibo['gnd'] = np.reshape(labels, (-1, 1))
        dict_weibo['X'] = features
        dict_weibo['A'] = graph.to_matrix()
        # print(dict_weibo)

        filepath_data = os.path.normpath(dir_output + netname + ".mat")
        filepath_output = os.path.normpath(dir_output + netname + ".txt")
        scio.savemat(filepath_data, dict_weibo)

        logging.info("Graph analyzer: RadarAnalyzer starts.")

        import matlab
        import matlab.engine

        filepath_code = "./resource/Radar/"

        eng = matlab.engine.start_matlab()

        eng.workspace['filename_input'] = filepath_data
        eng.workspace['filename_output'] = filepath_output
        eng.workspace['dir_code'] = filepath_code
        eng.eval("addpath(dir_code);", nargout=0)

        ## set args
        eng.workspace['niters'] = n_iters
        eng.workspace['alpha'] = alpha
        eng.workspace['beta'] = beta
        eng.workspace['gamma'] = gamma
        # eng.eval("niters = 20;", nargout=0)
        # eng.eval("alpha = 0.01;", nargout=0)
        # eng.eval("beta = 0.01;", nargout=0)
        # eng.eval("gamma = 0.1;", nargout=0)

        eng.eval("load(filename_input);", nargout=0)
        
        eng.eval("[n,~] = size(X);", nargout=0)
        eng.eval("X = normalizeFea(X, 0);", nargout=0)
        eng.eval("At = A';", nargout=0)
        eng.eval("Anew = max(A,At);", nargout=0)
        eng.eval("L = computelaplacian(Anew, 'undirected');", nargout=0)
        eng.eval("R = radar(X, A, L, alpha, beta, gamma, niters);", nargout=0)
        eng.eval("score= sum(R.*R,2);", nargout=0)
        eng.eval("[~,idx] = sort(score, 'descend');", nargout=0)

        ## plot ROC and compute AUC
        # eng.eval("gnd_data = zeros(n,2);", nargout=0)
        # eng.eval("gnd_data(:,1) = gnd;", nargout=0)
        # eng.eval("gnd_data(:,2) = score;", nargout=0)
        # eng.eval("[tp,fp] = roc([gnd_data(:,1),gnd_data(:,2)]);", nargout=0)
        # eng.eval("plot(fp,tp);", nargout=0)
        # eng.eval("auc_value = auc(gnd_data);", nargout=0)
        

        ## save data into file
        eng.eval("fid = fopen(filename_output,'W');", nargout=0)
        eng.eval("for i=1:length(score);fprintf(fid,'%d\\n',score(i));end;", nargout=0)
        eng.eval("fclose(fid);", nargout=0)

        eng.quit()

        logging.info("Graph analyzer: RadarAnalyzer finished.")

        '''
        load(Amazon.mat);

        [n,~] = size(X);
        X = normalizeFea(X, 0);
        niters = 20;

        alpha = 0.01;
        beta = 0.01;
        gamma = 0.1;
        At = A';
        Anew = max(A,At);
        L = computelaplacian(Anew, 'undirected');
        R = radar(X, A, L, alpha, beta, gamma, niters);
        score= sum(R.*R,2);
        [~,idx] = sort(score, 'descend');

        gnd_data = zeros(n,2);
        gnd_data(:,1) = gnd;
        gnd_data(:,2) = score;
        [tp,fp] = roc([gnd_data(:,1),gnd_data(:,2)]);
        plot(fp,tp);
        auc_value = auc(gnd_data);
        '''

    @classmethod
    def save_graph_for_java(cls, graph, features, netname, dir_output):
        filepath_graph = dir_output+netname+"_graph.txt"
        filepath_features = dir_output+netname+"_features.txt"
        graph.save(filepath_graph, with_shape=True)
        save_matrix(features, filepath_features, save_as_edges=True, with_shape=True)

    def evaluate_result(self):
        from ..utils.math import scale
        from sklearn.metrics import classification_report, roc_auc_score
        from ..utils.evaluate_utils import plot_roc_curve
        filepath_output = os.path.normpath(self.dir_output + self.graphloader.netname + ".txt")
        sus_score = np.array(load_table(filepath_output)[0], dtype=float)

        sus_score = np.log10(sus_score)
        sus_score = scale(sus_score)
        print("score", sus_score)
        AUC = roc_auc_score(self.graphloader.labels, sus_score)
        print("AUC", AUC)
        plot_roc_curve(self.graphloader.labels, sus_score, self.dir_output, identifier=self.graphloader.netname+"_"+str(AUC))

        radar_labels = (sus_score > 0.5).astype(int)
        print(sum(radar_labels))
        print(classification_report(self.graphloader.labels, radar_labels)) 