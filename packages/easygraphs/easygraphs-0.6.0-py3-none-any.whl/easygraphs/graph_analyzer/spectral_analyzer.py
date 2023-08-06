import logging
import os
import numpy as np
import scipy.sparse.linalg as linalg
import scipy.sparse.csgraph as csgraph
import matplotlib.pyplot as plt

from ..utils.plot_utils import plot_data
from ..utils.utils import get_abspath
from ..utils import graph_utils

class SpectralAnalyzer():
    """
    use eigenvalue decomposition and SVD
    then use SpectralAnalyzer and the distribution of eigenvalue to analyze network
    """
    def __init__(self, graphloader, is_undirected = True, use_laplacian = False):
        self.graphloader = graphloader
        self.is_undirected = is_undirected
        self.use_laplacian = use_laplacian
        self.dir_output = self.graphloader.dir_output + "SpectralAnalyzer/"

        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)

    def run(self, k, sus_threshold="sqrt"):
        csr_input = self.graphloader.data().to_csr()

        if self.use_laplacian:
            csr_input = csgraph.laplacian(csr_input)
            U, s, V = self.svd(csr_input, k, "SM")
            plot_data(s, "Laplacian matrix eigenvalues", self.dir_output)
        else:
            U, s, V  = self.svd(csr_input, k, "LM")
            plot_data(s, "Adjacent matrix singular values", self.dir_output)

            # flip, because s is in increasing order
            U, V = U[:, ::-1], V.T[:, ::-1]  
            s = s[::-1]

        self.plot_eigenspokes(U, s, "U", self.dir_output)
        sus_list = self.find_topk_suspicious_subgraph(U, sus_threshold)
        for i, list_node in enumerate(sus_list):
            with open(self.dir_output + "suspicious_subgraph%s.txt" % i, "w") as wfp:
                for node in list_node:
                    wfp.write("%s\n" % node)

        return sus_list


    @classmethod
    def svd(cls, csr_input, k = 20, which = "LM"):
        '''
        Do eigen decomposition.
    
        Args:
            which : str, [‘LM’ | ‘SM’], optional
                Which k singular values to find:
                    ‘LM’ : largest singular values
                    ‘SM’ : smallest singular values
        '''

        logging.info("SpectralAnalyzer: run EVD")
        max_k = np.min(csr_input.shape)
        k = np.min([k, max_k])
        logging.debug("max dim is: " + str(max_k))

        if k == 1:
            logging.warning("The matrix has only one pivot. No need to do Eigenspokes")
            return None

        u, s, vt = linalg.svds(csr_input.asfptype(), k, which=which)

        u = np.real(u)
        s = np.real(s)
        vt = np.real(vt)

        logging.debug("shape of u: " + str(u.shape))
        logging.debug("shape of v: " + str(vt.T.shape))
        logging.debug("singular value: " + str(s))
        logging.info("SpectralAnalyzer: SVD finished")

        return u, s, vt.T

    ## to make sure every row of u, v is dominated by positives
    @classmethod
    def make_positive_dominated(cls, M):
        '''
        To make the element with largest magnitude to be positive

        Args: 
            M: A matrix with shape (n, k)
	
        '''
        for i in range(M.shape[1]):
            if abs(max(M[:, i])) < abs(min(M[:, i])):
                M[:, i] *= -1

    @classmethod
    def get_threshold_by_n(cls, n, threshold_type="sqrt"):
        if threshold_type == "sqrt":
            t = 1.0 / np.sqrt(n+1)
        elif threshold_type == "log":
            t = 1.0 / np.log(n+1)
        elif threshold_type == "log10":
            t = 1.0 / np.log10(n+1)
        elif threshold_type == "log2":
            t = 1.0 / np.log2(n+1)
        elif threshold_type == "inv":
            t = 1.0 / (n+1)
        else:
            raise ValueError("Invalid arg 'threshold_type' %s" % threshold_type)
        logging.debug("Eigenspokes subgraph threshold %s" % t)
        return t

    @classmethod
    def find_topk_suspicious_subgraph(cls, S, sus_threshold='sqrt'):
        """
        Args:
            S: Singular matrix vetors with shape (n, k).
                Note: The order of singular values must be carefully checked.

            sus_threshold: 
                if type is int, then choose top sus_threshold element in singular values.

        Returns:
            list_result: Length is k.
        """
        cls.make_positive_dominated(S)
        

        list_result = []
        if isinstance(sus_threshold, int):
            for i in range(S.shape[1]):
                x =  S[:, i]
                topk_index = np.argsort(x)[-sus_threshold:]
                list_result.append(topk_index)
        else:
            for i in range(S.shape[1]):
                x =  S[:, i]
                if isinstance(sus_threshold, list):
                    t = 1.0 / (sus_threshold[i]+1) # use provide threshold
                    logging.debug("Eigenspokes subgraph %s threshold %s" % (i, t))
                else:
                    t = cls.get_threshold_by_n(S.shape[0], sus_threshold)
 
                list_higher = list(np.where(S[:, i] >= t)[0])
                logging.debug("Eigenspokes subgraph %s: eigen %s n_outliers %s" % (i, self.s[real_index], len(list_higher)))
                list_result.append(list_higher)
        
        return list_result

    @classmethod
    def plot_eigenspokes(cls, M, s, object_name="U", dir_output="./"):
        """
        Plot or savea a eigenspokes plot.

        Args:
            M: Singular matrix vetors with shape (n, k).
                Note: The order of singular values must be carefully checked.
        """
        cls.make_positive_dominated(M)

        for i in range(M.shape[1]-1):
            plt.plot(M[:, i], M[:, i+1], 'ro', alpha = 0.3)
            plt.xlabel(object_name + "_" + str(i+1))
            plt.ylabel(object_name + "_" + str(i+2))
            plt.title("EigenSpokes"  + "\n" +
                      "Singular value(x, y): " + str(s[i]) + " " + str(s[i+1]))
            plt.savefig(dir_output + "EigenSpokes_%s_%s %s_%s.png" % (object_name, i+1, object_name, i+2))
            plt.close()
            # plt.show()


    # def eigenspokes_undi(self, k, x_lower_bound = None, y_lower_bound = None,
    #                  x_upper_bound = None, y_upper_bound = None, dir_output = None, postfix = ""):
    #     if self.s is None:
    #         self.run_A_svd()

    #     logging.info("SpectralAnalyzer: getting outliers is runninng")
    #     n_row, n_col = graph_utils.get_max_index(self.data, True)

    #     ## here's undirected graph, so n_row = n_col
    #     ## And get_outliers use matrix u with shape (n_row, k)

    #     if not x_lower_bound and not y_lower_bound and not x_upper_bound and not y_upper_bound:
    #         x_lower_bound = -1 / np.sqrt(n_row + 1)
    #         y_lower_bound = -1 / np.sqrt(n_row + 1)
    #         x_upper_bound = 1 / np.sqrt(n_row + 1)
    #         y_upper_bound = 1 / np.sqrt(n_row + 1)

    #     INF = 999999999
    #     if not x_lower_bound:
    #         x_lower_bound = -INF
    #     if not y_lower_bound:
    #         y_lower_bound = -INF
    #     if not x_upper_bound:
    #         x_upper_bound = INF
    #     if not y_upper_bound:
    #         y_upper_bound = INF

    #     logging.info("SpectralAnalyzer: bounds [%s, %s, %s, %s]" % (x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound))

    #     real_index1 = s.shape[0] - index - 1
    #     real_index2 = s.shape[0] - index - 2

    #     x = u[:, real_index1]
    #     y = u[:, real_index2]


    #     list_x_lower_outliers = [index for index in range(len(x)) if x[index] > x_lower_bound]
    #     list_y_lower_outliers = [index for index in range(len(y)) if y[index] > y_lower_bound]
    #     list_x_upper_outliers = [index for index in range(len(x)) if x[index] < x_upper_bound]
    #     list_y_upper_outliers = [index for index in range(len(y)) if y[index] < y_upper_bound]

    #     outliers_index = list(set(list_x_lower_outliers) & set(list_y_lower_outliers) &
    #                           set(list_x_upper_outliers) & set(list_y_upper_outliers))
    #     inliers_index = list(set(range(len(x))).difference(outliers_index))

    #     if dir_output:
    #         filepath_output = dir_output + "outliers"
    #         if postfix:
    #             filepath_output = filepath_output + "_" + postfix
    #         filepath_output = filepath_output + ".txt"
    #         with open(filepath_output, "w") as wfp:
    #             for outlier in list_outlier:
    #                 wfp.write(str(outlier) + "\n")
    #     return list_outlier, list_inlier


    # def get_outliers(self, u, s, v, index, x_lower_bound = -9999, y_lower_bound = -9999,
    #                  x_upper_bound = 9999, y_upper_bound = 9999, inverse = False):
    #     """
    #     Given a eigenspokes graph v_index-v_index+1, and x_lower_bound, y_lower_bound, return
    #     a list of outliers and a list of inliers.
    #     """

    #     real_index1 = s.shape[0] - index - 1
    #     real_index2 = s.shape[0] - index - 2

    #     x = u[:, real_index1]
    #     y = u[:, real_index2]


    #     list_x_lower_outliers = [index for index in range(len(x)) if x[index] > x_lower_bound]
    #     list_y_lower_outliers = [index for index in range(len(y)) if y[index] > y_lower_bound]
    #     list_x_upper_outliers = [index for index in range(len(x)) if x[index] < x_upper_bound]
    #     list_y_upper_outliers = [index for index in range(len(y)) if y[index] < y_upper_bound]

    #     outliers_index = list(set(list_x_lower_outliers) & set(list_y_lower_outliers) &
    #                           set(list_x_upper_outliers) & set(list_y_upper_outliers))
    #     inliers_index = list(set(range(len(x))).difference(outliers_index))
    #     # print(outliers_index)

    #     logging.debug("#outliers: " + str(len(outliers_index)) + " #inliers: " + str(len(inliers_index)))
    #     return outliers_index, inliers_index


    
