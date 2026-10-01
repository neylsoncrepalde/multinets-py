"""Multilevel network definition and extraction of its levels."""

from __future__ import annotations

import numpy as np

from ._graph import (
    GraphT,
    has_multilevel_ties,
    levels,
    like,
    require_multilevel,
    tie_masks,
    to_igraph,
)


def is_multilevel(x: GraphT, *, type_attr: str = "type") -> bool:
    """Check whether a graph is multilevel.

    Follows the *linked design* proposed by Lazega et al. (2008). A multilevel
    network has two kinds of vertices and two kinds of edges. Lower level
    vertices are usually individuals. Higher level vertices are usually
    organizations, collectivities or other joint social structures. The first
    kind of edge links vertices of the same level. The second kind links
    vertices of different levels (affiliation ties).

    Put another way, a multilevel network is a bipartite (2-mode) network that
    also has ties between vertices *within each* level. This function checks
    that the graph:

    * is bipartite, i.e. it has a boolean vertex attribute ``type_attr``
      (``True`` for the higher level, ``False`` for the lower level), the same
      convention igraph uses for bipartite graphs;
    * has at least one tie across levels;
    * has at least one tie between two vertices of the higher level and at
      least one between two vertices of the lower level (self-loops do not
      count).

    Note that :meth:`igraph.Graph.is_bipartite() <igraph.GraphBase.is_bipartite>`
    is a different, purely structural test (is the graph 2-colourable?) that
    multilevel networks usually fail.

    Parameters
    ----------
    x : igraph.Graph or networkx.Graph
        A graph object.
    type_attr : str
        Name of the vertex attribute holding each vertex's level.

    Returns
    -------
    bool

    Raises
    ------
    TypeError
        If ``x`` is not a graph.
    ValueError
        If the graph is not bipartite (no ``type_attr`` vertex attribute) or
        the attribute is not boolean for every vertex.

    References
    ----------
    Lazega, E., Jourda, M. T., Mounier, L., & Stofer, R. (2008). Catching up
    with big fish in the big pond? Multi-level network analysis through linked
    design. *Social Networks*, 30(2), 159-176.

    Lazega, E. and Snijders, T. A. B. (eds) (2016), *Multilevel Network
    Analysis for the Social Sciences: Theory, Methods and Applications*,
    Springer, Methodos Series.

    Examples
    --------
    >>> from multinets import load_linked_sim, is_multilevel
    >>> is_multilevel(load_linked_sim())
    True
    """
    return has_multilevel_ties(*levels(x, type_attr))


def extract_highlevel(x: GraphT, *, type_attr: str = "type") -> GraphT:
    """Extract the higher level of a multilevel network.

    Keeps the higher level vertices (``type_attr`` set to ``True``) and the
    edges between them.

    Parameters
    ----------
    x : igraph.Graph or networkx.Graph
        A multilevel network.
    type_attr : str
        Name of the vertex attribute holding each vertex's level.

    Returns
    -------
    igraph.Graph or networkx.Graph
        A 1-mode network, of the same kind as ``x``.

    See Also
    --------
    extract_lowlevel, extract_mesolevel

    Examples
    --------
    >>> from multinets import load_linked_sim, extract_highlevel
    >>> organizations = extract_highlevel(load_linked_sim())
    """
    return _extract_level(x, type_attr, high=True)


def extract_lowlevel(x: GraphT, *, type_attr: str = "type") -> GraphT:
    """Extract the lower level of a multilevel network.

    Keeps the lower level vertices (``type_attr`` set to ``False``) and the
    edges between them.

    Parameters
    ----------
    x : igraph.Graph or networkx.Graph
        A multilevel network.
    type_attr : str
        Name of the vertex attribute holding each vertex's level.

    Returns
    -------
    igraph.Graph or networkx.Graph
        A 1-mode network, of the same kind as ``x``.

    See Also
    --------
    extract_highlevel, extract_mesolevel

    Examples
    --------
    >>> from multinets import load_linked_sim, extract_lowlevel
    >>> individuals = extract_lowlevel(load_linked_sim())
    """
    return _extract_level(x, type_attr, high=False)


def extract_mesolevel(x: GraphT, *, type_attr: str = "type") -> GraphT:
    """Extract the meso level of a multilevel network.

    Keeps all the vertices but only the edges between vertices of different
    levels. The literature also calls this an *affiliation* network.

    Parameters
    ----------
    x : igraph.Graph or networkx.Graph
        A multilevel network.
    type_attr : str
        Name of the vertex attribute holding each vertex's level.

    Returns
    -------
    igraph.Graph or networkx.Graph
        A bipartite (2-mode) network, of the same kind as ``x``.

    See Also
    --------
    extract_highlevel, extract_lowlevel, mode_transformation

    Examples
    --------
    >>> from multinets import load_linked_sim, extract_mesolevel
    >>> affiliations = extract_mesolevel(load_linked_sim())
    """
    g = to_igraph(x)
    types, edges = require_multilevel(g, type_attr)
    _, _, cross = tie_masks(types, edges)
    meso = g.subgraph_edges(np.flatnonzero(cross).tolist(), delete_vertices=False)
    return like(meso, x)


def _extract_level(x, type_attr: str, high: bool):
    g = to_igraph(x)
    types, _ = require_multilevel(g, type_attr)
    vertices = np.flatnonzero(types if high else ~types)
    return like(g.induced_subgraph(vertices.tolist()), x)
