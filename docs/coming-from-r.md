# Coming from R

The Python package has the same features as the
[R package](https://github.com/neylsoncrepalde/multinets). Function names are
the same; arguments follow Python's naming style.

## Functions

| R | Python |
|---|---|
| `is_multilevel(x)` | {func}`is_multilevel(x) <multinets.is_multilevel>` |
| `extract_highlevel(x)` | {func}`extract_highlevel(x) <multinets.extract_highlevel>` |
| `extract_lowlevel(x)` | {func}`extract_lowlevel(x) <multinets.extract_lowlevel>` |
| `extract_mesolevel(x)` | {func}`extract_mesolevel(x) <multinets.extract_mesolevel>` |
| `mode_transformation(x, which = "both")` | {func}`mode_transformation(x, which="both") <multinets.mode_transformation>` |
| `layout_multilevel(x, layout = igraph::layout_with_fr)` | {func}`layout_multilevel(x, layout="fr") <multinets.layout_multilevel>` |
| `set_color_multilevel(x, color.true, color.false, V.alpha, E.alpha)` | {func}`set_color_multilevel(x, color_true, color_false, v_alpha, e_alpha) <multinets.set_color_multilevel>` |
| `set_shape_multilevel(x, shape.true, shape.false)` | {func}`set_shape_multilevel(x, shape_true, shape_false) <multinets.set_shape_multilevel>` |
| `data(linked_sim)` | {func}`linked_sim = load_linked_sim() <multinets.load_linked_sim>` |
| `data(linked_sim_matrix)` | {func}`load_linked_sim_matrix() <multinets.load_linked_sim_matrix>` |
| `data(linked_sim_type)` | {func}`load_linked_sim_type() <multinets.load_linked_sim_type>` |
| `plot(x, layout = l)` | {func}`igraph.plot(x, layout=l, target=ax) <igraph.drawing.plot>` |

## Layout algorithms

| R | Python |
|---|---|
| `igraph::layout_with_fr` | `"fr"` |
| `igraph::layout_with_kk` | `"kk"` |
| `igraph::layout_with_drl` | `"drl"` |
| `igraph::layout_in_circle` | `"circle"` |
| `igraph::layout_as_star` | `"star"` |
| `igraph::layout_as_tree` | `"tree"` |
| `igraph::layout_on_grid` | `"grid"` |

A function works too, for example
{meth}`igraph.Graph.layout_kamada_kawai <igraph.GraphBase.layout_kamada_kawai>` or
{func}`networkx.spring_layout <networkx.drawing.layout.spring_layout>`.

## What is different

**Stricter definition of a multilevel network.**
: {func}`~multinets.is_multilevel` checks that there are ties across levels
  and ties within *both* levels; self-loops don't count. The R version only
  looks for ties within the lower level. See
  [](user-guide/multilevel-networks.md).

**No changes in place by default.**
: As in R, {func}`~multinets.set_color_multilevel` and
  {func}`~multinets.set_shape_multilevel` return a modified copy. Pass
  `inplace=True` to modify the graph itself; the function then returns `None`.

**Named projections.**
: `mode_transformation(which="both")` returns a
  {class}`~multinets.Projections` named tuple with `low` and `high` fields
  instead of `list(proj1, proj2)`.

**Layouts.**
: `layout` takes an igraph layout name or a function, and extra keyword
  arguments go to the algorithm. Vertices whose y coordinate is exactly 0 are
  placed on their level, and 3D layouts keep their z coordinate.

**Random numbers.**
: Layout coordinates don't match R's, even with the same seed. python-igraph
  uses Python's {mod}`random` module: call `random.seed()` for reproducible
  layouts.

**Errors.**
: R's `stop()` becomes a `TypeError` (not a graph) or a `ValueError` (not
  bipartite, not multilevel), with the same messages.

**networkx.**
: Every function also accepts networkx graphs. See
  [](user-guide/networkx.md).

**No startup message.**
: Python packages don't print anything when imported.
