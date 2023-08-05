"""
Useful functions to draw clusters
"""

import matplotlib.pyplot as plt
import numpy as np

from phasik.utils.clusters import rand_index_over_methods_and_sizes

__all__ = [
    'plot_randindex_bars_over_methods_and_sizes'
]

def plot_randindex_bars_over_methods_and_sizes(valid_cluster_sets, reference_method="ward", ax=None, plot_ref=False):

    "Plot Rand Index as bars, to compare any method to a reference method, for all combinations of methods and number of clusters"""

    if ax is None:
        ax = plt.gca()

    valid_methods = [sets[1] for sets in valid_cluster_sets]
    
    i_ref = valid_methods.index(reference_method)
    clusters_ref = valid_cluster_sets[i_ref][0]

    rand_index = rand_index_over_methods_and_sizes(valid_cluster_sets, reference_method)
    n_sizes, n_methods = rand_index.shape
    
    if not plot_ref :
        n_methods -= 1 
         
    width = 1 # bar width
    width_size = n_methods * width # width of all bars for a given # of clusters
    width_inter_size = 4 * width # width space between two # of clusters

    xlabels = clusters_ref.sizes
    xticks = np.arange(n_sizes) * (width_size + width_inter_size) # the label locations

    for i, method in enumerate(valid_methods): 
              
        heights = rand_index[:, i]
        
        if not plot_ref and i==i_ref: 
            pass
        else : # don't plot i_ref if plot_ref is False
            ax.bar(xticks + i * width - width_size / 2, heights, width, label=method)
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
