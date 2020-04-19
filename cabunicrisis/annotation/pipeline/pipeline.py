#!/usr/bin/env python

'''
Welcome to the backbone script of Team-2's Functional Annotation Group.

This script is responsible for calling various functional blocks of
Functional Annotation pipeline.

Input: 	This script takes in a directory of directories of fna/faa/gff files.

Output:	The final output is going to be gff files for Comparative Genomics.
'''
import argparse
import multiprocessing
import os
import random
import subprocess

import clustering_wrapper


def check_tool(tool):
	'''
	This function checks if the listed tool required for our pipeline to work is
	present on the system.
	'''
	try:
		#Calling the tool by name supplied.
		bash_output = subprocess.check_output([tool])
	except (FileNotFoundError, subprocess.CalledProcessError) as error:
		print("A tool: {}, was not present on the system. Now quitting...".format(tool))
		return False
	#All is fine.
	return True


def process_input_directory(input_directory_path):
	'''
	Get an idea of what the directory of directory files look like.
	'''
	#####################Please make sure that all files have a similar naming scheme.#####################

	nag_dirs = os.listdir(input_directory_path)
	if len(nag_dirs) != 3:
		return False, "Directory is not split into fna/faa/gff subdirectories."

	nag_keys = {'fna', 'faa', 'gff'}
	nag_dict = dict()
	same_files = {}

	for nag in nag_dirs:
		files = os.listdir(input_directory_path + nag)
		file_exts = set([file[file.index('.'):] for file in files])
		if len(file_exts) > 1:
			print("Too many file types present in a single directory.")
			return False, "Too many file types present in a single directory."
		elif len(file_exts) == 0:
			print("No files present in the directory.")
			return False, "No files present in the directory."
		else:
			nag_dict[file_exts[0]] = nag

		# checks if the same file naming scheme exists among fna/faa/gff directories
		if not same_files:
			same_files = set([file[0:file.index('.')] for file in files])
		else:
			nag_file_names = set([file[0:file.index('.')] for file in files])
			if nag_file_names != same_files:
				return False, "The naming scheme in each subdirectory is not consistent."

	return True, nags_dict


def run_assemblies(input_directory_path, output_directory_path, if_clustering = True):
	'''
	Input:
		input_directory_path (path of directory of fna/faa/gff directories)
	   	output_directory_path (path of final merged outputs)
	   	if_clustering (bool to see if clustering is necessary)

	We'll call clustering, ab initio, and homology tools:
		clustering: clustering_wrapper.py
		ab initio: signalp_wrapper.py, pilercr_wrapper.py, tmhmm_wrapper.py
		homology: eggnog_wrapper.py, operon_wrapper.py, vfdb_wrapper.py, card_wrapper.py
	'''

	if if_clustering:
		try:
			subprocess.check_output(["python", "clustering_wrapper.py", input_directory_path, output_directory_path])
		except:
			return False

	for fastq_file_forward, fastq_file_reverse in fastq_files_dict.items():

	return True



def main(essential_arguments = None):
	parser = argparse.ArgumentParser()

	#Arguments added for an input-directory and output-directory.
	parser.add_argument("-i", "--input-directory", help="Path to a directory that contains input fastq files.", required=False)
	parser.add_argument("-o", "--output-directory", help="Path to a directory that will store the output files.", required=False)

	#Argument for Kmers.
	parser.add_argument("-ka", "--kmer-abyss", help="Kmer value for abyss.", required=False)
	parser.add_argument("-ks", "--kmer-spades", help="Kmer value for spades.", required=False)
	parser.add_argument("-km", "--kmer-masurca", help="Kmer value for MaSuRCA.", required=False)
	parser.add_argument("-ku", "--kmer-unicycler", help="Kmer value for Unicycler.", required=False)
	parser.add_argument("-kv", "--kmer-velvet", help="Kmer value for Velvet.", required=False)
	#parser.add_argument("-ka", "--kmer-abyss", help="Kmer value for abyss.", required=False)

	parser.add_argument("-r", "--replace-output-files", help="Replace the output files that are already present. Currently not supported.", required=False, action="store_true")

	#Parsing the arguments.
	args = vars(parser.parse_args())

	if essential_arguments:

	else:
		input_directory_path_for_fastq_files = args['input_directory']
		output_directory_path = args['output_directory']
	replace_files_flag = args['replace_output_files']

	#Parse Kmers for assembly tools.
	#Most of our tools run on a Debuign graph based methods.
	#They need kmer values.
	kmer_spades = args['kmer_spades']
	kmer_dict['spades'] = 'auto'
	###########################################Parsing Documents Ends#############################################
	##############################################################################################################

	#Check if directories exist.
	if not os.path.exists(input_directory_path_for_fastq_files) and	not os.path.exists(output_directory_path):
		return False, "Input and Output directories do not exist."

	#Check if all the tools are present. Either the tool should be present in the PATH variable
	#or the bioinformatician should make sure that a proper path to their tool is sent.
	#Pipeline cannot work without tools.
	status_check_tools = check_tools()

	if not status_check_tools:
		return False, "Tools asked for by the Genome Assembly weren't present on the system."

	#########################################Check Directories Ends###############################################
	##############################################################################################################

	#Checks completed. Parse through input directories to see how fastq files are doing.
	#Get information of input files.
	status_process_input_directory, return_output_process_input_directory = process_input_directory(input_directory_path_for_fastq_files)

	if not status_process_input_directory:
		return False, return_output_process_input_directory

	fastq_files_dict = return_output_process_input_directory[1]

	#Read Manifest file. Manifest file has information of pre-trim and post-trim files.
	#Don't change the names of manifest files. This code expects them to be in tmp.

	#Reading manifest files.

	pre_trim_manifest = None
	post_trim_manifest = None

	#pre_trim_manifest, post_trim_manifest = get_manifest_files()

	#######################################Reading Manifest files Ends############################################
	##############################################################################################################


	print("Found {} file pairs in the input directory.\n".format(len(fastq_files_dict)))
	#################Quality Checks#################
	print("Started pre-assembly quality check.")

	#Kristine

	print("Completed quality check.\n")

	#################Passing data over to Genome Assembly Tools#################
	print("Now running genome assembly tools.")
	status_run_assemblies = run_assemblies(input_directory_path_for_fastq_files, output_directory_path, fastq_files_dict, kmer_dict, pre_trim_manifest, post_trim_manifest)

	if not status_run_assemblies:
		print("Running assembly tools failed")
		return False

	print("Completed genome assembly tools.\n")
	#################Post Assembly Quality Check#################

	print("Starting with post assembly quality check tools.")
	print("Starting Quast")

	#quast_output = quast_runner(output_directory_path)

	return True


if __name__ == "__main__":
	'''
	For Unit testing the functionality of Genome Assembly group.
	Always make sure that this script is working intact when called specifically.
	'''
	status = main()
	print("Final Status: {}".format(status))
