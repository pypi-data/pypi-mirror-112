from plotly.graph_objs import *
from plotly.offline import plot as offpy
import networkx as nx
import logging
import matplotlib.pyplot  as plt
import math

LAYOUT = {
        'graphviz_neato': nx.drawing.nx_agraph.graphviz_layout,
        'circular': nx.circular_layout,
        'kamada_kawai': nx.kamada_kawai_layout,
        'random': nx.random_layout,
        'shell': nx.shell_layout,
        'spectral': nx.spectral_layout,
        'spring': nx.spring_layout,
        'bipartite': nx.bipartite_layout
    }

LAYOUT_ARGS = {
    'spectral': dict(scale=0.1),
    'spring': dict(k=0.5, iterations=1000, seed=42),
    'graphviz_neato':dict(prog='neato')
}

NX_NODE_OPTIONS = (
    "nodelist",
    "node_size",
    "node_color",
    "node_shape",
    "alpha",
    "cmap",
    "vmin",
    "vmax",
    "ax",
    "linewidths",
    "edgecolors",
    "label",
)

NX_EDGE_OPTIONS = (
    "edgelist",
    "width",
    "edge_color",
    "style",
    "alpha",
    "arrowstyle",
    "arrowsize",
    "edge_cmap",
    "edge_vmin",
    "edge_vmax",
    "ax",
    "label",
    "node_size",
    "nodelist",
    "node_shape",
    "connectionstyle",
    "min_source_margin",
    "min_target_margin",
)

NX_LABEL_OPTIONS = (
    "labels",
    "font_size",
    "font_color",
    "font_family",
    "font_weight",
    "alpha",
    "bbox",
    "ax",
    "horizontalalignment",
    "verticalalignment",
)

NX_EDGE_LABEL_OPTIONS = (
    "edge_labels",
    "edge_font_size",
    "edge_font_color"
)

def plot_graph(g, layout="spring", node_labels=None, edge_labels=None, plot_options=dict(), dir_output=None, filename=None):
    '''
    Use networkx build-in draw function.

    Args:
	    node_labels : dictionary, optional (default=None)
                Node labels in a dictionary keyed by node of text labels.
        edge_labels : dictionary, optional (default=None)
                Edge labels in a dictionary keyed by edge two-tuple of text labels . 

    Usage: 
        plot_graph(self.g2, layout='spring', plot_options=dict(scale=1.0))
    '''
    logging.info("Starting plot graph")
    if not isinstance(g, nx.Graph):
        raise Exception("Graph type must be nx.Graph.")
    
    scale = plot_options.get("scale", 1.0)
    options = dict(node_color='r', alpha=0.8, labels=node_labels, edge_labels=edge_labels, 
                    node_size=15*scale, font_size=3*scale, edge_font_size=1*scale)
    options.update(plot_options)
    nx_options = {k: v for k, v in options.items() if k in (NX_NODE_OPTIONS+NX_EDGE_OPTIONS+NX_LABEL_OPTIONS)}

    pos = get_node_pos_2d(g, layout)
    # pop nodes which have no pos.
    if node_labels is not None:
        for key in list(node_labels.keys()): 
            if key not in pos:
                node_labels.pop(key)
    else:
        node_labels = dict((x, x) for x in pos.keys())

    fig = plt.figure(dpi=300)

    nx.draw_networkx(g, pos=pos, **nx_options)
    if edge_labels is not None:
        nx.draw_networkx_edge_labels(g, pos, options["edge_labels"], font_size=options["edge_font_size"])

    # output
    if dir_output:
        filepath_output = dir_output + filename + ".png"
        logging.info("Saving fig to:" + filepath_output)
        plt.savefig(filepath_output)
        plt.close()
    else :
        plt.show()
    return

def plot_spy(csr_plot, dir_output=None, title_prefix=None, highlight_ids=None, plot_options=None):
    '''
    Args: 
		
    Returns: 
		
    Usage:
        from easygraphs.utils.graph import Edgelist
        g_csr = Edgelist(self.g).to_csr()
        plot_spy(g_csr, plot_options=dict(marker='o'))
    '''
    options = dict(marker=",", color="royalblue")
    if plot_options is not None:
        options.update(plot_options)
    plt.spy(csr_plot, **options)
    filename_tmp = "spy_matrix"

    if highlight_ids is not None:
        set_node = set(highlight_ids)
        (rs, cs) = csr_plot.nonzero()
        for i in range(len(rs)):
            if rs[i] in set_node and cs[i] in set_node:
                pass
            else:
                csr_plot[rs[i], cs[i]] = 0
        options["color"] = "red"
        plt.spy(csr_plot, **options)
        filename_tmp += "_#" + str(len(highlight_ids)) + "_marked"

    if title_prefix is None:
        filename = filename_tmp
    else:
        filename = title_prefix + "_" + filename_tmp

    if dir_output:
        filepath_output = dir_output + filename + ".png"
        logging.info("Saving fig to:" + filepath_output)
        plt.savefig(filepath_output)
        plt.close()
    else :
        plt.show()


def plot_graph_plotly(graph, filename, node_labels=None, node_sizes=None, node_colors=None, edge_weights=None, layout="spring", node_scale=1, title="", auto_open=True, save_type="html"):
    '''
    # The code is mainly contributed by roholazandie.
    # The github link is: https://github.com/roholazandie/graph_drawing/blob/master/plotly_visualize.py
    #
    # Code is modified by EndlessLethe for further use.

    Args: 
        node_labels: List. 
        node_sizes: List.
        node_colors: List of number or str. If not seted, use node_sizes as their colors to specify different nodes.
            Example:
                colors = get_colors(2) # or ["green", "red"]
                node_colors = ["rgba"+str(colors[x]) for x in labels]
        edge_weights: Dict
        node_scale: Float. When node_sizes is None, node_scale will be used control the scale of nodes.
        save_type:
            If want to save as png, packages "plotly-orca" is needed.
            Run "conda install -c plotly plotly-orca" to install.

    Returns: 
	
    Details:
        Doc: https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html

    Usage: 
	
    '''
    if not isinstance(graph, nx.Graph):
        raise Exception("Graph type must be nx.Graph.")

    logging.debug("Start plotting.")
    positions = get_node_pos_2d(graph, layout)

    Xe = []
    Ye = []
    Xn = []
    Yn = []

    logging.debug("Pos computed.")

    edges = list(graph.edges())
    for edge in edges:
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        Xe += [x0, x1, None]
        Ye += [y0, y1, None]

    weights = 1
    if edge_weights is not None:
        weights = [edge_weights[edges[i]] for i in range(len(edges))]

    edge_trace = Scatter(
        x=Xe,
        y=Ye,
        line=Line(width=edge_weights, color='rgba(136, 136, 136, .8)'),
        hoverinfo='none',
        mode='lines')

    logging.debug("Edge computed.")

    node_list = list(graph.nodes())
    for node in node_list:
        x, y = positions[node]
        Xn.append(x)
        Yn.append(y)

    if node_labels is None:
        node_labels = node_list

    if node_sizes is None:
        node_sizes = []
        for node in node_list:
            node_sizes.append(math.log(len(list(graph.neighbors(node))))*node_scale)

    if node_colors is None:
        node_colors = node_sizes

    node_trace = Scatter(
        x=Xn,
        y=Yn,
        text=node_labels,
        mode='markers+text',
        textfont=dict(family='Calibri (Body)', size=15, color='black'),
        opacity=0.8,
        hoverinfo = "skip",
        marker=Marker(
            showscale= True if isinstance(node_colors[0], int) else False, # if color is int rather than rgba string.
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='Jet',
            color=node_colors,
            size=node_sizes,
            colorbar=dict(
                thickness=15,
                # title='Node Connections',
                xanchor='left',
                titleside='right'
            ) if isinstance(node_colors[0], int) else None,
            line=dict(width=1)))
    logging.debug("Node computed.")

    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(
                     title=title,
                     titlefont=dict(size=16),
                     showlegend=False,
                     width=1500,
                     height=800,
                     hovermode='closest', # where to show annotations
                    #  margin=dict(b=20, l=350, r=5, t=200),
                     # family='Courier New, monospace', size=18, color='#7f7f7f',
                     annotations=[dict(
                         text="",
                         showarrow=False,
                         xref="paper", yref="paper",
                         x=0.005, y=-0.002)],
                     xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False), # disable axis
                     yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)
                     ))

    if save_type == "html":
        offpy(fig, filename=filename, auto_open=auto_open, show_link=False)
    else:
        fig.write_image(filename+"."+save_type)
    logging.debug("Fig computed.")


def plot_3dgraph_plotly(graph, filepath, node_labels = None, node_sizes = None, title="3D_visualization", node_scale=1):
    # The code is mainly contributed by roholazandie.
    # The github link is: https://github.com/roholazandie/graph_drawing/blob/master/plotly_visualize.py
    #
    # Code is partly modified by EndlessLethe for further use.

    if not isinstance(graph, nx.Graph):
        raise Exception("Graph type must be nx.Graph.")

    Xe = []
    Ye = []
    Ze = []
    Xn = []
    Yn = []
    Zn = []

    # positions = nx.fruchterman_reingold_layout(graph, dim=3, iterations=50)
    positions = get_node_pos_3d(graph, filepath, "sfdp")
    logging.debug("Pos computed.")

    for edge in graph.edges():
        x0, y0, z0 = positions[edge[0]]
        x1, y1, z1 = positions[edge[1]]
        Xe += [x0, x1, None]
        Ye += [y0, y1, None]
        Ze += [z0, z1, None]

    edge_trace = Scatter3d(x=Xe,
                           y=Ye,
                           z=Ze,
                           mode='lines',
                           line=Line(color='rgba(136, 136, 136, 1)', width=1),
                           hoverinfo='none',
                           opacity=0.2
                           )

    logging.debug("Edge computed.")

    node_list = list(graph.nodes())
    for node in node_list:
        x, y, z = positions[node]
        Xn.append(x)
        Yn.append(y)
        Zn.append(z)

    if node_labels is None:
        node_labels = node_list

    if node_sizes is None:
        node_sizes = []
        for node in node_list:
            node_sizes.append(math.log(len(list(graph.neighbors(node))))*node_scale)
    

    node_trace = Scatter3d(x=Xn,
                           y=Yn,
                           z=Zn,
                           mode='markers',
                           hoverinfo = "text",
                           marker=Marker(
                                showscale=True,
                                size=node_sizes,
                                color=node_sizes,
                                colorscale='Jet', 
                                colorbar=dict(
                                    thickness=15,
                                    title='Node Connections',
                                    xanchor='left',
                                    titleside='right'
                                ),
                                line=Line(color='rgb(50,50,50)', width=0.5)
                                ),
                           text=node_labels,
                           )

    logging.debug("Node computed.")

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

    layout = Layout(
        title=title,
        width=1000,
        height=1000,
        showlegend=False,
        scene=Scene(
            xaxis=XAxis(axis),
            yaxis=YAxis(axis),
            zaxis=ZAxis(axis),
        ),
        margin=Margin(
            t=100
        ),
        hovermode='closest',
        annotations=Annotations([
            Annotation(
                showarrow=False,
                text="",
                xref='paper',
                yref='paper',
                x=0,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                font=Font(
                    size=14
                )
            )
        ]), )

    data = [node_trace, edge_trace]
    fig = Figure(data=data, layout=layout)

    logging.debug("Fig computed.")

    offpy(fig, filename=filepath, auto_open=True, show_link=False)
    logging.debug("output into: " + filepath)


def get_node_pos_2d(graph, layout):
    '''
    this method provide positions based on layout algorithm

    # The code is mainly contributed by roholazandie.
    # The github link is: https://github.com/roholazandie/graph_drawing/blob/master/plotly_visualize.py
    #
    # Code is partly modified by EndlessLethe for further use.
    '''
    pos = LAYOUT[layout](graph, **LAYOUT_ARGS.get(layout, dict()))
    return pos

def get_node_pos_3d(graph, filepath, prog='neato', root=None, args=''):
    """Create node positions for graph using Graphviz.

    # The code is mainly contributed by roholazandie.
    # The github link is: https://github.com/roholazandie/graph_drawing/blob/master/plotly_visualize.py
    #
    # Code is partly modified by EndlessLethe for further use.

    Parameters
    ----------
    graph : NetworkX graph
      A graph created with NetworkX
    prog : string
      Name of Graphviz layout program
    root : string, optional
      Root node for twopi layout
    args : string, optional
      Extra arguments to Graphviz layout program

    Returns : dictionary
      Dictionary of x, y, positions keyed by node.

    Examples
    --------
    graph = nx.petersen_graph()
    pos = nx.nx_agraph.graphviz_layout(graph)
    pos = nx.nx_agraph.graphviz_layout(graph, prog='dot')

    """
    try:
        import pygraphviz
    except ImportError:
        raise ImportError('requires pygraphviz ',
                          'http://pygraphviz.github.io/')
    if root is not None:
        args += "-Groot=%s" % root

    ag = nx.nx_agraph.to_agraph(graph)
    ag.graph_attr["dimen"] = "3"

    ag.layout(prog=prog, args=args)
    node_pos = {}

    for n in graph:
        node = pygraphviz.Node(ag, n)
        try:
            xx, yy, zz = node.attr["pos"].split(',')
            node_pos[n] = (float(xx), float(yy), float(zz))
        except:
            logging.debug("No position for node", n)
            node_pos[n] = (0.0, 0.0, 0.0)

    return node_pos

def plot_tripartite_graph(tri_tuples, a_ids, m_ids, c_ids, highlight_ids = None):
    '''
    plot for tri-partitate graph.

    Args:
        highlight_ids: dict. key - value is like (color, ids)

    Note: 
        id of a, m and c must be unique.
        triples must be (u, v, w), donated one edge from u to v. 
    '''

    a_ids = set(a_ids)
    m_ids = set(m_ids)
    c_ids = set(c_ids)

    BLUE = '#A0CBE2'
    INF = 999999999
    G = nx.Graph()
    dict_in = dict()
    dict_out = dict()
 
    # compute statistics value
    for u, v, w in tri_tuples:
        G.add_edge(u, v, weight = w)
        dict_out[u] = dict_out.get(u, 0) + w
        dict_in[v] = dict_in.get(v, 0) + w

    # node colors
    node_colors = [BLUE] * G.number_of_nodes()
    if highlight_ids is not None:
        import numpy as np
        node_ids = list(G.nodes())
        ids_map = dict((x, i) for i, x in enumerate(node_ids))
        for color, ids in highlight_ids.items():
            for idx in ids:
                node_colors[ids_map[idx]] = color

    # node positions
    components = [list(G.subgraph(c).nodes()) for i, c in enumerate(nx.connected_components(G))]
    node_list = [i for p in components for i in p]

    idx1 = [a for a in node_list if a in a_ids]
    idx2 = [m for m in node_list if m in m_ids]
    idx3 = [c for c in node_list if c in c_ids]

    pos = dict()
    max_size = max(len(idx1), len(idx2), len(idx3))
    pos.update((n, (0, i*3.0*max_size / len(idx1))) for i, n in enumerate(idx1))
    pos.update((n, (1, i*3.0*max_size / len(idx2))) for i, n in enumerate(idx2))
    pos.update((n, (2, i*3.0*max_size / len(idx3))) for i, n in enumerate(idx3))

    options = {'node_color':node_colors, 'node_size':500, 'width':0.5, 'pos':pos, 'with_labels':True, 'edge_color':BLUE}
    edge_labels = nx.get_edge_attributes(G, 'weight')
    
    # node labels
    node_labels = dict((x, x) for x in G.nodes())
    for m in idx2:
        node_labels[m] = "%s\nin_%d_out_%d_abs(in-out)_%d" % (node_labels[m], dict_in[m], 
                                dict_out[m], abs(dict_in[m]-dict_out[m]))
    for a in idx1:
        node_labels[a] = "%s\nout_%d" % (node_labels[a], dict_out[a])
    for c in idx3:
        node_labels[c] = "%s\nin_%d" % (node_labels[c], dict_in[c])

    plt.figure(figsize=(10, 8))
    nx.draw(G, labels = node_labels, **options)
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    plt.show()