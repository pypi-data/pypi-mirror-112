'''

Author: Zeng Siwei
Date: 2020-09-16 19:08:44
LastEditors: Zeng Siwei
LastEditTime: 2021-07-13 00:21:49
Description: 

'''

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import seaborn

from ..utils import get_value_ratio_by_labels
from .basic_plot_utils import number2color, get_colors
from .graph_plot_utils import plot_graph, plot_spy, plot_graph_plotly, plot_3dgraph_plotly
from .matrix_vis_utils import plot_tsne
from .plot_heatmap import plot_heatmap

def plot_data(x_object, filepath=None, sort=False, labels=None, 
                scale_type='linear', xlabel="index", 
                ylabel="value", title="scatter_plot", **plot_options):
    '''
    plot data value for continous or discrete data (with optional labels).

    Args: 
        scale_type: The axis scale type to apply.
                    value : {"linear", "log", "symlog", "logit", ...}
	
    Returns: 
	
    More Details:
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html


    '''
    options = dict(marker="o", alpha=0.3, c="red", s=None)
    
    if isinstance(scale_type, tuple):
        xscale = scale_type[0]
        yscale = scale_type[1]
    else:
        xscale = yscale = scale_type

    if sort is True:
        x_object = np.sort(x_object)

    # use label to color nodes
    if labels is not None:
        color_types = get_colors(np.max(labels)+1, "jet")
        options['c'] = [color_types[x] for x in labels]

    options.update(plot_options)

    index = range(1, len(x_object)+1)
    plt.scatter(index, x_object, **options)

    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.xlabel("log_" if "log" in xscale else "" + xlabel)
    plt.ylabel("log_" if "log" in yscale else "" + ylabel)
    plt.title(title)

    if filepath is not None:
        plt.savefig(filepath)
        plt.close()
    else :
        plt.show()


def plot_dist(x_object, filepath=None, labels=None, scale_type='linear', xlabel="value", 
                ylabel="count", title="dist_plot", **plot_options):
    '''
    plot frequency distribution for discrete data (with optional labels).

    Args: 
        scale_type: The axis scale type to apply.
            value : {"linear", "log", "symlog", "logit", ...}

    Returns: 
	
    More details:
        https://matplotlib.org/3.1.3/api/_as_gen/matplotlib.pyplot.xscale.html

    Usage: 
	
    '''

    options = dict(marker="o", alpha=0.3, c="red", s=None, cmap=None)
    options.update(plot_options)

    if isinstance(scale_type, tuple):
        xscale = scale_type[0]
        yscale = scale_type[1]
    else:
        xscale = yscale = scale_type

    from collections import Counter
    dict_count = Counter(x_object) 
    X = list(dict_count.keys())  # numbers of triangles
    Y = list(dict_count.values()) # count

    if labels is not None:
        if np.max(labels) > 1:
            raise ValueError("Labels must be 0 or 1 (True or False).")

        colors = []
        dict_value_ratio = get_value_ratio_by_labels(x_object, labels)
        # get ratio for label False
        # because the cmap 'viridis': the smaller value, the darker color
        for x in X:
            colors.append(dict_value_ratio[x][0]) 
        options['c'] = colors
        if options.get('cmap', None) is None:
            options['cmap'] = "viridis" 

    plt.scatter(X, Y, **options)
    if options.get('cmap', None) is not None:
        plt.colorbar()
    
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.xlabel("log_" if "log" in xscale else "" + xlabel)
    plt.ylabel("log_" if "log" in yscale else "" + ylabel)
    plt.title(title)

    if filepath is not None:
        plt.savefig(filepath)
        plt.close()
    else :
        plt.show()
    

def plot_hist(x_object, filepath=None, colors=None, xlabel="value", 
                ylabel="count", title="hist_plot", **plot_options):
    '''
    Plot

    Args:
        x_object: A series of data point, not counter.
                    list "[1.1, 2.1, ...]" or dict "{0:list_data1, 1:list_data2}".
        colors: The same format as x_object. Use given colors to plot.
                list of colors "['r', 'b', ...]" or Dict "{0:color1, 1:color2}". 
                    
    Usage:
        plot_hist({0:list_20, 1:list_100}, "./gene.png", colors={0:'red', 1:'blue'})

    More details: 
        https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist.html
        https://seaborn.pydata.org/generated/seaborn.histplot.html#seaborn.histplot
    '''

    options = dict(stat="count", kde=True, bins=20, binrange=None)
    options.update(plot_options)
   
    if isinstance(x_object, (tuple, list, np.ndarray)):
        seaborn.histplot(x_object, **options)
    elif isinstance(x_object, dict):  # dict of list. plot #key subfig.
        if colors is None:
            colors = get_colors(len(x_object))
            colors = dict((key, colors[i]) for i, key in enumerate(x_object.keys()))

        plt.figure(figsize=(16, 10))
        for key, x in x_object.items():
            seaborn.histplot(x, label=key, color=colors[key], **options)
        plt.legend(loc = 0)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
    if filepath is not None:
        plt.savefig(filepath)
        plt.close()
    else :
        plt.show()


def plot_join(xs, ys, filepath=None, scale_type='linear', color_scale='linear',
                gridnum=200, kind="default", title='Rectangle binning points',
                xlabel='X', ylabel='Y', with_margin=False):
    xs = np.array(xs) 
    ys = np.array(ys) 

    if isinstance(gridnum, tuple):
        xgridnum = gridnum[0]
        ygridnum = gridnum[1]
    else:
        xgridnum = ygridnum = gridnum

    if isinstance(scale_type, tuple):
        xscale = scale_type[0]
        yscale = scale_type[1]
    else:
        xscale = yscale = scale_type

    if xscale == 'log' and min(xs) <= 0:
        print('[Warning] logscale with nonpositive values in x coord')
        print('\tremove {} nonpositives'.format(len(np.argwhere(xs <= 0))))
        xg0 = xs > 0
        xs = xs[xg0]
        ys = ys[xg0]
    if yscale == 'log' and min(ys) <= 0:
        print('[Warning] logscale with nonpositive values in y coord')
        print('\tremove {} nonpositives'.format(len(np.argwhere(ys <= 0))))
        yg0 = ys > 0
        xs = xs[yg0]
        ys = ys[yg0]


    

    # color scale
    cnorm = matplotlib.colors.LogNorm() if color_scale == "log" else matplotlib.colors.Normalize()

    fig = plt.figure()
    if with_margin:
        gs = matplotlib.gridspec.GridSpec(4, 4)
        ax_joint = fig.add_subplot(gs[1:4, 0:3])
        ax_marg_x = fig.add_subplot(gs[0, 0:3], sharex=ax_joint)
        ax_marg_y = fig.add_subplot(gs[1:4, 3], sharey=ax_joint)
        plt.sca(ax_joint)

    # plot
    if kind == "default":
        if xscale == 'log':
            xlogmax = np.ceil(np.log10(max(xs)))
            xgridsize = np.logspace(0, xlogmax, xgridnum)
        else:
            xmax = np.ceil(max(xs))
            xgridsize = np.linspace(0, xmax, xgridnum)

        if yscale == 'log':
            ylogmax = np.ceil(np.log10(max(ys)))
            ygridsize = np.logspace(0, ylogmax, ygridnum)
        else:
            ymax = np.ceil(max(ys))
            ygridsize = np.linspace(0, ymax, ygridnum)
        plt.hist2d(xs, ys, bins=(xgridsize, ygridsize), cmin=1, norm=cnorm, cmap=plt.cm.jet)
    elif kind == "hex":
        plt.hexbin(xs, ys, gridsize=gridnum, xscale=xscale, yscale=yscale, mincnt=1, norm=cnorm, cmap=plt.cm.jet)

    # set axis label, etc.
    if with_margin:
        _, cbins = np.histogram(np.log10(xs) if xscale == "log" else xs, bins='auto')
        _, imcbins = np.histogram(np.log10(ys) if yscale == "log" else ys, bins='auto')

        ax_marg_x.hist(xs, bins=10*cbins, histtype='bar', density=True, facecolor='blue', alpha=0.75)
        ax_marg_y.hist(ys, orientation="horizontal", bins=10*imcbins, density=True, histtype='bar', facecolor='red', alpha=0.75)
        ax_marg_x.set_yscale(xscale)
        ax_marg_y.set_yscale(yscale)

        def simpleaxis(ax):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        simpleaxis(ax_marg_x)
        simpleaxis(ax_marg_y)

        # Turn off tick labels on marginals
        plt.setp(ax_marg_x.get_xticklabels(), visible=False)
        plt.setp(ax_marg_y.get_yticklabels(), visible=False)

        ax_joint.set_xscale(xscale)
        ax_joint.set_yscale(yscale)

        font2 = {'family': 'Times New Roman',
                'weight': 'normal',
                'size': 20,
                }
        ax_joint.tick_params(axis='both', which='major', labelsize=15)
        ax_marg_x.tick_params(axis='both', which='major', labelsize=15)
        ax_marg_y.tick_params(axis='both', which='major', labelsize=15)

        # Set labels on joint
        ax_joint.set_xlabel(xlabel, font2)
        ax_joint.set_ylabel(ylabel, font2)

        plt.tight_layout()

    else:
        cb = plt.colorbar()
        if color_scale == 'log':
            cb.set_label('log10(N)')
        else:
            cb.set_label('counts')

        plt.xscale(xscale)
        plt.yscale(yscale)

        plt.xlabel("log_" if "log" in xscale else "" + xlabel)
        plt.ylabel("log_" if "log" in yscale else "" + ylabel)
        plt.title(title)


    if filepath is not None:
        plt.savefig(filepath)
        plt.close()
    else:
        plt.show()