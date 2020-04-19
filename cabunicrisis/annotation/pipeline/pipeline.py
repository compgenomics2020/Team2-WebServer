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
			subprocess.call(["cat", input_directory_path + "/fna/*", ">", "all.fna"])
			subprocess.call(["cat", input_directory_path + "/faa/*", ">", "all.faa"])
			subprocess.check_output(["python", "clustering_wrapper.py", input_directory_path, output_directory_path])
			subprocess.call(["rm", input_directory_path + "/faa/all.faa"])
			subprocess.call(["rm", input_directory_path + "/fna/all.fna"])
		except:
			return False

	for fastq_file_forward, fastq_file_reverse in fastq_files_dict.items():

	return True



def main(essential_arguments = None):
	run_assemblies("./input/", "./output/")

	return True


if __name__ == "__main__":
	'''
	For Unit testing the functionality of Functional Annotation group.
	Always make sure that this script is working intact when called specifically.
	'''
	status = main()
	print("Final Status: {}".format(status))
