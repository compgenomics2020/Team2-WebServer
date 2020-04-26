
'''
Welcome to the backbone script of Team-2's Functional Annotation Group.

This script is responsible for calling various functional blocks of
Functional Annotation pipeline.

Input: 	This script takes in a directory of directories of fna/faa/gff files.

Output:	The final output is going to be gff files for Comparative Genomics.
'''
import sys
import os
import subprocess
from shutil import rmtree

from .signalp_wrapper import main as sp_main
from .pilercr_wrapper import main as pc_main
from .tmhmm_wrapper import main as tm_main


def process_in_directory(file_list, input_dir):
	'''
	Checks if there are the same number of fna/faa/gff files, if the naming
	schemes are consistent, and only then sort each into its own directory.

	CURRENTLY ASSUMES that the input is a list of file paths, so I can move them
	using os.move.
	'''

	fna_files = filter(lambda file: os.path.splitext(file)[1] == ".fna", file_list)
	fna_list_length = len(fna_files)
	fna_names = set([os.path.splitext(file)[0] for file in fna_files])
	if len(fna_names) < fna_list_length:
		return False, "there are duplicate fna files in your input"

	faa_files = filter(lambda file: os.path.splitext(file)[1] == ".faa", file_list)
	faa_list_length = len(faa_files)
	faa_names = set([os.path.splitext(file)[0] for file in faa_files])
	if len(faa_names) < faa_list_length:
		return False, "there are duplicate faa files in your input"

	gff_files = filter(lambda file: os.path.splitext(file)[1] == ".gff", file_list)
	gff_list_length = len(gff_files)
	gff_names = set([os.path.splitext(file)[0] for file in gff_files])
	if len(gff_names) < gff_list_length:
		return False, "there are duplicate gff files in your input"

	if (gff_list_length != fna_list_length) or (fna_list_length != faa_list_length):
		return False, "the number of fna, faa, and gff files are inconsistent"

	if (gff_names != fna_names) or (fna_names != faa_names):
		return False, "the naming schemes of your fna, faa, and gff files are inconsistent"

	# we made sure all inputs are consistent - make directories.
	if os.path.exists(input_dir):
		rmtree(input_dir)
	os.mkdir(input_dir)

	os.mkdir(os.path.join(input_dir, "fna"))
	[os.move(file, os.path.join(input_dir, "fna", file.split("/")[-1])) for file in fna_files]

	os.mkdir(os.path.join(input_dir, "faa"))
	[os.move(file, os.path.join(input_dir, "faa", file.split("/")[-1])) for file in faa_files]

	os.mkdir(os.path.join(input_dir, "gff"))
	[os.move(file, os.path.join(input_dir, "gff", file.split("/")[-1])) for file in gff_files]

	return True, 3 * faa_list_length


def run_annotations(in_dir, out_dir, db_dir):
	'''
	Input:
		in_dir (path of directory of fna/faa/gff directories)
	   	out_dir (path of final merged outputs)
	   	use_clustering (bool to see if clustering is necessary)

	We'll call clustering, ab initio, and homology tools:
		clustering: clustering_wrapper.py
		ab initio: signalp_wrapper.py, pilercr_wrapper.py, tmhmm_wrapper.py
		homology: eggnog_wrapper.py, vfdb_wrapper.py, card_wrapper.py
	'''

	# ####################
	# # Clustering tools #
	# ####################

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

	# VFDB
	try:
		os.system("blastn -db "+ db_dir + '/vfdb/vfdb'+
			" -query "+ out_dir + "/cdhit/fna_rep_seq.fna"+
			" -out "+ out_dir + "/vfdb"+
			" -max_hsps 1 -max_target_seqs 1 -outfmt '6 qseqid length qstart qend sstart send evalue bitscore stitle' -perc_identity 100 -num_threads 5")
		print("Finished VFDB!")
	except:
		print("Error running VFDB.")
		return False

	# EGGNOG
	try:
		subprocess.check_output(["python2", db_dir + "/eggnog-mapper/emapper.py",
	        "-i", out_dir + "/cdhit/faa_rep_seq.faa", "--output", out_dir + "/eggnog",
			"--data_dir", db_dir + "/eggnog-db", "-m", "diamond"])
	except subprocess.CalledProcessError as err:
		print("Error running EGGNOG.")
		print("Error thrown: " + err.output)
		return False

	###################
	# ab initio tools #
	###################

	# SignalP - must be on $PATH
	sp_result = sp_main([in_dir + "/faa/", out_dir + "/signalp/"])
	if sp_result:
		print("SignalP succeeded!")
	else:
		print("SignalP failed, check input files.")
		return False

	# # PilerCR - must use LDLIBS = -lm when using make, needs fasta files from genome assembly
	# pc_result = pc_main([in_dir + "/fasta/", out_dir + "/pilercr/"])
	# if pc_result:
	# 	print("PilerCR succeeded!")
	# else:
	# 	print("PilerCR failed, check input files.")
	# 	return False

	# TMHMM - must be on $PATH
	tm_result = tm_main([in_dir + "/faa/", out_dir + "/tmhmm/"])
	if tm_result:
		print("TMHMM succeeded!")
	else:
		print("TMHMM failed, check input files.")
		return False

	print("All tools ran!")


	#######################
	# Merging annotations #
	#######################

	subprocess.check_output(["python", "create_homology_gff.py",
		out_dir + "/vfdb", out_dir + "/eggnog.emapper.annotations",
		out_dir + "/cdhit/faa_rep_seq.faa",
		out_dir + "/cdhit/faa_cluster_membership.txt"])

	subprocess.check_output(["python", "create_abinitio_gff.py",
		out_dir + "/tmhmm/", out_dir + "/signalp/"])

	subprocess.check_output(["python", "merging_annotations.py",
		"./tmp", out_dir + "/final"])
	print("Everything merged!")


	################
	# Making plots #
	################

	subprocess.check_output(["python", "generate_plots.py",
		"./tmp", out_dir + "/plots"])
	print("Everything plotted!")

	os.remove("Clust2")
	rmtree("tmp")
	return True



def main(argv, use_clustering = True):
	in_dir = argv[0]
	out_dir = argv[1]
	db_dir = argv[2]

	if os.path.exists(out_dir):
		rmtree(out_dir)
	os.mkdir(out_dir)

	os.mkdir(out_dir + "/cdhit")
	# os.mkdir(out_dir + "/card")
	os.mkdir(out_dir + "/signalp")
	# os.mkdir(out_dir + "/pilercr")
	os.mkdir(out_dir + "/tmhmm")
	os.mkdir(out_dir + "/final")
	os.mkdir(out_dir + "/plots")

	if os.path.exists("tmp"):
		rmtree("tmp")
	os.mkdir("tmp")

	return run_annotations(in_dir, out_dir, db_dir)


if __name__ == "__main__":
	status = main(sys.argv[1:])
	print("Final Status: {}".format(status))
