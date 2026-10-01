---
file_format: mystnb
kernelspec:
  name: python3
---

# multinets

**Multilevel network analysis in Python.**

`multinets` provides tools to visualize and analyze multilevel network data, as
described in Lazega et al. (2008) and in Lazega and Snijders (2016). It was
built as an extension to [igraph](https://python.igraph.org) and works with
[networkx](https://networkx.org) graphs too. It is the Python version of the
[multinets R package](https://github.com/neylsoncrepalde/multinets).

```bash
pip install multinets
```

## A first look

`linked_sim` is a simulated multilevel network of 100 individuals (the lower
level) and 50 organizations (the higher level):

```{code-cell} ipython3
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

# Load the dataset
linked_sim = load_linked_sim()

# Test if the data is a multilevel network
is_multilevel(linked_sim)
```

```{code-cell} ipython3
# Set the layout coordinates
l = layout_multilevel(linked_sim, layout="kk")

# Set different colors and shapes for each level vertices
linked_sim = set_color_multilevel(linked_sim)
linked_sim = set_shape_multilevel(linked_sim)

# Plot
fig, ax = plt.subplots(figsize=(8, 7))
ig.plot(linked_sim, target=ax, layout=l, vertex_size=7, edge_width=0.6);
```

Organizations sit at the top and individuals at the bottom. Ties inside each
level have the level's color and affiliation ties are grey.

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} {fas}`book` User guide
:link: user-guide/index
:link-type: doc

What a multilevel network is, and how to analyze and draw one, with igraph or
networkx.
:::

:::{grid-item-card} {fas}`code` API reference
:link: api
:link-type: doc

Every function, its parameters and what it returns.
:::

:::{grid-item-card} {fab}`r-project` Coming from R
:link: coming-from-r
:link-type: doc

The R functions and their Python equivalents, and what changed.
:::

:::{grid-item-card} {fas}`clock-rotate-left` Changelog
:link: changelog
:link-type: doc

What is new in each release.
:::
::::

## References

Lazega, E., Jourda, M. T., Mounier, L., & Stofer, R. (2008). Catching up with
big fish in the big pond? Multi-level network analysis through linked design.
*Social Networks*, 30(2), 159-176.
[doi:10.1016/j.socnet.2008.02.001](https://doi.org/10.1016/j.socnet.2008.02.001)

Lazega, E. and Snijders, T. A. B. (eds) (2016). *Multilevel Network Analysis
for the Social Sciences: Theory, Methods and Applications*. Springer, Methodos
Series. ISBN 978-3-319-24520-1.

```{toctree}
:hidden:

user-guide/index
api
coming-from-r
changelog
```
