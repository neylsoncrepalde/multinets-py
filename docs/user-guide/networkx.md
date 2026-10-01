---
file_format: mystnb
kernelspec:
  name: python3
---

# Using networkx

Every `multinets` function accepts [networkx](https://networkx.org) graphs as
well as igraph graphs, and gives back networkx objects:

- functions that return a graph return one of the **same class** as their
  input ({class}`networkx.Graph`, {class}`networkx.DiGraph`,
  {class}`networkx.MultiGraph`...). Projections are always undirected.
- {func}`~multinets.layout_multilevel` returns a `{node: coordinates}` dict, as
  networkx layouts do.

Node ids and node and edge attributes are kept. Install networkx support with
`pip install "multinets[networkx]"`.

## Levels

networkx's own convention for bipartite graphs is a `bipartite` node attribute.
Pass `type_attr="bipartite"` to use it (the default is `type`, as in igraph):

```{code-cell} ipython3
import networkx as nx
import multinets as mn

G = nx.Graph()
G.add_nodes_from(["ana", "bruno", "carla", "davi"], bipartite=False)  # people
G.add_nodes_from(["firm1", "firm2"], bipartite=True)                  # firms
G.add_edges_from([
    ("ana", "bruno"), ("bruno", "carla"), ("carla", "davi"),
    ("firm1", "firm2"),
    ("ana", "firm1"), ("bruno", "firm1"), ("carla", "firm2"), ("davi", "firm2"),
])

mn.is_multilevel(G, type_attr="bipartite")
```

## Analysis

```{code-cell} ipython3
people = mn.extract_lowlevel(G, type_attr="bipartite")
affiliations = mn.extract_mesolevel(G, type_attr="bipartite")
print(type(people).__name__, sorted(people.edges()))
print(type(affiliations).__name__, sorted(affiliations.edges()))
```

```{code-cell} ipython3
low, high = mn.mode_transformation(affiliations, type_attr="bipartite")
sorted(low.edges(data="weight"))
```

## Drawing

Layouts can use igraph's algorithms, by name, or networkx's own functions:

```{code-cell} ipython3
pos = mn.layout_multilevel(G, nx.spring_layout, type_attr="bipartite", seed=3)
G = mn.set_color_multilevel(G, type_attr="bipartite")
G = mn.set_shape_multilevel(G, "s", "o", type_attr="bipartite")
```

{func}`networkx.draw <networkx.drawing.nx_pylab.draw>` doesn't read colors or
shapes from the graph, and it draws a single shape per call. So draw the nodes one shape at a time.
matplotlib's markers `"s"` and `"o"` are a square and a circle:

```{code-cell} ipython3
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 5))
edge_colors = [c for *_, c in G.edges(data="color")]
nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors)
for shape in ("s", "o"):
    nodes = [n for n, s in G.nodes(data="shape") if s == shape]
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_shape=shape, ax=ax,
                           node_color=[G.nodes[n]["color"] for n in nodes])
nx.draw_networkx_labels(G, pos, ax=ax, font_size=9)
ax.axis("off");
```

## Converting between the two

`multinets` converts networkx graphs to igraph behind the scenes with
{meth}`igraph.Graph.from_networkx`. To work in igraph directly, convert your
graph once. The networkx node ids end up in the `_nx_name` vertex attribute:

```{code-cell} ipython3
import igraph as ig

g = ig.Graph.from_networkx(G)
g.vs["_nx_name"], mn.is_multilevel(g, type_attr="bipartite")
```
