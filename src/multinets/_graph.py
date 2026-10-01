"""Internal helpers shared by the public functions.

Every public function accepts either an :class:`igraph.Graph` or a networkx
graph. Levels are read from a boolean vertex attribute (``"type"`` by
default): ``True`` marks the higher level and ``False`` the lower level. This
is the same convention igraph uses for bipartite graphs.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, TypeVar

import igraph as ig
import numpy as np

if TYPE_CHECKING:
    import networkx as nx

GraphT = TypeVar("GraphT", ig.Graph, "nx.Graph")


def is_networkx(x: Any) -> bool:
    # If x is a networkx graph, networkx has already been imported.
    nx = sys.modules.get("networkx")
    return nx is not None and isinstance(x, nx.Graph)


def check_graph(x: Any) -> None:
    if not isinstance(x, ig.Graph) and not is_networkx(x):
        raise TypeError("Not a graph object")


def levels(x: Any, type_attr: str) -> tuple[np.ndarray, np.ndarray]:
    """Return vertex types and the (E, 2) array of edge endpoints.

    Both follow the graph's own vertex and edge iteration order. Raises if
    ``x`` is not a graph or does not have a valid bipartite ``type_attr``.
    """
    check_graph(x)
    if isinstance(x, ig.Graph):
        if type_attr not in x.vs.attributes():
            raise ValueError("Data is not bipartite")
        raw = x.vs[type_attr]
        edges = x.get_edgelist()
    else:
        if not any(type_attr in data for _, data in x.nodes(data=True)):
            raise ValueError("Data is not bipartite")
        nodes = list(x)
        index = {node: i for i, node in enumerate(nodes)}
        raw = [x.nodes[node].get(type_attr) for node in nodes]
        edges = [(index[u], index[v]) for u, v in x.edges()]

    # Accepts bools and 0/1; rejects missing values (None, NaN) and anything else.
    if any(t not in (True, False) for t in raw):
        raise ValueError(
            f"Vertex attribute '{type_attr}' must be boolean for every vertex "
            "(True for the higher level, False for the lower level)"
        )
    return np.array(raw, dtype=bool), np.array(edges, dtype=np.int64).reshape(-1, 2)


def tie_masks(
    types: np.ndarray, edges: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Edge masks for ties within the higher level, within the lower level and across levels."""
    source, target = types[edges[:, 0]], types[edges[:, 1]]
    return source & target, ~source & ~target, source != target


def has_multilevel_ties(types: np.ndarray, edges: np.ndarray) -> bool:
    high, low, cross = tie_masks(types, edges)
    # A self-loop is not a tie between two vertices of the same level.
    not_loop = edges[:, 0] != edges[:, 1]
    return bool((high & not_loop).any() and (low & not_loop).any() and cross.any())


def require_multilevel(x: Any, type_attr: str) -> tuple[np.ndarray, np.ndarray]:
    types, edges = levels(x, type_attr)
    if not has_multilevel_ties(types, edges):
        raise ValueError("The network is not multilevel")
    return types, edges


def to_igraph(x: Any) -> ig.Graph:
    check_graph(x)
    return x if isinstance(x, ig.Graph) else ig.Graph.from_networkx(x)


def like(result: ig.Graph, x: Any) -> Any:
    """Convert an igraph result back to the kind of graph the user passed in."""
    if isinstance(x, ig.Graph):
        return result
    cls = type(x) if result.is_directed() == x.is_directed() else None
    out = result.to_networkx(create_using=cls)
    # to_networkx() tags every node and edge with its igraph index.
    for _, data in out.nodes(data=True):
        data.pop("_igraph_index", None)
    for *_, data in out.edges(data=True):
        data.pop("_igraph_index", None)
    return out


def node_ids(g: ig.Graph, x: Any) -> list:
    """Identifiers of the vertices of ``g = to_igraph(x)``, in igraph order."""
    return list(range(g.vcount())) if isinstance(x, ig.Graph) else g.vs["_nx_name"]
