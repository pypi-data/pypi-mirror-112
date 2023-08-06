'''

Author: Zeng Siwei
Date: 2021-07-01 16:57:49
LastEditors: Zeng Siwei
LastEditTime: 2021-07-02 17:32:02
Description: 

'''


import matplotlib.pyplot as plt
import numpy as np

# import functools
# PLOTDEFAULT_OPTIONS = (
#     'filepath',
#     'xscale',
#     'yscale',
#     'xlabel',
#     'ylabel',

# )
# def plotdefault_wrapper(func):
#     '''
#     Functions in plot utils must have the following argument format:
#         data_args, ..., filepath, plot_options
#     '''
#     @functools.wraps(func)
#     def wrapper_plotdefault(*args, **kwargs):
#         plotdefault_options = {k: v for k, v in kwargs.items() if k in PLOTDEFAULT_OPTIONS}
#         kwargs = {k: v for k, v in kwargs.items() if k not in PLOTDEFAULT_OPTIONS}
#         func(*args, **kwargs)
        
#         xscale = plotdefault_options.get('xscale', 'linear')
#         yscale = plotdefault_options.get('yscale', 'linear')
#         xlabel = plotdefault_options.get
#         plt.xscale(xscale)
#         plt.yscale(yscale)
#         plt.xlabel("log_" if "log" in xscale else "" + xlabel)
#         plt.ylabel("log_" if "log" in yscale else "" + ylabel)
#         plt.title(title)

#         if filepath is not None:
#             plt.savefig(filepath)
#             plt.close()
#         else :
#             plt.show()


def get_colors(num, colormap = "rainbow"):
    '''
    Common used colormaps: "gist_rainbow", "rainbow", "spring", "summer", "YlGn"
                            "winter", "binary", "viridis"

    Returns:
        A list of tuples RGBA.

    More details:
        https://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html

    Usage:
        colors = get_colors(np.max(labels)+1, "viridis")
        node_colors = [colors[x] for x in labels]
    '''
    colormap = getattr(plt.cm, colormap)
    colors = [colormap(i) for i in np.linspace(0, 1, num)]
    return colors

def number2color(values, cmap):
    '''

    Args: 
	
    Returns: 
	
    Usage: 
        colors = number2color(y, "RdBu")
    '''
    norm = matplotlib.colors.Normalize(vmin=np.min(values), vmax=np.max(values))
    cmap = matplotlib.cm.get_cmap(cmap)
    return [cmap(norm(val)) for val in values]

