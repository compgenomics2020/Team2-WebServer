This is kSNP wrapper
#### Run MakeFasta with text file as input and name of output file to concatenate all inputs to a single fasta
	MakeFasta <input_file.txt> <output_file.fasta>
#### Run Kchooser on generated fasta file
	Kchooser <all_genomes.fasta>
#### If optimal K is 31, the`n K likely plateaued at a specific percentage. Check Kchooser.report and rerun with asymptotic percentage as cutoff (ex. 95.8%)
	Kchooser <all_genomes.fasta> 0.958
### Creating phylogenetic tree
	kSNP3 -in <input_file> -k 25 -outdir <output_directory> -ML 
  
Then visualize the output file

     python3 make_phylogeny.py <path/to/input_file.tre> </path/to/output/location>
     
Please import required packages prior to usage.
