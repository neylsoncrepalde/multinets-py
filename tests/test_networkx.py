"""The same features on networkx graphs."""

import random
from collections import Counter

import pytest

nx = pytest.importorskip("networkx")

import multinets as mn  # noqa: E402
from helpers import check_levels  # noqa: E402


def to_nx(g, cls=None, type_attr="type"):
    """Copy an igraph graph into networkx with string node ids, in shuffled order."""
    G = (cls or nx.Graph)()
    nodes = list(range(g.vcount()))
    random.Random(0).shuffle(nodes)
    G.add_nodes_from((f"v{i}", {type_attr: g.vs[i]["type"]}) for i in nodes)
    G.add_edges_from((f"v{e.source}", f"v{e.target}") for e in g.es)
    return G


@pytest.fixture
def G(linked_sim):
    return to_nx(linked_sim)


def no_igraph_leftovers(H):
    return all(not k.startswith("_") for _, d in H.nodes(data=True) for k in d) and all(
        not k.startswith("_") for *_, d in H.edges(data=True) for k in d
    )


def test_is_multilevel(G, linked_sim, g_bip, rfid):
    assert mn.is_multilevel(G)
    assert not mn.is_multilevel(to_nx(g_bip))
    with pytest.raises(ValueError, match="Data is not bipartite"):
        mn.is_multilevel(nx.karate_club_graph())
    G.nodes["v0"].pop("type")
    with pytest.raises(ValueError, match="must be boolean"):
        mn.is_multilevel(G)


def test_networkx_bipartite_convention(linked_sim):
    G = to_nx(linked_sim, type_attr="bipartite")
    assert mn.is_multilevel(G, type_attr="bipartite")
    assert mn.extract_highlevel(G, type_attr="bipartite").number_of_nodes() == 50


@pytest.mark.parametrize(
    ("extract", "counts", "level"),
    [
        (mn.extract_highlevel, (50, 89), {True}),
        (mn.extract_lowlevel, (100, 304), {False}),
        (mn.extract_mesolevel, (150, 207), {True, False}),
    ],
)
def test_extractions(G, extract, counts, level):
    H = extract(G)
    assert type(H) is nx.Graph
    assert (H.number_of_nodes(), H.number_of_edges()) == counts
    assert {d["type"] for _, d in H.nodes(data=True)} == level
    assert set(H) <= set(G) and set(H.edges) <= set(G.edges)
    assert no_igraph_leftovers(H)


@pytest.mark.parametrize("cls", [nx.DiGraph, nx.MultiGraph])
def test_graph_class_is_kept(linked_sim, cls):
    G = to_nx(linked_sim, cls)
    assert type(mn.extract_lowlevel(G)) is cls
    assert type(mn.set_shape_multilevel(G)) is cls


def test_multigraph_keeps_parallel_edges_and_keys(linked_sim):
    G = to_nx(linked_sim, nx.MultiGraph)
    u, v = next((u, v) for u, v in G.edges() if G.nodes[u]["type"] and G.nodes[v]["type"])
    G.add_edge(u, v, key="again", weight=3)
    H = mn.extract_highlevel(G)
    assert H.number_of_edges(u, v) == 2
    assert H.edges[u, v, "again"]["weight"] == 3


def test_layout(G):
    pos = mn.layout_multilevel(G)
    assert set(pos) == set(G)
    nodes = list(G)
    check_levels([pos[n] for n in nodes], [G.nodes[n]["type"] for n in nodes])


def test_networkx_layout_function(G):
    pos = mn.layout_multilevel(G, layout=nx.spring_layout, seed=1)
    nodes = list(G)
    check_levels([pos[n] for n in nodes], [G.nodes[n]["type"] for n in nodes])


def test_set_color(G):
    colored = mn.set_color_multilevel(G)
    assert all("color" not in d for _, d in G.nodes(data=True))
    for node, data in colored.nodes(data=True):
        assert data["color"] == ("#0000FFB3" if data["type"] else "#FF0000B3")
    for u, v, data in colored.edges(data=True):
        tu, tv = colored.nodes[u]["type"], colored.nodes[v]["type"]
        assert data["color"] == ("#BEBEBEB3" if tu != tv else "#0000FFB3" if tu else "#FF0000B3")
    assert Counter(c for *_, c in colored.edges(data="color")) == {
        "#FF0000B3": 304, "#BEBEBEB3": 207, "#0000FFB3": 89
    }


def test_set_shape_inplace(G):
    assert mn.set_shape_multilevel(G, inplace=True) is None
    assert {d["shape"] for _, d in G.nodes(data=True)} == {"square", "circle"}


def test_mode_transformation(G):
    low, high = mn.mode_transformation(mn.extract_mesolevel(G))
    assert type(low) is type(high) is nx.Graph
    assert (low.number_of_nodes(), low.number_of_edges(), low.size(weight="weight")) == (100, 410, 429)
    assert (high.number_of_nodes(), high.number_of_edges(), high.size(weight="weight")) == (50, 185, 202)
    assert no_igraph_leftovers(low)


def test_mode_transformation_of_directed_graph_is_undirected(linked_sim):
    meso = mn.extract_mesolevel(to_nx(linked_sim, nx.DiGraph))
    assert type(meso) is nx.DiGraph
    assert type(mn.mode_transformation(meso, "high")) is nx.Graph
