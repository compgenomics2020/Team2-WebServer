#!/usr/bin/env python

'''
Welcome to the backbone script of Team-2's Functional Annotation Group.

This script is responsible for calling various functional blocks of
Functional Annotation pipeline.

Input: 	This script takes in a directory of directories of fna/faa/gff files.

Output:	The final output is going to be gff files for Comparative Genomics.
'''
import sys
import os
import random
import subprocess
from shutil import rmtree

import cluster_wrapper


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


def process_in_directory(in_dir):
	'''
	Get an idea of what the directory of directory files look like.
	'''
	#####################Please make sure that all files have a similar naming scheme.#####################

	nag_dirs = os.listdir(in_dir)
	if len(nag_dirs) != 3:
		return False, "Directory is not split into fna/faa/gff subdirectories."

	nag_keys = {'fna', 'faa', 'gff'}
	nag_dict = dict()
	same_files = {}

	for nag in nag_dirs:
		files = os.listdir(in_dir + nag)
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


def run_assemblies(in_dir, out_dir, if_clustering = True):
	'''
	Input:
		in_dir (path of directory of fna/faa/gff directories)
	   	out_dir (path of final merged outputs)
	   	if_clustering (bool to see if clustering is necessary)

	We'll call clustering, ab initio, and homology tools:
		clustering: clustering_wrapper.py
		ab initio: signalp_wrapper.py, pilercr_wrapper.py, tmhmm_wrapper.py
		homology: eggnog_wrapper.py, operon_wrapper.py, vfdb_wrapper.py, card_wrapper.py
	'''

	# Clustering
	if if_clustering:
		try:
			if !(os.path.exists(in_dir + "/fna/all.fna")):
				subprocess.call(["cat " + in_dir + "/fna/*" + " > " + in_dir + "/fna/all.fna"], shell=True)
			if !(os.path.exists(in_dir + "/faa/all.faa")):
				subprocess.call(["cat " + in_dir + "/faa/*" + " > " + in_dir + "/faa/all.faa"], shell=True)
			subprocess.check_output(["python", "cluster_wrapper.py", in_dir, out_dir + "/cdhit"])
			os.remove(in_dir + "/fna/all.fna")
			os.remove(in_dir + "/faa/all.faa")
			print("Finished clustering!\n")
		except:
			print("Clustering failed!\n")
			return False

	# EGGNOG
	try:
		eggnog_dir = "eggnog-mapper" #TODO: make this an input?
		subprocess.check_output(["python2", "eggnog_wrapper.py", eggnog_dir, out_dir + "/cdhit/faa_rep_seq.faa", out_dir + "/eggnog_results"])
	except:
		print("EGGNOG failed!\n")
		return False


	return True



def main(argv, if_clustering = True):
	in_dir = argv[0]
	output_dir = argv[1]

	if os.path.exists(output_dir):
		rmtree(output_dir)
	os.mkdir(output_dir)

	if if_clustering:
		os.mkdir(output_dir + "/cdhit")
	os.mkdir(output_dir + "/eggnog_results")

	return run_assemblies(in_dir, output_dir, if_clustering)


if __name__ == "__main__":
	'''
	For Unit testing the functionality of Functional Annotation group.
	Always make sure that this script is working intact when called specifically.
	'''
	status = main(sys.argv[1:]) #TODO: include clustering bool in sys argv
	print("Final Status: {}".format(status))
