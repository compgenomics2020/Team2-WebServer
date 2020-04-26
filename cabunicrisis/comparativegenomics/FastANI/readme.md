This is FastANI wrapper
For the fastANI_wrapper.py you can just run it by typing
	
	python fastANI_wrapper.py <input directory pat> <output directory path> <databast path>
	

This script will: first, calculate pairwise anverage nucleitide identity among the samples you offered. Second, compare all the offered genomes to a reference genome and returen the highest ANI value in the reference genome and the taxonomy information of reference genome with highst ANI value. the input directory contains all the contig files you are going to calculate. Those files must be in a fasta format. the ourput directory will be used to store all the results. By default the database path is Campylobacter genome database with ~2000 complete genomes that were downloaded and then mannualy curated.

For the output directory, file with .txt will be used for visualization by running the following code
	
	python fastANI_output_to_distance_matrix.py <three_column_pairwise_ANI_file_from_the_wrapper> >> distance matrix_file_name.txt

For visualize_ANI.py
	
	python FastANI_heatmap.py <distance_matrix_file_name.txt path> <output directory>

This script will generate a heatmap of pairwise ANI vaules.
