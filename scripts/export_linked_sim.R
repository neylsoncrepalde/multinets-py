# Regenerates src/multinets/data/linked_sim.graphml from the R package data.
# Run from the root of the R multinets repository:
#   Rscript /path/to/multinets-py/scripts/export_linked_sim.R /path/to/multinets-py
args <- commandArgs(trailingOnly = TRUE)
out_dir <- file.path(args[1], "src", "multinets", "data")

load("data/linked_sim.rda")
g <- igraph::upgrade_graph(linked_sim)
igraph::write_graph(g, file.path(out_dir, "linked_sim.graphml"), format = "graphml")
