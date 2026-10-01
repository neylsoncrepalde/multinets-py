"""multinets: Multilevel Network Analysis.

Analyze multilevel networks as described in Lazega et al. (2008)
<doi:10.1016/j.socnet.2008.02.001> and in Lazega and Snijders (2016,
ISBN:978-3-319-24520-1). Built as an extension to igraph; networkx graphs are
supported too.
"""

from importlib.metadata import version

from .datasets import load_linked_sim, load_linked_sim_matrix, load_linked_sim_type
from .layout import layout_multilevel
from .multilevel import (
    extract_highlevel,
    extract_lowlevel,
    extract_mesolevel,
    is_multilevel,
)
from .projection import Projections, mode_transformation
from .style import set_color_multilevel, set_shape_multilevel

__version__ = version("multinets")  # Set in setup.py.

__all__ = [
    "Projections",
    "extract_highlevel",
    "extract_lowlevel",
    "extract_mesolevel",
    "is_multilevel",
    "layout_multilevel",
    "load_linked_sim",
    "load_linked_sim_matrix",
    "load_linked_sim_type",
    "mode_transformation",
    "set_color_multilevel",
    "set_shape_multilevel",
]
