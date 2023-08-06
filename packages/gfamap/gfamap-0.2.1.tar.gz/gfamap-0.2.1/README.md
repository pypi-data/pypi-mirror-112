## gfamap

*gfamap* is a programme intended for exploration of assembly graphs. 
It annotates assembly graphs by mapping edges of a genome / metagenome 
assembly graph to a reference genome database.

### Requirements

*gfamap* requires [*minimap2*](https://github.com/lh3/minimap2) be on PATH.

### Installation

*gfamap* can be installed using pip:

```
pip install gfamap
gfamap --help
```
### Basic usage

*gfamap* requires three mandatory inputs:

* Edges: comma-separated names of edges in the assembly graph to be mapped 
* Assembly graph: path to an assembly graph in GFA format
* Reference genome: path to a reference genome / genome database

The selected edges are extracted from the assembly graph and converted to 
a fasta file, which is then mapped to the given reference genome database. 
The alignments generated are returned in the form of a SAM file. 
Additionally, the edges of the assembly graph with valid mappings are 
annotated, and an annotated GFA file is returned. 
