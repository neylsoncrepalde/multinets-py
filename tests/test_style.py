from collections import Counter

import pytest

from multinets import set_color_multilevel, set_shape_multilevel

# Values of grDevices::adjustcolor() in R.
BLUE, RED, GREY = "#0000FFB3", "#FF0000B3", "#BEBEBEB3"


def test_set_color_multilevel(linked_sim):
    colored = set_color_multilevel(linked_sim)
    assert colored.vs["color"] == [BLUE if t else RED for t in linked_sim.vs["type"]]
    types = colored.vs["type"]
    for edge in colored.es:
        source, target = types[edge.source], types[edge.target]
        expected = GREY if source != target else (BLUE if source else RED)
        assert edge["color"] == expected
    assert Counter(colored.es["color"]) == {RED: 304, GREY: 207, BLUE: 89}


def test_set_color_arguments(linked_sim):
    colored = set_color_multilevel(linked_sim, "green", "#FFA500", v_alpha=1, e_alpha=0.5)
    assert set(colored.vs["color"]) == {"#00FF00FF", "#FFA500FF"}
    assert set(colored.es["color"]) == {"#00FF0080", "#FFA50080", "#BEBEBE80"}


def test_set_shape_multilevel(linked_sim):
    shaped = set_shape_multilevel(linked_sim)
    assert shaped.vs["shape"] == ["square" if t else "circle" for t in linked_sim.vs["type"]]
    shaped = set_shape_multilevel(linked_sim, shape_true="triangle-up", shape_false="diamond")
    assert set(shaped.vs["shape"]) == {"triangle-up", "diamond"}


@pytest.mark.parametrize(("setter", "attr"), [(set_color_multilevel, "color"), (set_shape_multilevel, "shape")])
def test_copy_by_default(linked_sim, setter, attr):
    result = setter(linked_sim)
    assert result is not linked_sim
    assert attr in result.vs.attributes()
    assert attr not in linked_sim.vs.attributes()


@pytest.mark.parametrize(("setter", "attr"), [(set_color_multilevel, "color"), (set_shape_multilevel, "shape")])
def test_inplace(linked_sim, setter, attr):
    assert setter(linked_sim, inplace=True) is None
    assert attr in linked_sim.vs.attributes()


@pytest.mark.parametrize("setter", [set_color_multilevel, set_shape_multilevel])
def test_setters_reject_non_multilevel(setter, g_bip, rfid):
    with pytest.raises(ValueError, match="not multilevel"):
        setter(g_bip, inplace=True)
    assert "color" not in g_bip.vs.attributes() and "shape" not in g_bip.vs.attributes()
    with pytest.raises(ValueError, match="Data is not bipartite"):
        setter(rfid)
    with pytest.raises(TypeError, match="Not a graph object"):
        setter(None)
