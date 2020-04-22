'''
Wrapper script for Piler-CR, an ab-initio tool for detecting CRISPR spaces and repeats in bacterial genome.

Piler-CR requires contig fasta files as input. We will be using the contig files generated by the Genome Assembly group.

WARNING: Using "gene" sequences will not give the desired results.

'''

#!/usr/bin/env python

import subprocess,os,sys

def pilercr_runner(input_directory_path,contig_file,output_directory_path):

	#Creating file path
	input_file=input_directory_path + contig_file

	#Creating output file
	mod_contig_file_name=contig_file.replace(".fasta","_crispr")
	output_file=output_directory_path+mod_contig_file_name

	#Executing PilerCR
	try:
		print("Running PilerCR for "+contig_file)
		subprocess.check_output(["pilercr", "-in", input_file, "-out",output_file, "-noinfo", "-quiet"])

	except subprocess.CalledProcessError as err:
		print("Error running PilerCR. Check the input files")
		print("Error thrown: "+err.output)
		return False
	print("Completed running PilerCR")
	return True

def main(argv):
	inputpath=argv[0]
	outputpath=argv[1]
	files=os.listdir(inputpath)
	if len(files) == 0:
		print("No files present in the directory.")
		return False
	for name in files:
		result = pilercr_runner(inputpath,name,outputpath)
		if not result:
			return False
	return True

if __name__ == "__main__":
	main(sys.argv[1:])
