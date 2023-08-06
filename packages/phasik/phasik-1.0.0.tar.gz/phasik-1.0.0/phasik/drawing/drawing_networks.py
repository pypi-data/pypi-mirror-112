"""
Functions to visualise networks and temporal networks
"""

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

__all__ = [
    'standard_node_params',
    'standard_edge_params',
    'standard_label_params',
    'standard_params',    
    'draw_graph',
    'highlight_subgraphs',
]    

def standard_params(color):
    return {
        'node_color': color,
        'edge_color': color,
        'font_color': 'k',
        'font_size' : 'medium',
        'edgecolors': 'k',
        'node_size': 100,
        'bbox': dict(facecolor=color, edgecolor='black', boxstyle='round, pad=0.2', alpha=1)
    }        
    
    
def standard_node_params(color):
    return {
        'node_color': color,
        'edgecolors': 'k',
        'node_size': 100
    }      
    
    
def standard_edge_params(color):
    return {
        'edge_color': color,
    }    
    
    
def standard_label_params(color):
    return {
        'font_color': 'k',
        'font_size' : 'medium',
        'bbox': dict(facecolor=color, edgecolor='black', boxstyle='round, pad=0.2', alpha=1)
    }              


def draw_graph(graph, ax=None, label_nodes=True, color='mediumseagreen'):
    """Basic graph drawing function

    Parameters
    ----------
    graph : networkx.Graph 
        
    ax : matplotlib.Axes, optional
        Axes on which to draw the graph
    label_nodes : bool, optional 
        Whether to label the nodes or just leave them as small circles (default True)
    color : str, optional
        Color to use for the graph nodes and edges (default mediumseagreen)
        
    Returns
    -------
    None
    """

    if ax is None:
        ax = plt.gca()

    layout = graphviz_layout(graph, prog='neato')
    _draw_graph(graph, layout, ax, label_nodes, color)


def _draw_graph(graph, layout, ax, label_nodes, color):
    # PRIVATE function for the parts of graph drawing that are common to multiple methods
    params_nodes = standard_node_params(color)
    params_edges = standard_edge_params(color)   
    params_labels = standard_label_params(color)     
    nx.draw_networkx_nodes(graph, ax=ax, pos=layout, **params_nodes)
    nx.draw_networkx_edges(graph, ax=ax, pos=layout, **params_edges)
    if label_nodes:
        nx.draw_networkx_labels(graph, ax=ax, pos=layout, **params_labels)


def highlight_subgraphs(graphs, colors, ax=None, label_nodes=True):
    """Draw multiple nested subgraphs on the same axes

    Parameters
    ----------
    graphs : list of networkx.Graph
        
    colors : list of str
        List of colours, one for each of the graphs in 'graphs'
    ax : matplotlib.Axes, optional
        Axes to plot on
    label_nodes : bool, optional 
        Whether or not to label the graph nodes or leave them as circles
        
    Returns
    -------
    None
    """

    if ax is None:
        ax = plt.gca()

    layout = graphviz_layout(graphs[0], prog='neato')
    for graph, color in zip(graphs, colors):
        _draw_graph(graph, layout, ax, label_nodes, color)
        
        
