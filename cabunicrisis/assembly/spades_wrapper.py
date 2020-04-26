#!/usr/bin/env python

import subprocess
import os

def spades_runner(fastq_file_forward, fastq_file_reverse, input_directory_path, output_directory_path, kmer):
	#Create file paths.
	fastq_file_forward_path = os.path.join(input_directory_path, fastq_file_forward)
	fastq_file_reverse_path = os.path.join(input_directory_path, fastq_file_reverse)

	#Creating a directory inside output directory.
	output_subdir_name = fastq_file_forward.split('.')[0].split('_')[0]
	output_subdir_path = output_directory_path.rstrip('/') + '/' + output_subdir_name 

	#Check if subdir is already there.
	if not output_subdir_name in os.listdir(output_directory_path):
		os.mkdir(output_subdir_path)

	#Execute SPAdes.
	try:
		print("Running spades for {} and {}".format(fastq_file_forward, fastq_file_reverse))
		if kmer == "auto":
			#SPAdes running in auto mode.
			bash_output = subprocess.check_output(["spades.py", "--careful", "--only-assembler", "-1", fastq_file_forward_path, "-2", fastq_file_reverse_path, "-o", output_subdir_path])
		else:
			#SPAdes in custom kmer mode.
			bash_output = subprocess.check_output(["spades.py", "--careful", "--only-assembler", "-1", fastq_file_forward_path, "-2", fastq_file_reverse_path, "-k", kmer ,"-o", output_subdir_path])

	except subprocess.CalledProcessError:
		print("SPAdes could not finish the assembly. Please check the files.")
		return False

	print("Successfully ran spades for {} and {}".format(fastq_file_forward, fastq_file_reverse))
	return True


if __name__ == "__main__":
	#spades_runner()
	pass
