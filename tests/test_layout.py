import random

import igraph as ig
import numpy as np
import pytest

from helpers import check_levels

from multinets import layout_multilevel


def test_layout_responds_correctly_to_various_objects(linked_sim, g_bip, rfid):
    with pytest.raises(ValueError, match="not multilevel"):
        layout_multilevel(g_bip)
    with pytest.raises(ValueError, match="Data is not bipartite"):
        layout_multilevel(rfid)
    assert isinstance(layout_multilevel(linked_sim), ig.Layout)


@pytest.mark.parametrize("layout", ["fr", "kk", "drl", "circle", "star", "tree", "grid"])
def test_levels_are_separated(linked_sim, layout):
    l = layout_multilevel(linked_sim, layout=layout)
    assert l.dim == 2
    check_levels(l.coords, linked_sim.vs["type"])


def test_callable_layout_and_kwargs(linked_sim):
    l = layout_multilevel(linked_sim, layout=ig.Graph.layout_kamada_kawai, maxiter=10)
    check_levels(l.coords, linked_sim.vs["type"])


def test_three_dimensional_layout(linked_sim):
    coords = np.array(layout_multilevel(linked_sim, dim=3).coords)
    assert coords.shape == (150, 3)
    check_levels(coords, linked_sim.vs["type"])
    assert coords[:, 2].min() == -1 and coords[:, 2].max() == 1


def test_seeded_layout_is_reproducible(linked_sim):
    random.seed(42)
    first = layout_multilevel(linked_sim).coords
    random.seed(42)
    assert layout_multilevel(linked_sim).coords == first
