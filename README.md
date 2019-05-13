# Tree Beautifier

- FILE: tree_beautifier.py
- AUTH: ekherman
- DATE: May 13, 2019
- VERS: 1.0

This program accepts a Newick or Nexus tree file and a key file as inputs, and generates new tree file with taxon 
annotations matching those in the key file. It does not discard the original accessions, which can be found in the 
resulting Nexus-formatted .tree output file. 

Usage:

`tree_beautifier.py [-h] [--tree TREE] [--key KEY]`

	-h, --help   show this help message and exit

Required:

	--tree TREE  Newick or Nexus formatted input file
	--key KEY    tab-delimited key file of the structure
			
### Input file structure
Nexus input files are recognized by an initial `#NEXUS` line, while Newick files are recognized
as beginning with an open parenthesis.

See https://en.wikipedia.org/wiki/Newick_format 
and https://en.wikipedia.org/wiki/Nexus_file#Basic_blocks
 for more details and test files for examples. 
 
The key file is a tab-delimited file of the structure
		
	[tree accession]	[annotation]
where the first column contains the node labels in the input tree, and the second column contains
 the desired annotation. 

### Output file structure
A nexus file is generated with the filename [input_basename]_annotated.tre, which can be opened 
in any tree-viewing program (e.g. FigTree)

### Example Usage
The following lines generate annotated Nexus tree files from Newick and Nexus input files, 
respectively.

`python tree_beautifier.py --tree test_newick.txt --key key_file.txt`

`python tree_beautifier.py --tree test_nexus.nxs --key key_file.txt`
