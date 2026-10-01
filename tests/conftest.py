import igraph as ig
import pytest

from multinets import load_linked_sim


@pytest.fixture
def linked_sim():
    return load_linked_sim()


@pytest.fixture
def g_bip():
    """``sand::g.bip``: a toy 2-mode (actors x movies) network, not multilevel."""
    g = ig.Graph()
    g.add_vertices(["actor1", "actor2", "actor3", "movie1", "movie2"])
    g.add_edges([("actor1", "movie1"), ("actor2", "movie1"), ("actor1", "movie2")])
    g.vs["type"] = [name.startswith("movie") for name in g.vs["name"]]
    return g


@pytest.fixture
def rfid():
    """Stands in for ``igraphdata::rfid``: a 1-mode graph with no ``type`` attribute."""
    return ig.Graph.Famous("Zachary")

