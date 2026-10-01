"""Helpers shared by the tests."""

import igraph as ig
import numpy as np


def make_graph(types, edges, directed=False):
    g = ig.Graph(n=len(types), edges=edges, directed=directed)
    g.vs["type"] = types
    return g


def check_levels(coords, types):
    coords, types = np.asarray(coords), np.asarray(types, dtype=bool)
    assert coords.shape[0] == len(types)
    assert (coords[types, 1] >= 0.25).all()
    assert (coords[~types, 1] <= -0.25).all()
    assert (np.abs(coords[:, 1]) <= 1.25).all()
    assert (np.abs(coords[:, 0]) <= 1).all()
