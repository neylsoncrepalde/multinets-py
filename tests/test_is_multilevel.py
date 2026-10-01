import pytest
from helpers import make_graph

from multinets import is_multilevel

LOW, HIGH = False, True


def test_is_multilevel_works_properly(linked_sim, g_bip, rfid):
    assert is_multilevel(linked_sim) is True
    assert is_multilevel(g_bip) is False
    with pytest.raises(TypeError, match="Not a graph object"):
        is_multilevel(5)
    with pytest.raises(ValueError, match="Data is not bipartite"):
        is_multilevel(rfid)


@pytest.mark.parametrize(
    ("edges", "expected"),
    [
        ([(0, 1), (2, 3), (0, 2)], True),  # low-low, high-high and cross ties
        ([(0, 1), (0, 2)], False),  # no ties within the higher level
        ([(2, 3), (0, 2)], False),  # no ties within the lower level
        ([(0, 1), (2, 3)], False),  # no ties across levels
        ([(0, 0), (2, 2), (0, 2)], False),  # self-loops are not ties between vertices
        ([], False),
    ],
)
def test_multilevel_definition(edges, expected):
    assert is_multilevel(make_graph([LOW, LOW, HIGH, HIGH], edges)) is expected


def test_single_level_graph_is_not_multilevel():
    assert is_multilevel(make_graph([HIGH, HIGH, HIGH], [(0, 1), (1, 2)])) is False
    assert is_multilevel(make_graph([LOW, LOW, LOW], [(0, 1), (1, 2)])) is False


def test_directed_graphs():
    assert is_multilevel(make_graph([LOW, LOW, HIGH, HIGH], [(1, 0), (3, 2), (2, 0)], directed=True))


def test_integer_types_are_accepted():
    assert is_multilevel(make_graph([0, 0, 1, 1], [(0, 1), (2, 3), (0, 2)]))


@pytest.mark.parametrize("bad", [None, "yes", 2, float("nan")])
def test_invalid_types_raise(bad):
    with pytest.raises(ValueError, match="must be boolean"):
        is_multilevel(make_graph([LOW, bad, HIGH, HIGH], [(0, 1), (2, 3), (0, 2)]))


def test_custom_type_attribute(linked_sim):
    linked_sim.vs["level"] = linked_sim.vs["type"]
    del linked_sim.vs["type"]
    assert is_multilevel(linked_sim, type_attr="level")
    with pytest.raises(ValueError, match="Data is not bipartite"):
        is_multilevel(linked_sim)
