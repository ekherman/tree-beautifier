#!/usr/bin/python

# This program takes a .tree file (which can be a single line in Newick format, or a saved FigTree tree file), and
# annotates the leaves using a tab-delimited key file of the structure [tree accession] [annotation]. It does not
# discard the tree accession, so this information can be found in the resulting .tree output file.

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    "--tree",
    type=str,
    help="Newick or Nexus formatted input file",
)
parser.add_argument(
    "--key",
    type=str,
    help="tab-delimited key file of the structure [tree accession] [annotation]",
)

if len(sys.argv) < 4:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

# Open input tree file
input_tree = [line.rstrip('\n') for line in open(args.tree)]

# Check that input file format is correct (either starts with "(" or "#NEXUS")
file_fmt = ''
nexus_input = []
newick_input = ''
if input_tree[0].startswith('('):
    newick_input = input_tree[0]
    file_fmt = 'newick'
elif input_tree[0].startswith('#'):
    file_fmt = 'nexus'
    # Get number of accessions
    dim_line = input_tree[2].lstrip("\t")
    dim_line = dim_line.rstrip(';')
    dimension = int(dim_line.replace("dimensions ntax=", ''))
else:
    print("Input file is not in Newick or Nexus format\n")

# Open key file
with open(args.key, 'r') as key_file:
    rows = (line.split('\t') for line in key_file)
    key_dict = {entry[0]: entry[1].rstrip('\n') for entry in rows}
key_file.close()

# Name output file
file_ends = ['.txt', '.tre', '.tree', '.nex', '.nxs']
output_name = 'output_tree_annotated.tre'
for ending in file_ends:
    if args.tree.endswith(ending):
        output_name = args.tree.replace(ending, '_annotated.tre')


# Add annotations and write to output file
if file_fmt == 'newick':
    # Write nexus output file
    with open(output_name, 'w') as output_file:
        dict_size = int(len(key_dict))
        output_file.write('#NEXUS\n'
                          'begin taxa;'
                          '\n\tdimensions ntax=' + str(dict_size) +
                          ';\n\ttaxlabels\n')
        for key in key_dict:
            new_name = "'" + key + "'" + '[&!name="' + key_dict[key] + '"]'
            output_file.write('\t' + new_name + '\n')
        output_file.write(';\nend;\n\nbegin trees;\n\ttree tree_1 = ')
        output_file.write(input_tree[0] + '\n')
        output_file.write('end;\n\n')
    output_file.close()
elif file_fmt == 'nexus':
    output_rows = []
    file_range = len(input_tree) - 1
    lineno = 0
    with open(output_name, 'w') as output_file:
        while lineno <= 3:
            output_file.write(input_tree[lineno] + '\n')
            lineno += 1
        while lineno <= (dimension + 3):
            current_line = input_tree[lineno]
            accession_clean = current_line.lstrip("\t")
            accession_clean = accession_clean.rstrip("\n")
            accession_clean = accession_clean.strip("'")
            new_name = current_line + '[&!name="' + key_dict[accession_clean] + '"]'
            output_file.write(new_name + '\n')
            lineno += 1
        while lineno <= file_range:
            output_file.write(input_tree[lineno] + '\n')
            lineno += 1
    output_file.close()
else:
    print("Something went wrong!\n")
