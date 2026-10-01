import igraph as ig
import pytest

from multinets import extract_highlevel, extract_lowlevel, extract_mesolevel

EXTRACTORS = [extract_highlevel, extract_lowlevel, extract_mesolevel]


@pytest.mark.parametrize("extract", EXTRACTORS)
def test_extractions_reject_non_multilevel(extract, g_bip, rfid):
    with pytest.raises(ValueError, match="not multilevel"):
        extract(g_bip)
    with pytest.raises(ValueError, match="Data is not bipartite"):
        extract(rfid)
    with pytest.raises(TypeError, match="Not a graph object"):
        extract("not a graph")


# Vertex and edge counts computed with the R package on the same data.
@pytest.mark.parametrize(
    ("extract", "vcount", "ecount"),
    [(extract_highlevel, 50, 89), (extract_lowlevel, 100, 304), (extract_mesolevel, 150, 207)],
)
def test_extractions_match_r(linked_sim, extract, vcount, ecount):
    level = extract(linked_sim)
    assert isinstance(level, ig.Graph)
    assert (level.vcount(), level.ecount()) == (vcount, ecount)
    assert (linked_sim.vcount(), linked_sim.ecount()) == (150, 600)


def test_extracted_levels_keep_the_right_vertices(linked_sim):
    assert all(extract_highlevel(linked_sim).vs["type"])
    assert not any(extract_lowlevel(linked_sim).vs["type"])


def test_mesolevel_only_keeps_cross_level_ties(linked_sim):
    meso = extract_mesolevel(linked_sim)
    assert meso.vs["type"] == linked_sim.vs["type"]
    assert all(meso.vs[e.source]["type"] != meso.vs[e.target]["type"] for e in meso.es)
