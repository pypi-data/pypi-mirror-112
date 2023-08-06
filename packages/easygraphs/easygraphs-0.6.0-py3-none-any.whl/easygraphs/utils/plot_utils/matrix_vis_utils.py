
'''

Author: Zeng Siwei
Date: 2021-04-06 11:02:02
LastEditors: Zeng Siwei
LastEditTime: 2021-04-06 11:02:02
Description: 

'''

import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

def plot_tsne(matrix, labels, dir_name = None, title = None):
    '''

    Args: 
	
    Returns: 
	
    Usage: 
	
    '''

    from sklearn.manifold import TSNE

    model = TSNE(n_components=2)
    node_pos = model.fit_transform(matrix)


    color_idx = defaultdict(list)
    for i, label in enumerate(labels):
        color_idx[label].append(i)

    for c, idx in color_idx.items():
        plt.scatter(node_pos[idx, 0], node_pos[idx, 1], label=c)  # c=node_colors)

    plt.legend()
    if not dir_name:
        plt.show()
    else:
        filename = dir_name+"tsne" if title is None else title
        plt.savefig(filename, dpi = 300)
        # plt.clf()
        plt.close()

def plot_heatmap(matrix, title, dir_output=None, row_labels=None, col_labels=None, cbarlabel=""):
    '''

	
    Args: 
        cbarlabel: The title of colorbar.
	
    Returns: 
	
    Usage:
        plot_heatmap(A_true, "A_true", "./log/")

    '''
    matrix = np.array(matrix)

    fig, ax = plt.subplots()
    m, n = matrix.shape

    if m < 20 and row_labels is None:
        row_labels = list(range(m))
    if n < 20 and col_labels is None:
        col_labels = list(range(n))

    im, cbar = heatmap(matrix, row_labels, col_labels, ax=ax,
                    cmap="YlGn", cbarlabel=cbarlabel)
    
    if m < 20 and n < 20:
        texts = annotate_heatmap(im, valfmt="{x:.1f}")

    fig.tight_layout()
    plt.title(title)

    if dir_output:
        plt.savefig(dir_output + title + ".png", dpi = 300)
        # plt.clf()
        plt.close()
    else :
        plt.show()


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Code is borrowed from https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    # ... and label them with the respective list entries.
    if col_labels is not None:
        ax.set_xticks(np.arange(len(col_labels)))
        ax.set_xticklabels(col_labels)
    
    if row_labels is not None:
        ax.set_yticks(np.arange(len(row_labels)))
        ax.set_yticklabels(row_labels)
    

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    # plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
            #  rotation_mode="anchor")
    plt.setp(ax.get_xticklabels(), ha="right")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Code is borrowed from https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """
    import matplotlib
    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


def plot_heatmap(x_vec, y_vec, heatmap, base=10, xlabel=None, ylabel=None, outfn=None):
    n, m = heatmap.shape
    fig = plt.figure(figsize=(8, 6.5), dpi=96)
    plt.pcolormesh(heatmap, cmap='jet', norm=LogNorm(), rasterized=True)
    cb = plt.colorbar()
    for lb in cb.ax.yaxis.get_ticklabels():
        lb.set_family('Times New roman')
        lb.set_size(20)

    ax = fig.gca()
    xticks = ax.get_xticks()
    if xticks[-1] > m:  xticks = xticks[:-1]
    xstep = xticks[1] - xticks[0]
    nw_xtick = []
    for xt in xticks:
        if (xt < m) and (xt % (2*xstep) == 0):
            pws = int(np.log(x_vec[int(xt)]) / np.log(base))
            if pws != 0:
                nw_xtick.append('%dE%d' % (base, pws))
            else:
                nw_xtick.append('1')
        else:
            nw_xtick.append('')

    nw_ytick = []
    for yt in ax.get_yticks():
        if yt < n:
            yval = y_vec[int(yt)]
            if yval < 1e4:
                nw_ytick.append(r'%d' % yval)
            else:
                pws = int(np.log10(yval))
                fv = yval * 1.0 / 10**pws
                nw_ytick.append('%.1fE%d'%(fv, pws))

    if nw_xtick[-1] == '':
        nw_xtick[-1] = '%.2f'%x_vec[-1]
        # nw_xtick[-1] = '%.2f'%np.power(base, x_vec[-1])
    if nw_ytick[-1] == '':
        nw_ytick[-1] = '%d' % int(y_vec[-1])
        # nw_ytick = '%d' % int(np.power(base, y_vec[-1]))

    ax.set_xticklabels(nw_xtick, fontsize=27, family='Times New roman')
    ax.set_yticklabels(nw_ytick, fontsize=27, family='Times New roman')

    if xlabel is not None:
        plt.xlabel(xlabel, linespacing=12, fontsize=32, family='Times New roman')
    if ylabel is not None:
        plt.ylabel(ylabel, linespacing=12, fontsize=32, family='Times New roman')

    # fig.set_size_inches(8, 7.3)
    fig.tight_layout()
    if outfn is not None:
        fig.savefig(outfn)
    return fig

def simpleaxis(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

def drawRectbin_with_marg(xs, ys, outfig=None, xscale='log', yscale='log',
                gridsize=200,
                colorscale=True,
                suptitle='Rectangle binning points',
                xlabel='linear', ylabel='linear'):
    xs = np.array(xs) if type(xs) is list else xs
    ys = np.array(ys) if type(ys) is list else ys

    if xscale == 'log' and min(xs) <= 0:
        print('[Warning] logscale with nonpositive values in x coord')
        print('\tremove {} nonpositives'.format(len(np.argwhere(xs <= 0))))
        xg0 = xs > 0
        xs = xs[xg0]
        ys = ys[xg0]

    if xscale == 'linear' and min(xs) <= 0:
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

    fig = plt.figure()
    gs = GridSpec(4, 4)

    ax_joint = fig.add_subplot(gs[1:4, 0:3])
    ax_marg_x = fig.add_subplot(gs[0, 0:3], sharex=ax_joint)
    ax_marg_y = fig.add_subplot(gs[1:4, 3], sharey=ax_joint)

    # color scale
    cnorm = matplotlib.colors.LogNorm() if colorscale else matplotlib.colors.Normalize()
    suptitle = suptitle + ' with a log color scale' if colorscale else suptitle

    # axis space
    if isinstance(gridsize, tuple):
        xgridsize = gridsize[0]
        ygridsize = gridsize[1]
    else:
        xgridsize = ygridsize = gridsize

    # xlogmax = np.ceil(np.log10(max(xs)))
    # ylogmax = np.ceil(np.log10(max(ys)))
    # xymax = max(xlogmax, ylogmax)
    if xscale == 'log':
        xlogmax = np.ceil(np.log10(max(xs)))
        x_space = np.logspace(0, xlogmax, xgridsize)
        # x_space = np.logspace(0, xymax, xgridsize)
    else:
        x_space = xgridsize
    if yscale == 'log':
        ylogmax = np.ceil(np.log10(max(ys)))
        y_space = np.logspace(0, ylogmax, ygridsize)
        # y_space = np.logspace(0, xymax, xgridsize)
    else:
        y_space = ygridsize

    hist = ax_joint.hist2d(xs, ys, bins=(x_space, y_space), cmin=1, norm=cnorm,
            cmap=plt.cm.jet)

    _, cbins = np.histogram(np.log10(xs), bins='auto')
    _, imcbins = np.histogram(np.log10(ys), bins='auto')

    ax_marg_x.hist(xs, bins=20**cbins, histtype='bar', density=True, facecolor='blue', alpha=0.75)
    ax_marg_y.hist(ys, orientation="horizontal", bins=20**imcbins, density=True, histtype='bar', facecolor='red', alpha=0.75)
    ax_marg_x.set_yscale('log')
    ax_marg_y.set_yscale('log')

    simpleaxis(ax_marg_x)
    simpleaxis(ax_marg_y)

    # c_xs = dict(Counter(xs))
    # c_xs_value = c_xs.values()
    # c_xs_sum = sum(c_xs_value)
    # c_xs_value = np.array(list(c_xs_value)) / c_xs_sum
    # ax_marg_x.bar(np.array(c_xs.keys()), c_xs_value)
    #
    # c_ys = dict(Counter(ys))
    # c_ys_value = c_ys.values()
    # c_ys_sum = sum(c_ys_value)
    # c_ys_value = np.array(list(c_ys_value))  / c_ys_sum
    # ax_marg_x.bar(np.array(c_ys.keys()), c_ys_value, orientation="horizontal")


    # Turn off tick labels on marginals
    plt.setp(ax_marg_x.get_xticklabels(), visible=False)
    plt.setp(ax_marg_y.get_yticklabels(), visible=False)

    ax_joint.set_xscale(xscale)
    ax_joint.set_yscale(yscale)

    # plt.title(suptitle)

    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 20,
             }
    ax_joint.tick_params(axis='both', which='major', labelsize=15)
    ax_marg_x.tick_params(axis='both', which='major', labelsize=15)
    ax_marg_y.tick_params(axis='both', which='major', labelsize=15)

    # # Hide the right and top spines
    # ax_marg_x.spines['right'].set_visible(False)
    # ax_marg_x.spines['top'].set_visible(False)
    # ax_marg_x.yaxis.set_ticks_position('left')
    # ax_marg_x.xaxis.set_ticks_position('bottom')
    #
    # # Hide the right and top spines
    # ax_marg_y.spines['right'].set_visible(False)
    # ax_marg_y.spines['top'].set_visible(False)
    # ax_marg_y.yaxis.set_ticks_position('left')
    # ax_marg_y.xaxis.set_ticks_position('bottom')

    # ax_joint.set_xticklabels(fontsize=15)
    # ax_joint.set_yticklabels(fontsize=15)

    # Set labels on joint
    ax_joint.set_xlabel(xlabel, font2)
    ax_joint.set_ylabel(ylabel, font2)

    plt.tight_layout()

    # cb = plt.colorbar()
    # if colorscale:
    #     cb.set_label('log10(N)',size=15)
    # else:
    #     cb.set_label('counts',size=15)

    if outfig is not None:
        fig.savefig(outfig)
    return fig, hist