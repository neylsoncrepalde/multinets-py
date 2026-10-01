"""Layout for multilevel networks."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Callable

import igraph as ig
import numpy as np

from ._graph import GraphT, node_ids, require_multilevel, to_igraph

# Vertical distance added between the two levels, on each side of y = 0.
_LEVEL_GAP = 0.25


def layout_multilevel(
    x: GraphT,
    layout: str | Callable[..., Any] = "fr",
    *,
    type_attr: str = "type",
    **kwargs: Any,
) -> ig.Layout | dict:
    """Set layout coordinates for a multilevel network from a chosen algorithm.

    To make multilevel networks easier to read, higher level vertices are
    placed in the upper part of the plane and lower level vertices in the
    lower part. Coordinates are first rescaled to [-1, 1] as
    ``igraph::norm_coords()`` does, then the levels are pushed 0.25 apart from
    y = 0.

    Parameters
    ----------
    x : igraph.Graph or networkx.Graph
        A multilevel network.
    layout : str or callable
        The layout algorithm. Either the name of an igraph layout (``"fr"``
        for Fruchterman-Reingold, the default, ``"kk"`` for Kamada-Kawai,
        ``"drl"``, ``"circle"``... see :meth:`igraph.Graph.layout`) or a
        callable that takes ``x`` and returns coordinates, such as
        :meth:`igraph.Graph.layout_kamada_kawai <igraph.GraphBase.layout_kamada_kawai>`
        or :func:`networkx.spring_layout <networkx.drawing.layout.spring_layout>`.
    type_attr : str
        Name of the vertex attribute holding each vertex's level.
    **kwargs
        Passed on to the layout algorithm (for example ``dim=3``).

    Returns
    -------
    igraph.Layout or dict
        For an igraph graph, an :class:`igraph.Layout <igraph.layout.Layout>`
        with one row of coordinates per vertex id, ready for
        :func:`igraph.plot() <igraph.drawing.plot>`. For a networkx graph, a
        ``{node: coordinates}`` dict, ready for
        :func:`networkx.draw() <networkx.drawing.nx_pylab.draw>`.

    Examples
    --------
    >>> import igraph as ig
    >>> from multinets import load_linked_sim, layout_multilevel
    >>> linked_sim = load_linked_sim()
    >>> l = layout_multilevel(linked_sim)
    >>> l_kk = layout_multilevel(linked_sim, layout="kk")
    >>> l_kk = layout_multilevel(linked_sim, layout=ig.Graph.layout_kamada_kawai)
    """
    g = to_igraph(x)
    types, _ = require_multilevel(g, type_attr)
    ids = node_ids(g, x)

    coords = layout(x, **kwargs) if callable(layout) else g.layout(layout, **kwargs)
    if isinstance(coords, Mapping):
        coords = [coords[i] for i in ids]
    elif isinstance(coords, ig.Layout):
        coords = coords.coords
    coords = _norm_coords(np.asarray(coords, dtype=float))

    # Send the higher level up and the lower level down.
    y = np.abs(coords[:, 1]) + _LEVEL_GAP
    coords[:, 1] = np.where(types, y, -y)

    if isinstance(x, ig.Graph):
        return ig.Layout(coords.tolist())
    return dict(zip(ids, coords))


def _norm_coords(coords: np.ndarray, low: float = -1.0, high: float = 1.0) -> np.ndarray:
    """Port of ``igraph::norm_coords()``: rescale every column to [low, high]."""
    minimum, span = coords.min(axis=0), np.ptp(coords, axis=0)
    constant = span == 0
    scaled = (coords - minimum) / np.where(constant, 1.0, span) * (high - low) + low
    scaled[:, constant] = (low + high) / 2
    return scaled
