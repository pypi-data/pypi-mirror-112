import os
import logging
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
import networkx as nx
import numpy as np

class TriangleCount(AbstractNetworkAnalyzer):
    """
    use 1. A^3 and 2. intersection with A and A^2 to finish TriangleCount
    use function of package Networkx
    """
    @classmethod
    def run(cls, data_network):
        logging.info("Network analyzer: Triangle Count starts.")
        if not os.path.exists(PathManager.get_dir_tc()):
            os.makedirs(PathManager.get_dir_tc())

        result = cls.run_algorithm(data_network)
        cls.show_result(result)
        logging.info("Network analyzer: Triangle Count finished")

    @classmethod
    def run_algorithm(cls, data_network):
        logging.info("Triangle Count: algorithm is runninng")

        x_input = NetworkUtils.df2nparray(data_network)

        # A_svd_result = cls.A3(x_input)
        result = cls.networkx(x_input)
        logging.info("Triangle Count: algorithm finished")
        return result

    @classmethod
    def intersectionAA2(cls, x_input):
        pass

    @classmethod
    def A3(cls, x_input):
        x_triangle_num = np.zeros((network_info.n_timestamp, network_info.n_vertex))
        for i in range(network_info.n_timestamp):
            csr_input = csr_matrix((x_input[i][2], (x_input[i][0], x_input[i][1])),
                                   shape = (network_info.n_vertex, network_info.n_vertex))
            csr_input = csr_input.power(3)

            for j in range(network_info.n_vertex):
                x_triangle_num[i][j] = csr_input.diagonal()[j]
            print(csr_input.diagonal())

        print(np.sum(x_triangle_num[0]))
        print(x_triangle_num[0])
        return x_triangle_num

    @classmethod
    def networkx(cls, list_x):
        """
        Args:
            list_x : shape of ndarray is n_timestamp * 3 * （list_n_edge*2）

        Returns:
            A_svd_result : a list with n_timestamp triangle dictionary
                and each dictionary is : Number of triangles keyed by node label.

            x_result : a ndarray with shape (n_timestamp, n_gene)
                x[0][0] donates #triange of vertex 0 in stage 1
        """
        import networkx as nx

        g = nx.Graph()
        x_result = np.zeros((network_info.n_timestamp, network_info.n_vertex), dtype ="int")

        for t in range(network_info.n_timestamp):
            g.clear()
            for i in range(list_x[t].shape[1]):
                g.add_edge((int)(list_x[t][0][i]), (int)(list_x[t][1][i]))

            tri = nx.algorithms.cluster.triangles(g)
            avg_clustering = nx.algorithms.cluster.average_clustering(g)
            logging.info("TriangleCount:  the average clustering coefficient is " +
                         str(avg_clustering) + " in stage" + str(t+1))

            for x, y in tri.items():
                x_result[t][x] = y


        return x_result


    @classmethod
    def show_result(cls, result):
        """
        Now in this function, the triangle counts will be sort, and data will be disorder.
        but can use dict tri for further analyze if necessary .

        Note : We need to skip these data equal to 0 which is 90% more.

        Args:
            result : a ndarray with shape (n_timestamp, n_gene)
                x[0][0] donates #triange of vertex 0 in stage 1
        """
        from collections import Counter

        result = np.sort(result)
        plt.plot(range(network_info.n_vertex), result[0], "ro", alpha = 0.3)
        plt.savefig(PathManager.get_filepath_tc_origin(1))
        plt.close()
        # plt.show()


        for t in range(network_info.n_timestamp):
            num = t + 1

            num_total = np.sum(result[t]) / 3
            logging.debug("#triangle in total: " + str((int)(num_total)) + " in stage " + str(num))

            dict_result = Counter(result[t])
    
            X = np.log10(np.array(list(dict_result.keys())) + 1).reshape(-1, 1)  # numbers of triangles
            Y = np.log10(list(dict_result.values())).reshape(-1, 1) # count


            ## calculate the slope
            from sklearn import linear_model
            regr = linear_model.LinearRegression()
            regr.fit(X, Y)

            # 模型结果与得分
            # logging.debug('Coefficients: ' + str(regr.coef_))
            # logging.debug("Intercept: " + str(regr.intercept_))
            regr_rss = np.mean((regr.predict(X) - Y) ** 2)
            # logging.debug("RSS : %.8f" % regr_rss)  # 残差平方和
            # plt.plot(X, regr.predict(X), color='blue', linewidth=3)

            plt.plot(X, Y, "ro", alpha=0.3)
            plt.xlabel("log(#triangle)")
            plt.ylabel("log(count)")
            # plt.title("TriangleCount stage" + str(num) + "\n" +
            #           'Coefficients: ' + str(regr.coef_[0][0]) + " Intercept: " +
            #           str(regr.intercept_[0]) + "\nTotal: " + str((int)(num_total)))
            plt.title("TriangleCount at stage" + str(num) + "\n")

            plt.savefig(PathManager.get_filepath_tc_log(num))
            plt.close()
            # plt.show()
