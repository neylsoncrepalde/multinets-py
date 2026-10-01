---
file_format: mystnb
kernelspec:
  name: python3
---

# Analyzing each level

A multilevel network can be split into three networks, one per level of
analysis. The examples use `linked_sim`, a simulated multilevel network with
100 individuals and 50 organizations:

```{code-cell} ipython3
from multinets import load_linked_sim

linked_sim = load_linked_sim()
print(linked_sim.summary())
```

## The higher and lower levels

{func}`~multinets.extract_highlevel` keeps the higher level vertices and the
ties between them. {func}`~multinets.extract_lowlevel` does the same for the
lower level. Both return 1-mode networks:

```{code-cell} ipython3
from multinets import extract_highlevel, extract_lowlevel

organizations = extract_highlevel(linked_sim)
individuals = extract_lowlevel(linked_sim)

for name, level in [("organizations", organizations), ("individuals", individuals)]:
    print(f"{name}: {level.vcount()} vertices, {level.ecount()} ties")
```

They are regular igraph graphs, ready for any other analysis:

```{code-cell} ipython3
print("density of the organizations network:", round(organizations.density(), 3))
print("density of the individuals network:  ", round(individuals.density(), 3))
```

## The meso level

{func}`~multinets.extract_mesolevel` keeps *all* the vertices but only the ties
across levels. The literature also calls this an *affiliation* network. It is
a bipartite (2-mode) network:

```{code-cell} ipython3
from multinets import extract_mesolevel

affiliations = extract_mesolevel(linked_sim)
print(affiliations.vcount(), "vertices,", affiliations.ecount(), "affiliation ties")
```

## From 2-mode to 1-mode

{func}`~multinets.mode_transformation` projects a bipartite network onto each
of its levels:

- two organizations are tied when they share at least one individual;
- two individuals are tied when they are affiliated to the same organization.

With the default `which="both"`, it returns a
{class}`~multinets.Projections` named tuple with a `low` and a `high` network:

```{code-cell} ipython3
from multinets import mode_transformation

transformed = mode_transformation(affiliations)
print("low: ", transformed.low.summary())
print("high:", transformed.high.summary())
```

The `weight` edge attribute counts how many vertices a pair shares. For
example, these are the pairs of organizations that share the most individuals:

```{code-cell} ipython3
high = transformed.high
top = sorted(high.es, key=lambda e: e["weight"], reverse=True)[:5]
for edge in top:
    print(f"{edge.source} and {edge.target} share {edge['weight']} individuals")
```

Use `which="high"` or `which="low"` to get a single network:

```{code-cell} ipython3
high_transformed = mode_transformation(affiliations, which="high")
high_transformed.vcount()
```

Projections only make sense for a 2-mode network, so a multilevel network is
refused. Extract its meso level first:

```{code-cell} ipython3
:tags: [raises-exception]

mode_transformation(linked_sim)
```
