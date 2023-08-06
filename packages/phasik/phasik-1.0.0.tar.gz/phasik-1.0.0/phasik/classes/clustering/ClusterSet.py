"""
Base class for a cluster set of temporal network snapshots
"""

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import scipy.cluster.hierarchy as sch
import seaborn as sb
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import KMeans

from phasik.classes import DistanceMatrix
from phasik.drawing.drawing_clusters import plot_cluster_set, plot_dendrogram

__all__ = ['ClusterSet']


class ClusterSet :

    def __init__(self, clusters, times, linkage, distance_matrix, distance_metric,
                 cluster_method, n_clusters_max, n_max_type) :

        self._clusters = clusters
        self._times = times
        self.n_clusters = len(set(clusters))
        self._cluster_method = cluster_method
        self._n_max = n_clusters_max
        self._n_max_type = n_max_type
        self._distance_metric = distance_metric
        try :
            self.silhouette_average = silhouette_score(distance_matrix.distance_matrix, clusters, metric='precomputed')
            self.silhouette_samples = silhouette_samples(distance_matrix.distance_matrix, clusters, metric='precomputed')
        except ValueError as error :
            # Often the number of clusters is 1, which sklearn does not like.
            print(f'WARNING: unable to compute silhouette for cluster set. Error is: {error}')
            self.silhouette_average = 0
            self.silhouette_samples = np.array([])
        self.linkage = linkage

    @property
    def clusters(self):
        return self._clusters

    @clusters.setter
    def clusters(self, arr) :
        self._clusters = arr

    @property
    def times(self) :
        return self._times

    @property
    def cluster_method(self) :
        return self._cluster_method

    @property
    def n_max_type(self) :
        return self._n_max_type

    @property
    def n_max(self) :
        return self._n_max

    @property
    def distance_metric(self) :
        return self._distance_metric

    @classmethod
    def from_distance_matrix(cls, distance_matrix, n_max_type, n_clusters_max, cluster_method) :

        times = distance_matrix.times
        distance_metric = distance_matrix.distance_metric

        if cluster_method=='k_means' :
            # k-means clustering is only applicable for n_max_type of 'maxclust'
            if n_max_type != 'maxclust' :
                raise ValueError(f"With {cluster_method}, the n_max_type must be 'maxclust'.")

            k_means = KMeans(n_clusters=n_clusters_max, random_state=None)
            clusters = k_means.fit_predict(distance_matrix.snapshots_flat) + 1
            linkage = None

        else : # hierarchical clustering TODO specify allowed methods
            # From scipy's documentation:
            # "Methods ‘centroid’, ‘median’, and ‘ward’ are correctly defined
            # only if Euclidean pairwise metric is used. If 'y' is passed as precomputed pairwise distances,
            # then it is the user’s responsibility to assure that these distances are in fact Euclidean,
            # otherwise the produced result will be incorrect."
            if cluster_method in ['ward', 'centroid', 'median'] :
                if distance_metric!='euclidean' :
                    raise ValueError(f"With {cluster_method}-linkage, the distance metric must be 'euclidean'.")

            # if len(distance_matrix.distance_matrix_flat) > 0 : # TODO check what it checks
            linkage = sch.linkage(distance_matrix.distance_matrix_flat, method=cluster_method)
            clusters = sch.fcluster(linkage, n_clusters_max, criterion=n_max_type)

        return cls(clusters, times, linkage, distance_matrix, distance_metric, cluster_method, n_clusters_max, n_max_type)

    @classmethod
    def from_temporal_network(cls, temporal_network, distance_metric,
                              cluster_method, n_max_type, n_clusters_max) :

        distance_matrix = SnapshotsDistanceMatrix.from_temporal_network(temporal_network, distance_metric)

        return cls.from_distance_matrix(distance_matrix, n_max_type, n_clusters_max, cluster_method)
            
    def distance_threshold(self):
        """Calculate the distance at which clustering stops
        
        Parameters
        ----------
        None
        
        Returns
        -------
        int 
            Smallest number d such that the distance between any two clusters is < d.
        """
        
        if self.linkage is None :
            raise ValueError('Cannot compute the threshold of a non-hierarchical clustering')
            
        number_of_observations = self.linkage.shape[0] + 1
        if self.n_clusters >= number_of_observations:
            return 0
        elif self.n_clusters <= 1:
            return self.linkage[-1, 2] * 1.001
        else:
            return self.linkage[-self.n_clusters, 2] * 1.001     
            
    def plot_dendrogram(self, ax=None, distance_threshold=None, leaf_rotation=90, leaf_font_size=6):
        """Plot this cluster set as a dendrogram

        Parameters
        ----------
        ax : matplotlib.Axes, optional
            Axes on which to plot 
        leaf_rotation : int or float, optional
            Rotation to apply to the x-axis (leaf) labels (default 90)
        leaf_font_size : int or str, optional
            Desired size of the x-axis (leaf) labels (default 6)
            
        Returns
        -------
        None
    """ 
    
        return plot_dendrogram(self, ax, distance_threshold, leaf_rotation, leaf_font_size)   

    def plot(self, ax=None, y_height=0, cmap=cm.get_cmap('tab10'), number_of_colors=10, colors=None) :
        """Plots this cluster set as a scatter graph

        Parameters
        ----------
        ax : matplotlib.Axes, optional
            Axes on which to plot
        y_height : int or float, optional
            Height at which to plot (default 0)
        cmap : matplotlib.cm, optional
            Desired colour map (default 'tab10')
        number_of_colors : int, optional
            Desired number of colours to use for the colormap (default 10)
        colors :

        Returns
        -------
        None
        """

        return plot_cluster_set(self, ax, y_height, cmap, number_of_colors, colors)
        
    def plot_silhouette_samples(self, ax=None):
        """Plot the silhouette samples from this cluster set

        Parameters
        ----------
        ax : matplotlib.Axes, optional
            Axes on which to plot 
            
        Returns
        -------
        None
        """

        if ax is None:
            ax = plt.gca()

        # If there are more than 10 clusters in this cluster set, we'll need to use more colours in our plot.
#        sb.set_palette("tab20" if self.size > 10 else "tab10")
        # replace by single colour palette with 20 colours such that first 10 colours are same as tab10
        pal = sb.color_palette('tab20', n_colors=20)
        pal2_arr = np.append(pal[::2], pal[1::2], axis=0)
        pal2 = sb.color_palette(pal2_arr)
        sb.set_palette(pal2)
        
        if self.silhouette_samples.size > 0:
            y_lower = 0
            for i, cluster in enumerate(np.unique(self.clusters)):
                # Aggregate the silhouette scores for samples belonging to each cluster, and sort them
                silhouette_values = self.silhouette_samples[self.clusters == cluster]
                silhouette_values.sort()
                silhouette_size = silhouette_values.shape[0]

                # Calculate height of this cluster
                y_upper = y_lower + silhouette_size
                y = np.arange(y_lower, y_upper)
                ax.fill_betweenx(y, 0, silhouette_values, facecolor=f"C{i}", edgecolor=f"C{i}", alpha=1)

                # Compute the new y_lower for next cluster
                vertical_padding = 0
                y_lower = y_upper + vertical_padding

        ax.axvline(x=self.silhouette_average, c='k', ls='--')        
