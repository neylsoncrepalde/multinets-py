---
file_format: mystnb
kernelspec:
  name: python3
---

# Multilevel networks

## The linked design

A multilevel network, following the *linked design* of Lazega et al. (2008),
has **two kinds of vertices**:

- vertices on the **lower level**, usually individuals;
- vertices on the **higher level**, usually organizations, collectivities or
  other joint social structures.

It also has **two kinds of edges**:

- ties between vertices of the **same level**: individuals with individuals,
  organizations with organizations;
- ties between vertices of **different levels**: individuals affiliated to
  organizations. These are *affiliation* ties.

Put another way, a multilevel network is a bipartite (2-mode) network that also
has ties between vertices within each level.

## Levels are a vertex attribute

As in igraph, the level of each vertex is stored in a boolean vertex attribute
called `type`: `True` for the higher level and `False` for the lower level.
This is what {meth}`igraph.Graph.Bipartite` creates, and what
{meth}`igraph.Graph.bipartite_projection` reads.

Let's build a small network with three people and two firms:

```{code-cell} ipython3
import igraph as ig
from multinets import is_multilevel

g = ig.Graph()
g.add_vertices(["ana", "bruno", "carla", "firm1", "firm2"])
g.vs["type"] = [False, False, False, True, True]
g.add_edges([
    ("ana", "bruno"), ("bruno", "carla"),                     # between people
    ("firm1", "firm2"),                                       # between firms
    ("ana", "firm1"), ("bruno", "firm1"), ("carla", "firm2"), # affiliations
])
is_multilevel(g)
```

## What makes a network multilevel

{func}`~multinets.is_multilevel` returns `True` when the graph:

1. is bipartite: it has a `type` vertex attribute with a boolean value for every
   vertex (`0` and `1` are accepted too);
2. has at least one tie across levels;
3. has at least one tie between two vertices of the higher level, **and** at
   least one between two vertices of the lower level. Self-loops don't count.

Without the ties inside the levels, the same people and firms form a plain
2-mode (affiliation) network:

```{code-cell} ipython3
affiliation = g.copy()
affiliation.delete_edges([("ana", "bruno"), ("bruno", "carla"), ("firm1", "firm2")])
is_multilevel(affiliation)
```

A graph without a `type` attribute is not bipartite at all, and that's an error:

```{code-cell} ipython3
:tags: [raises-exception]

is_multilevel(ig.Graph.Famous("Zachary"))
```

:::{note}
{meth}`igraph.Graph.is_bipartite() <igraph.GraphBase.is_bipartite>` answers a
different question: can the vertices be split into two groups with no edges
inside the groups? A multilevel network has ties inside its levels, so it is
usually *not* bipartite in that sense. `multinets` only looks at the `type`
attribute, as the R version of igraph does.
:::

## Another attribute name

Every function takes a `type_attr` argument if the levels are stored under
another name. networkx, for example, uses `bipartite`:

```{code-cell} ipython3
g.vs["level"] = g.vs["type"]
del g.vs["type"]
is_multilevel(g, type_attr="level")
```

## Errors

| Problem | Exception | Message |
|---|---|---|
| Not an igraph or networkx graph | `TypeError` | `Not a graph object` |
| No `type` attribute | `ValueError` | `Data is not bipartite` |
| A vertex without a boolean `type` | `ValueError` | `Vertex attribute 'type' must be boolean ...` |
| A function that needs a multilevel network gets something else | `ValueError` | `The network is not multilevel` |
