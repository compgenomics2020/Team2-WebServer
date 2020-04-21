This is mlst wrapper
### Running MLST

	mlst --csv --legacy --scheme --campylobacter <input_fasta_file> > <mlst_output_csv>

* We use the campylobacter scheme from PubMLST database for running the tool
* Input file format: Contig fasta files
* For our website we have a python wrapper script that checks the input files, output directory and calls MLST on the campylobacter scheme.
 
### Visualising MLST results for the website

#### We have a python scripts that creates a simple visualisation of the mlst results, depicting the STs detected and the sample names belonging to each ST
	python3 mlst_viz.py <mlst_output_csv> <output_directory>
