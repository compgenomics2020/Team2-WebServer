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

import cluster_wrapper, match_clust_inputs

import card_wrapper

import signalp_wrapper
import pilercr_wrapper
import tmhmm_wrapper


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


def run_annotations(in_dir, out_dir, db_dir, plasmid_dir):
	'''
	Input:
		in_dir (path of directory of fna/faa/gff directories)
	   	out_dir (path of final merged outputs)
	   	use_clustering (bool to see if clustering is necessary)

	We'll call clustering, ab initio, and homology tools:
		clustering: clustering_wrapper.py
		ab initio: signalp_wrapper.py, pilercr_wrapper.py, tmhmm_wrapper.py
		homology: eggnog_wrapper.py, operon_wrapper.py, vfdb_wrapper.py, card_wrapper.py
	'''

	####################
	# Clustering tools #
	####################

	# CD-HIT
	try:
		if not os.path.exists(in_dir + "/fna/all.fna"):
			subprocess.call(["cat " + in_dir + "/fna/*" + " > " + in_dir + "/fna/all.fna"], shell=True)
		if not os.path.exists(in_dir + "/faa/all.faa"):
			subprocess.call(["cat " + in_dir + "/faa/*" + " > " + in_dir + "/faa/all.faa"], shell=True)
		subprocess.check_output(["python", "cluster_wrapper.py", in_dir, out_dir + "/cdhit"])
		os.remove(in_dir + "/fna/all.fna")
		os.remove(in_dir + "/faa/all.faa")
		print("Finished clustering!")
	except:
		print("Clustering failed!")
		return False

	try:
		subprocess.check_output(["python", "match_clust_inputs.py", in_dir, out_dir + "/cdhit"])
		print("Finished matching cluster outputs to individual files!")
	except:
		print("Cluster matching failed!")
		return False


	########################
	# Homology-based tools #
	########################

	# EGGNOG
	try:
        subprocess.check_output(["python2", db_dir + "/eggnog-mapper/emapper.py",
            "-i", out_dir + "/cdhit/faa_rep_seq.faa",
			"--output", out_dir + "/eggnog_results",
            "--data_dir", db_dir + "/eggnog-db", "-m", "diamond", ">", "log", "&"])
    except subprocess.CalledProcessError as err:
        print("Error running EGGNOG.")
        print("Error thrown: " + err.output)
		return False

	# Operons

	# VFDB
	try:
		subprocess.check_output(["blastn", "-db", db_dir + '/vfdb-db/vfdb-db',
			"-query", out_dir + "/cdhit/fna_rep_seq.fna",
			"-out", out_dir + "/vfdb",
			"-max_hsps", "1", "-max_target_seqs", "1",
		    "-outfmt", '"6 qseqid length qstart qend sstart send evalue bitscore stitle"',
			"-perc_identity", "100", "-num_threads", "5"])
	except subprocess.CalledProcessError as err:
        print("Error running VFDB.")
        print("Error thrown: " + err.output)
		return False

	# CARD
	c_result = card_wrapper(out_dir + "/cdhit/faa_rep_seq.faa", plasmid_dir, out_dir + "/card", db_dir + "/card")
	if c_result:
		print("CARD succeeded!")
	else:
		print("CARD failed, check input files.")
		return False

	###################
	# ab initio tools #
	###################

	# SignalP - must be on $PATH
	sp_result = signalp_wrapper.main(input_dir + "/faa/", output_dir + "/signalp/")
	if sp_result:
		print("SignalP succeeded!")
	else:
		print("SignalP failed, check input files.")
		return False

	# PilerCR - must use LDLIBS = -lm when using make, needs fasta files from genome assembly
	pc_result = pilercr_wrapper.main(input_dir + "/fasta/", output_dir + "/pilercr/")
	if pc_result:
		print("PilerCR succeeded!")
	else:
		print("PilerCR failed, check input files.")
		return False

	# TMHMM - must be on $PATH
	tm_result = tmhmm_wrapper.main(input_dir + "/faa/", output_dir + "/tmhmm/")
	if pc_result:
		print("TMHMM succeeded!")
	else:
		print("TMHMM failed, check input files.")
		return False

	print("All tools run!")
	return True



def main(argv, use_clustering = True):
	in_dir = argv[0]
	out_dir = argv[1]
	db_dir = argv[2]
	plasmid_dir = argv[3]

	if os.path.exists(out_dir):
		rmtree(out_dir)
	os.mkdir(out_dir)

	if use_clustering:
		os.mkdir(out_dir + "/cdhit")
	os.mkdir(out_dir + "/eggnog_results")
	os.mkdir(out_dir + "/card")
	os.mkdir(out_dir + "/card/plasmids")
	os.mkdir(out_dir + "/signalp")
	os.mkdir(out_dir + "/pilercr")
	os.mkdir(out_dir + "/tmhmm")

	return run_annotations(in_dir, out_dir, db_dir, plasmid_dir)


if __name__ == "__main__":
	status = main(sys.argv[1:]) #TODO: include clustering bool in sys argv
	print("Final Status: {}".format(status))
