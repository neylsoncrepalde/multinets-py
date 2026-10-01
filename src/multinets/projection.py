"""2-mode to 1-mode transformation."""

from __future__ import annotations

from typing import Any, NamedTuple

from ._graph import GraphT, has_multilevel_ties, levels, like, tie_masks, to_igraph


class Projections(NamedTuple):
    """Both 1-mode projections of a bipartite network."""

    low: Any
    """Network of lower level vertices tied when they share a higher level vertex."""
    high: Any
    """Network of higher level vertices tied when they share a lower level vertex."""


def mode_transformation(
    x: GraphT, which: str = "both", *, type_attr: str = "type"
) -> Projections | GraphT:
    """Transform a bipartite (2-mode) network into 1-mode networks.

    Wraps :meth:`igraph.Graph.bipartite_projection`. It is meant as an
    analysis tool for a bipartite network obtained from
    :func:`extract_mesolevel`.

    Two higher level vertices are tied when they share a lower level vertex,
    and two lower level vertices are tied when they are affiliated to the same
    higher level vertex. The ``weight`` edge attribute counts how many
    vertices they share.

    Parameters
    ----------
    x : igraph.Graph or networkx.Graph
        A bipartite graph. It must not be multilevel and must have no ties
        between vertices of the same level.
    which : {"both", "high", "low"}
        ``"high"`` projects onto the higher level, ``"low"`` onto the lower
        level and ``"both"`` returns both networks.
    type_attr : str
        Name of the vertex attribute holding each vertex's level.

    Returns
    -------
    Projections or igraph.Graph or networkx.Graph
        If ``which="both"``, a :class:`Projections` named tuple with fields
        ``low`` and ``high``. Otherwise a single graph. Graphs are of the same
        kind as ``x``.

    Examples
    --------
    >>> from multinets import load_linked_sim, extract_mesolevel, mode_transformation
    >>> affiliation = extract_mesolevel(load_linked_sim())
    >>> transformed = mode_transformation(affiliation)
    >>> high_transformed = mode_transformation(affiliation, which="high")
    """
    g = to_igraph(x)
    if which not in ("both", "high", "low"):
        raise ValueError(f"`which` must be one of 'both', 'high' or 'low', not {which!r}")
    types, edges = levels(g, type_attr)
    if has_multilevel_ties(types, edges):
        raise ValueError("Data must be bipartite but not multilevel")
    high, low, _ = tie_masks(types, edges)
    if high.any() or low.any():
        raise ValueError(
            "Data is not bipartite: there are ties between vertices of the same level"
        )

    types = types.tolist()
    if which == "both":
        low_projection, high_projection = g.bipartite_projection(types=types)
        return Projections(low=like(low_projection, x), high=like(high_projection, x))
    projection = g.bipartite_projection(types=types, which=1 if which == "high" else 0)
    return like(projection, x)
