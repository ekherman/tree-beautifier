#!/bin/bash
set -e
if [ ! -d test_output ]; then
    mkdir test_output
fi

python tree_beautifier.py --tree test_newick.txt --key key_file.txt
python tree_beautifier.py --tree test_nexus.nxs --key key_file.txt

# output file is originally in main directory
mv test_newick_annotated.tre test_output/
mv test_nexus_annotated.tre test_output/

#compare new output to sample output
new_output=test_output
old_output=sample_output
new_files=($( find $new_output -type f -print0 | perl -ne 'my @files = split(/\0/, $_); foreach(@files) { if (!($_ =~ m/\.svn/)) {print "$_\n";}}'))
for (( i=0; i<${#new_files[@]}; i++ ));
do
    old_file=${old_output}`echo "${new_files[$i]}" | perl -nl -e 's/^[^\/]+//;' -e 'print $_'`
    echo "Comparing ${old_file} to ${new_files[$i]}"
    set +e
    diff -u $old_file ${new_files[$i]}
    if [ $? -eq 0 ]; then
	echo "No differences found"
    fi
    set -e
done