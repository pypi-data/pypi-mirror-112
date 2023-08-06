'''

Author: Zeng Siwei
Date: 2020-12-28 16:50:54
LastEditors: Zeng Siwei
LastEditTime: 2020-12-28 17:06:55
Description: 

'''
import numpy as np

def network_warpper(full_fn_name, *args, **kwargs):
    '''
    All optional functions listed in: https://networkx.org/documentation/stable/reference/generators.html

    Args: 
        full_fn_name: Full path like "networkx.generators.classic.complete_graph"
        
    Returns: 
        list_src
        list_dst
        
    Usage: 
        list_src, list_dst = network_warpper("networkx.generators.classic.complete_graph", 3)
        
    '''
    from .utils import load_function_by_reflection
    nx_fn = load_function_by_reflection(full_fn_name)
    nx_g = nx_fn(*args, **kwargs)

    list_src, list_dst = [], []
    for u, v in nx_g.edges():
        list_src.add(u)
        list_dst.add(v)
    return list_src, list_dst


def generate_dense_graph(n, p, given_node_ids = None, directed=False, random_seed=None, shuffle=False):
    """
    Generate a dense graph with n nodes.

    Args:
        n: number of nodes
        p: the probability of choosing a edge.
        given_node_ids: the generated node IDs
    """
    

    if random_seed is not None:
        rng = np.random.RandomState(random_seed)
    else:
        rng = np.random.default_rng()

    list_src = []
    list_dst = []
    # dict_node = dict((x, x) for x in range(n))
    dict_node = dict()

    if given_node_ids is not None:
        if len(given_node_ids) != n:
            raise ValueError("length of given_node_ids must be equal to input arg n")
    else:
        given_node_ids = list(range(n))

    if shuffle:
        rng.shuffle(given_node_ids)

    for i in range(n):
        dict_node[i] = given_node_ids[i]
    

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if (directed is not True) and i > j:
                continue
            if rng.uniform() < p:
                list_src.append(dict_node[i])
                list_dst.append(dict_node[j])
    if not directed:
        list_src_tmp = list_src + list_dst
        list_dst_tmp = list_dst + list_src
        list_src = list_src_tmp
        list_dst = list_dst_tmp
    return list_src, list_dst


def generate_bipartite_graph(src, dst, p=1, directed=False, random_seed=None):
    """
    Generate a bipartite graph.

    Note: 
        Make sure that src and dst don't overlap.
    """

    if random_seed is not None:
        rng = np.random.RandomState(random_seed)
    else:
        rng = np.random.default_rng()

    list_src = []
    list_dst = []
    
    for i in src:
        for j in dst:
            if rng.uniform() < p:
                list_src.append(i)
                list_dst.append(j)
    if not directed:
        list_src_tmp = list_src + list_dst
        list_dst_tmp = list_dst + list_src
        list_src = list_src_tmp
        list_dst = list_dst_tmp
    return list_src, list_dst


def generate_hyperbolic_graph(n, frac=10, p=1, random_seed=None):
    """
    Generate a hyperbolic graph.

    Note: 
        Make sure that src and dst don't overlap.
    """
    if random_seed is not None:
        rng = np.random.RandomState(random_seed)
    else:
        rng = np.random.default_rng()

    list_src = []
    list_dst = []
    
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i >= j:
                continue
            
            x = 1.0 * i / n
            y = 1.0 * j / n
            if y < 1.0 / (frac * x) and rng.uniform() <= p:
                list_src.append(i)
                list_dst.append(j)


    list_src_tmp = list_src + list_dst
    list_dst_tmp = list_dst + list_src
    list_src = list_src_tmp
    list_dst = list_dst_tmp
    return list_src, list_dst

def inject_block(g, list_src, list_dst, replace=False):
    '''

    Args: 
	
    Returns: 
	
    Usage: 
        args.inject_ids = np.random.choice(g.number_of_nodes(), size=args.inject_size, replace=False)
        # given_node_ids = list(range(input_n_nodes, input_n_nodes+args.inject_size))
        list_src, list_dst = generate_dense_graph(args.inject_size, args.inject_p, args.inject_ids)
        g = inject_block(g, list_src, list_dst, replace=True)
    '''

    if replace:
        g_new = g
    else:
        import copy
        src, dst = g.edges()
        src, dst = src.clone(), dst.clone()
        g_new = dgl.graph((src, dst))

    n_nodes = g_new.number_of_nodes()
    g_new.add_edges(list_src, list_dst)
    return g_new


if __name__ == "__main__":
    from graph_plot_utils import plot_spy
    from graph_utils import edges2df, Edges, edges2g, edges2csr

    # list_src, list_dst = network_warpper("networkx.generators.classic.complete_graph", 3)
    # list_src, list_dst = generate_hyperbolic_graph(10)
    list_src, list_dst = generate_hyperbolic_graph(1000, 20, 0.5)
    edges = Edges(list_src, list_dst) 
    df = edges2df(edges)
    g = edges2g(edges, g_type="networkx")
    # plot_graph(g, layout='spring')
    csr_plot = edges2csr(edges)
    plot_spy(csr_plot, highlight_node=list(range(100)))
    edges.save("./input/hyperbolic_1000.txt")
