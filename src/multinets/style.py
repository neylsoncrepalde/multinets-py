"""Visual attributes (colors and shapes) for the levels of a multilevel network."""

from __future__ import annotations

from typing import Sequence

import igraph as ig
import numpy as np
from igraph.drawing.colors import color_name_to_rgba

from ._graph import GraphT, check_graph, require_multilevel, tie_masks


def set_color_multilevel(
    x: GraphT,
    color_true: str = "blue",
    color_false: str = "red",
    v_alpha: float = 0.7,
    e_alpha: float = 0.7,
    *,
    type_attr: str = "type",
    inplace: bool = False,
) -> GraphT | None:
    """Set vertex and edge colors for the levels of a multilevel network.

    Vertices and the edges within each level get the color of their level:
    blue for the higher level and red for the lower level by default. Edges
    across levels are grey. Colors are stored as ``"#RRGGBBAA"`` strings,
    which igraph and matplotlib (and therefore networkx) all understand.

    Parameters
    ----------
    x : igraph.Graph or networkx.Graph
        A multilevel network.
    color_true : str
        Color for the higher level (``type_attr`` set to ``True``).
    color_false : str
        Color for the lower level (``type_attr`` set to ``False``).
    v_alpha : float
        Factor modifying the opacity of vertex colors, typically in [0, 1].
    e_alpha : float
        Factor modifying the opacity of edge colors, typically in [0, 1].
    type_attr : str
        Name of the vertex attribute holding each vertex's level.
    inplace : bool
        If ``False`` (default), return a modified copy and leave ``x``
        untouched. If ``True``, modify ``x`` itself and return ``None``.

    Returns
    -------
    igraph.Graph or networkx.Graph or None
        The graph with a ``color`` vertex attribute and a ``color`` edge
        attribute, or ``None`` if ``inplace=True``.

    Examples
    --------
    >>> from multinets import load_linked_sim, set_color_multilevel
    >>> linked_sim = set_color_multilevel(load_linked_sim())
    """
    target = _target(x, inplace)
    types, edges = require_multilevel(target, type_attr)
    high, low, _ = tie_masks(types, edges)

    v_true, v_false = _adjust_color(color_true, v_alpha), _adjust_color(color_false, v_alpha)
    e_true, e_false = _adjust_color(color_true, e_alpha), _adjust_color(color_false, e_alpha)
    e_diff = _adjust_color("grey", e_alpha)

    _set_vertex_attr(target, "color", np.where(types, v_true, v_false).tolist())
    _set_edge_attr(target, "color", np.select([high, low], [e_true, e_false], e_diff).tolist())
    return None if inplace else target


def set_shape_multilevel(
    x: GraphT,
    shape_true: str = "square",
    shape_false: str = "circle",
    *,
    type_attr: str = "type",
    inplace: bool = False,
) -> GraphT | None:
    """Set vertex shapes for the levels of a multilevel network.

    Parameters
    ----------
    x : igraph.Graph or networkx.Graph
        A multilevel network.
    shape_true : str
        Shape for the higher level (``type_attr`` set to ``True``).
    shape_false : str
        Shape for the lower level (``type_attr`` set to ``False``).
    type_attr : str
        Name of the vertex attribute holding each vertex's level.
    inplace : bool
        If ``False`` (default), return a modified copy and leave ``x``
        untouched. If ``True``, modify ``x`` itself and return ``None``.

    Returns
    -------
    igraph.Graph or networkx.Graph or None
        The graph with a ``shape`` vertex attribute, or ``None`` if
        ``inplace=True``.

    Examples
    --------
    >>> from multinets import load_linked_sim, set_shape_multilevel
    >>> linked_sim = set_shape_multilevel(load_linked_sim())
    """
    target = _target(x, inplace)
    types, _ = require_multilevel(target, type_attr)
    _set_vertex_attr(target, "shape", np.where(types, shape_true, shape_false).tolist())
    return None if inplace else target


def _target(x, inplace: bool):
    check_graph(x)
    return x if inplace else x.copy()


def _adjust_color(color, alpha: float) -> str:
    """Port of R's ``grDevices::adjustcolor(color, alpha.f = alpha)``."""
    *rgb, a = color_name_to_rgba(color)
    a = min(max(a * alpha, 0.0), 1.0)
    return "#" + "".join(f"{int(c * 255 + 0.5):02X}" for c in (*rgb, a))


def _set_vertex_attr(g, name: str, values: Sequence) -> None:
    if isinstance(g, ig.Graph):
        g.vs[name] = values
    else:
        for node, value in zip(g, values):
            g.nodes[node][name] = value


def _set_edge_attr(g, name: str, values: Sequence) -> None:
    if isinstance(g, ig.Graph):
        g.es[name] = values
    else:
        for (*_, data), value in zip(g.edges(data=True), values):
            data[name] = value
