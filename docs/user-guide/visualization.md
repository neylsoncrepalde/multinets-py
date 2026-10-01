---
file_format: mystnb
kernelspec:
  name: python3
---

# Visualization

Multilevel networks are easier to read when each level has its own area of the
plot and its own colors and shapes. `multinets` does each of those in one call,
and igraph's {func}`igraph.plot <igraph.drawing.plot>` picks them up.

```{code-cell} ipython3
import random

import igraph as ig
import matplotlib.pyplot as plt
from multinets import (
    layout_multilevel,
    load_linked_sim,
    set_color_multilevel,
    set_shape_multilevel,
)

random.seed(42)  # igraph layouts use Python's random module
linked_sim = load_linked_sim()
```

## Layout

{func}`~multinets.layout_multilevel` runs a layout algorithm, rescales the
coordinates to [-1, 1] and moves the higher level up and the lower level down,
with a gap between them. The default algorithm is Fruchterman-Reingold. Any
[igraph layout](https://python.igraph.org/en/stable/tutorial.html#layout-algorithms)
name works, or a function that returns coordinates:

```{code-cell} ipython3
styled = set_shape_multilevel(set_color_multilevel(linked_sim))

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, layout in zip(axes, ["fr", "kk", "drl"]):
    ig.plot(styled, target=ax, layout=layout_multilevel(linked_sim, layout=layout),
            vertex_size=6, edge_width=0.4)
    ax.set_title(f'layout="{layout}"')
```

Extra keyword arguments go to the layout algorithm:

```{code-cell} ipython3
l = layout_multilevel(linked_sim, layout="kk", maxiter=5000)
l3d = layout_multilevel(linked_sim, dim=3)
l3d.dim
```

The result is an {class}`igraph.Layout <igraph.layout.Layout>`. In a 3D layout
the levels are split along the second (y) axis.

## Colors

{func}`~multinets.set_color_multilevel` adds a `color` attribute to vertices
and edges. By default the higher level is blue, the lower level is red and the
ties across levels are grey, all semi-transparent. Colors are stored as
`"#RRGGBBAA"` strings, the same values R's `adjustcolor()` gives:

```{code-cell} ipython3
colored = set_color_multilevel(linked_sim)
sorted(set(colored.vs["color"])), sorted(set(colored.es["color"]))
```

Any color name or hex code works, with separate opacities for vertices and
edges:

```{code-cell} ipython3
colored = set_color_multilevel(
    linked_sim, "darkgreen", "orange", v_alpha=1, e_alpha=0.3
)
fig, ax = plt.subplots(figsize=(7, 6))
ig.plot(colored, target=ax, layout=l, vertex_size=7, edge_width=0.6);
```

## Shapes

{func}`~multinets.set_shape_multilevel` adds a `shape` vertex attribute: squares
for the higher level and circles for the lower level by default. Other igraph
shapes include `"triangle-up"`, `"triangle-down"`, `"diamond"` and
`"rectangle"`.

```{code-cell} ipython3
shaped = set_shape_multilevel(colored, "diamond", "triangle-up")
fig, ax = plt.subplots(figsize=(7, 6))
ig.plot(shaped, target=ax, layout=l, vertex_size=8, edge_width=0.6);
```

## Copy or modify in place

The color and shape functions return a modified **copy** and leave the original
graph untouched:

```{code-cell} ipython3
"color" in linked_sim.vs.attributes()
```

Pass `inplace=True` to modify the graph itself. The function then returns
`None`, like other Python functions that modify their argument:

```{code-cell} ipython3
set_color_multilevel(linked_sim, inplace=True)
"color" in linked_sim.vs.attributes()
```
