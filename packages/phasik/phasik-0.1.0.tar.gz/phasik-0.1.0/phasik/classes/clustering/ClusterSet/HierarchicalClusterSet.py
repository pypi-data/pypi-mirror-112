"""
Base class for HierarchicalClusterSet
"""

import scipy.cluster.hierarchy as sch

from phasik.classes.clustering.ClusterSet import ClusterSet
from phasik.classes.clustering import Silhouette

__all__ = ['HierarchicalClusterSet']

class HierarchicalClusterSet(ClusterSet):
    """Subclass of ClusterSet, to be used for any clusters created by a hierarchical method"""

    def __init__(self, snapshots, cluster_limit_type, cluster_limit):
        """
        See base class for parameter info
        """

        if snapshots.linkage is not None:
            clusters = sch.fcluster(snapshots.linkage, cluster_limit, criterion=cluster_limit_type)
        else:
            clusters = None
        silhouette = Silhouette(snapshots.distance_matrix.full, clusters, metric='precomputed')
        super().__init__(clusters, snapshots, cluster_limit_type, cluster_limit, silhouette)
