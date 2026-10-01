"""Regenerates docs/figures/readme-example.png (the README example)."""

import random

import igraph as ig
import matplotlib.pyplot as plt

from multinets import (
    is_multilevel,
    layout_multilevel,
    load_linked_sim,
    set_color_multilevel,
    set_shape_multilevel,
)

random.seed(1)
linked_sim = load_linked_sim()
assert is_multilevel(linked_sim)

l = layout_multilevel(linked_sim, layout="kk")
linked_sim = set_color_multilevel(linked_sim)
linked_sim = set_shape_multilevel(linked_sim)

fig, ax = plt.subplots(figsize=(8, 7))
ig.plot(linked_sim, target=ax, layout=l, vertex_size=7, edge_width=0.6)
fig.savefig("docs/figures/readme-example.png", dpi=100, bbox_inches="tight")
