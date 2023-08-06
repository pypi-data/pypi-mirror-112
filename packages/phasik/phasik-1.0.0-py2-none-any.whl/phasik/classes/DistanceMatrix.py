"""
Base class for the distance matrix of snapshots
"""

import numpy as np
from sklearn.metrics import pairwise_distances

__all__ = ['DistanceMatrix']


class DistanceMatrix :
    """Base class for matrix of pairwise distance/similarity between snapshots of a temporal network."""

    def __init__(self, snapshots, times, distance_metric) :
        """

        Parameters
        ----------
        snapshots : numpy array
            Array of dim (T, N, N) representing instantaneous adjacency matrices
        times : list of float or int
            Times corresponding to each snapshots
        distance_metric : str
            Distance metric to use to compute the distance between snapshots
        """

        if snapshots.ndim==2 : # snapshots already in vector form
            T, N = snapshots.shape
            snapshots_flat = snapshots
        elif snapshots.ndim==3 :
            T, N, _ = snapshots.shape
            snapshots_flat = snapshots.reshape(T, -1)  # flatten each each snapshot (i.e. adjacency matrix) into a vector
        else :
            raise ValueError('Snapshots has wrong number of dimensions: must be 2 or 3.')

        self._times = times
        self._snapshots = snapshots
        self._snapshots_flat = snapshots_flat
        self._distance_metric = distance_metric
        self._distance_matrix = pairwise_distances(self._snapshots_flat, metric=distance_metric)

        # the distance matrix is symmetric. Create a condensed version
        # by flattening the upper triangular half of the matrix into a vector
        upper_triangular_indices = np.triu_indices(n=T, k=1)
        distance_matrix_condensed = self._distance_matrix[upper_triangular_indices]
        self._distance_matrix_flat = distance_matrix_condensed

    @property
    def snapshots(self) :
        return self._snapshots

    @property
    def snapshots_flat(self) :
        return self._snapshots_flat

    @property
    def distance_metric(self) :
        return self._distance_metric

    @property
    def distance_matrix(self) :
        return self._distance_matrix

    @property
    def times(self) :
        return self._times

    @property
    def distance_matrix_flat(self):
        return self._distance_matrix_flat

    @classmethod
    def from_temporal_network(cls, temporal_network, distance_metric) :
        """

        Parameters
        ----------
        temporal_network : TempNet
            Temporal network from which to compute the distance matrix
        distance_metric : str
            Distance metric to compute the distances between snapshots

        Returns
        -------

        """

        return cls(temporal_network.snapshots, temporal_network.times, distance_metric)
