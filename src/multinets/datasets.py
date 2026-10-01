"""A simulated multilevel network following the linked design."""

from __future__ import annotations

from importlib.resources import as_file, files

import igraph as ig
import numpy as np


def load_linked_sim() -> ig.Graph:
    """Load ``linked_sim``, a simulated multilevel network.

    Follows the *linked design* proposed by Lazega et al. (2008). The graph
    has 150 vertices and 600 edges. The vertex attribute ``type`` defines the
    level of each vertex: ``False`` means lower level (100 vertices) and
    ``True`` means higher level (50 vertices).

    Returns
    -------
    igraph.Graph
        A new copy of the network on every call.

    References
    ----------
    Lazega, E., Jourda, M. T., Mounier, L., & Stofer, R. (2008). Catching up
    with big fish in the big pond? Multi-level network analysis through linked
    design. *Social Networks*, 30(2), 159-176.
    """
    with as_file(files("multinets") / "data" / "linked_sim.graphml") as path:
        g = ig.Graph.Read_GraphML(str(path))
    del g.vs["id"]  # Node ids added by the GraphML reader.
    return g


def load_linked_sim_matrix() -> np.ndarray:
    """Load the 150 x 150 adjacency matrix of :func:`load_linked_sim`."""
    return np.array(load_linked_sim().get_adjacency().data)


def load_linked_sim_type() -> np.ndarray:
    """Load the level of each vertex of :func:`load_linked_sim` (``True`` = higher level)."""
    return np.array(load_linked_sim().vs["type"], dtype=bool)
