import numpy as np

from multinets import load_linked_sim, load_linked_sim_matrix, load_linked_sim_type


def test_linked_sim(linked_sim):
    assert (linked_sim.vcount(), linked_sim.ecount()) == (150, 600)
    assert not linked_sim.is_directed()
    assert linked_sim.vs.attributes() == ["type"]
    assert all(isinstance(t, bool) for t in linked_sim.vs["type"])
    assert sum(linked_sim.vs["type"]) == 50


def test_each_call_returns_a_new_graph():
    assert load_linked_sim() is not load_linked_sim()


def test_matrix_and_type(linked_sim):
    matrix, types = load_linked_sim_matrix(), load_linked_sim_type()
    assert matrix.shape == (150, 150)
    assert (matrix == matrix.T).all() and matrix.sum() == 2 * 600
    assert (matrix == np.array(linked_sim.get_adjacency().data)).all()
    assert types.dtype == bool and types.tolist() == linked_sim.vs["type"]
