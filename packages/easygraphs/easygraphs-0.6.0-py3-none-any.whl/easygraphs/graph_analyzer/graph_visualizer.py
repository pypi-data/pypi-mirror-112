'''

Author: Zeng Siwei
Date: 2021-04-06 19:35:54
LastEditors: Zeng Siwei
LastEditTime: 2021-04-06 19:35:55
Description: 

'''

class GraphVisualizer(object):
    def plot_graph(cls):
        from ..utils.plot_utils import plot_graph_plotly, get_colors
        plot_graph_plotly(gl.dir_output, gl.netname, G=gl.data().to_nxgraph())
    
    def feature_tsne(cls):
        from ..utils.plot_utils import plot_tsne
        plot_tsne(features, labels)

    def plot_egonetwork(cls, k=1):
        from ..utils.plot_utils import plot_graph_plotly, get_colors

        dict_nei = k_hop_neighbors(gl.data().to_adm(), list(range(gl.data().number_of_nodes())), 1, True)
        print(len(dict_nei.keys()))

        for key in dict_nei.keys():
            print(key)
            list_nei = list(dict_nei[key])
            list_nei.append(key)

            edgelist = gl.data().subgraph(list_nei)
            nx_g = edgelist.to_nxgraph()
            
            colors = ['green', 'red']
            node_colors = [colors[x] for x in gl.labels]
            node_colors[key] = 'yellow'
            plot_graph_plotly(gl.dir_output+"VisEgo/", "label%s_node%s"%(gl.labels[key], key), G=nx_g, node_colors=node_colors, node_scale=10, save_type="png", layout="spring")
            gc.collect()

