import warnings

import igraph as ig
import pytest
from helpers import make_graph

from multinets import Projections, extract_mesolevel, mode_transformation


def test_mode_transformation_responds_properly_to_different_objects(linked_sim, g_bip, rfid):
    with pytest.raises(ValueError, match="must be bipartite but not multilevel"):
        mode_transformation(linked_sim, "high")
    with pytest.raises(ValueError, match="Data is not bipartite"):
        mode_transformation(rfid, "high")
    with pytest.raises(TypeError, match="Not a graph object"):
        mode_transformation([1, 2], "high")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        mode_transformation(g_bip, "high")


def test_mode_transformation_works_without_specifying_which(g_bip):
    projections = mode_transformation(g_bip)
    assert isinstance(projections, Projections)
    assert isinstance(projections.low, ig.Graph)
    assert isinstance(projections.high, ig.Graph)
    low, high = projections
    expected_low, expected_high = g_bip.bipartite_projection(types="type")
    assert low.vs["name"] == expected_low.vs["name"] == ["actor1", "actor2", "actor3"]
    assert high.vs["name"] == expected_high.vs["name"] == ["movie1", "movie2"]


def test_which(g_bip):
    assert mode_transformation(g_bip, "high").vs["name"] == ["movie1", "movie2"]
    assert mode_transformation(g_bip, "low").vs["name"] == ["actor1", "actor2", "actor3"]
    with pytest.raises(ValueError, match="`which` must be one of"):
        mode_transformation(g_bip, "true")


def test_projection_of_mesolevel_matches_r(linked_sim):
    low, high = mode_transformation(extract_mesolevel(linked_sim))
    # Counts and total weights computed with the R package on the same data.
    assert (low.vcount(), low.ecount(), sum(low.es["weight"])) == (100, 410, 429)
    assert (high.vcount(), high.ecount(), sum(high.es["weight"])) == (50, 185, 202)


@pytest.mark.parametrize("extra", [(0, 1), (3, 3)])
def test_ties_within_a_level_are_rejected(extra):
    # Not multilevel (only one level has internal ties) but not 2-mode either.
    g = make_graph([False, False, False, True, True], [(0, 3), (1, 3), (0, 4), extra])
    with pytest.raises(ValueError, match="same level"):
        mode_transformation(g)
