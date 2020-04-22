#!/usr/bin/env python

'''
Welcome to the backbone script of Team-2's Genome Assembly Group.

This script is responsible for calling various functional blocks of
Genome Assembly pipeline.

Input: 	This script takes in Input fastq files. We expect paired-end or single-end libraries.
		Ideally we should generalize more, for mate-pairs and sequencing instrument information and what not.
		But we're focusing on basic functionality right now.

Output:	-	The final output is going to be Genome Assembly contigs for respective read files given. For paired-end libraries,
			one can expect 1 contig file for every file pair.
		-	We're also going to send the organism name to the next group in the main pipeline.
		-	There are also intermediate output that we are generating, we'll be sending them to the web server people
			to display thing if needed.
'''

import argparse
import multiprocessing
import os
import random
import subprocess

from .spades_wrapper import spades_runner
from .quast_wrapper import quast_runner
from .plasmid_spades_wrapper import plasmid_spades_runner

from .models import GenomeAssembly

#############################Globals#############################

#Please do not change or add keys in the following dictionary.
#Please do not use direct_paths unless you have to.
genome_assembly_tools = {'in_path_variable': [], 'direct_paths': []}

#Variable values as desired by other members.

default_kmer_values = {'abyss': 'auto', 'spades': 'auto', 'masurca': 'auto', 'unicycler': 'auto', 'velvet': '91'}

###########################Globals End############################


def check_tools():
	'''
	This function checks if all the tools required for our pipeline to work.
	It uses the 'genome_assembly_tools' global dictionary to see if everything is all right. 
	'''
	for tool_name in genome_assembly_tools['in_path_variable']:
		try:
			#Calling the tool by name supplied.
			bash_output = subprocess.check_output([tool_name])
		except (FileNotFoundError, subprocess.CalledProcessError) as error:
			print("A tool: {}, was not present on the system. Now quitting...".format(tool_name))
			return False

	for tool_path in genome_assembly_tools['direct_paths']:
		try:
			#Calling the tool by name supplied.
			bash_output = subprocess.check_output([tool_path])
		except (FileNotFoundError, subprocess.CalledProcessError) as error:
			print("A tool with path: {}, was not present on the system. Now quitting...".format(tool_name))
			return False		

	#All is fine.
	return True


def process_input_directory(input_directory_path):
	'''
	Get an idea of what fastq files look like.
	The logic assumes files to be written as: CGT2049_1.fq, CGT2049_2.fq or CGT2049_1.fq.gz, ...
	'''
	#####################Please make sure that all files have a similar naming scheme.#####################

	files = os.listdir(input_directory_path)
	
	#Check if directory is empty.
	if len(files) == 0:
		print("No files present in the directory.")
		return False, "No files present in the directory."

	#Check if at least one fastq file is present.
	fastq_files = [file_name for file_name in files if file_name.endswith("fastq") or file_name.endswith("fq")]
	
	#See if they are paired or single. Seperate paired from single as well.
	#This dict looks like: {'CGT2049_1.fq':	'CGT2049_2.fq'}

	#Shuffle the read files.
	random.shuffle(fastq_files)
	fastq_files_dict = {}

	#The for loop below creates the above dict.
	for file_name in fastq_files:
		#Get the prefix name of file.
		if '_1' in file_name or '_2' not in file_name:
			fastq_files_dict[file_name] = None

	for file_name_1 in list(fastq_files_dict.keys()):
		if file_name_1.replace('_1', '_2') in files:
			fastq_files_dict[file_name_1] = file_name_1.replace('_1', '_2')

	if None not in (fastq_files_dict.values()):
		#All reads are paired.
		return True, ['paired', fastq_files_dict]

	else:
		#One or more reads are Single-pair.
		return True, ['single', fastq_files_dict]


def get_manifest_files():
	'''
	Manifest files contain information of length of reads contained in fastq files given as 
	input data.
	It's a two cloumn file, with first as name and second as length of reads.
	'''
	pre_trim_manifest_file_path = "tmp/pre_trim_manifest.tsv"
	post_trim_manifest_file_path = "tmp/pre_trim_manifest.tsv"

	pre_trim_manifest = {}
	post_trim_manifest = {}

	with open(pre_trim_manifest_file_path) as f:
		raw = f.read()

	rows = raw.rstrip('\n').split('\n')

	for row in rows:
		pre_trim_manifest[row.split('\t')[0]] = row.split('\t')[1]

	#Repeating the same task for similar post trim file.
	'''
	with open(post_trim_manifest_file_path) as f:
		raw = f.read()

	rows = raw.rstrip('\n').split('\n')

	for row in rows:
		post_trim_manifest[row.split('\t')[0]] = row.split('\t')[1]	
	'''
	return pre_trim_manifest, None


def check_already_done(fastq_file_forward, output_directory):
	'''
	This function looks in the output directory to see if the fastq file (pairs)
	have already been processed.
	'''
	directories = os.listdir(output_directory)
	if fastq_file_forward.split('.')[0].split('_')[0] in directories:
		return True
	else:
		return False



def run_assemblies(input_directory_path, output_directory_path, fastq_files_dict, kmer_dict, model_object_user):
	'''
	We'll call 3 assembly tools, parallely
	'''
	parallel_manager = multiprocessing.Manager()
	status_returned = parallel_manager.dict()

	#print(pre_trim_manifest)

	#Assembly flags, put these to False if you want to NOT RUN a particular tool.
	if_spades = True
	if_plasmid = False

	#Output directory paths.
	output_spades_path = output_directory_path.rstrip('/') + '/' + 'spades'
	output_plasmid_spades_path = output_directory_path.rstrip('/') + '/' + 'plasmid_spades' + '/' 


	#Refer: https://stackoverflow.com/questions/10415028/how-can-i-recover-the-return-value-of-a-function-passed-to-multiprocessing-proce
	for fastq_file_forward, fastq_file_reverse in fastq_files_dict.items():
		#Check if foward has an _1 as a suffix.
		if '_1' in fastq_file_forward:
			#Getting the fastq file objects.
			model_object_raw_fastq_file =  model_object_user.raw_files.all().filter(path__icontains = fastq_file_forward)[0]

			##########################################
			################Tools Start###############
			##########################################


			##################SPAdes##################
			if if_spades:
				#Create directory for SPAdes' results.			
				if not os.path.exists(output_spades_path):
					os.mkdir(output_spades_path)

				#Check if the file has already been processed using SPAdes.
				if check_already_done(fastq_file_forward, output_spades_path):
					#print("\nFiles {} & {} have already been processed by SPAdes.".format(fastq_file_forward, fastq_file_reverse))
					#print("If you want to process it again, please delete the directory: {} in directory: {}".format(fastq_file_forward.split('.')[0].split('_')[0], output_spades_path))
					#print("Skipping for now...\n")
					continue

				else:
					#print("Running SPAdes for {} & {}.".format(fastq_file_forward, fastq_file_reverse))
					contigs_file_path = output_spades_path + '/' + fastq_file_forward.split('_')[0] + '/' + 'contigs.fasta'
					model_object_genome_assembly = model_object_user.assembly.all()[0]
					spades_output = spades_runner(fastq_file_forward, fastq_file_reverse, input_directory_path, output_spades_path, kmer_dict['spades']) 

					#Check if SPAdes ran fine.
					if spades_output is not True or None:
						print("SPAdes process failed for reads: {} and {}".format(fastq_file_forward, fastq_file_reverse))
					
					#Job is completed, updating it in the database.
					model_object_genome_assembly.job_status = True
					model_object_genome_assembly.save()
			##########################################


			##############Plasmids SPAdes#############
			if if_plasmid:
				#Create directory for SPAdes' results.			
				if not os.path.exists(output_plasmid_spades_path):
					os.mkdir(output_plasmid_spades_path)

				#Check if the file has already been processed using SPAdes.
				if check_already_done(fastq_file_forward, output_plasmid_spades_path):
					#print("\nFiles {} & {} have already been processed by plasmid-SPAdes.".format(fastq_file_forward, fastq_file_reverse))
					#print("If you want to process it again, please delete the directory: {} in directory: {}".format(fastq_file_forward.split('.')[0].split('_')[0], output_plasmid_spades_path))
					#print("Skipping for now...\n")
					continue

				else:
					#print("Running SPAdes for {} & {}.".format(fastq_file_forward, fastq_file_reverse))
					
					plasmid_spades_output = plasmid_spades_runner(fastq_file_forward, fastq_file_reverse, input_directory_path, output_plasmid_spades_path, "auto") 

					#Check if SPAdes ran fine.
					if plasmid_spades_output is not True or None:
						print("plasmid-SPAdes process failed for reads: {} and {}".format(fastq_file_forward, fastq_file_reverse))
			##########################################


			##########################################
			#################Tools END################
			##########################################
			
	return True



def main(essential_arguments = None):
	#Getting the arguments.	
	#Directories.
	input_directory_path_for_fastq_files = essential_arguments['input_directory']
	output_trimmed_files = essential_arguments['output_trimmed_files']
	output_genome_assembly = essential_arguments['output_genome_assembly']
	output_quast = essential_arguments['output_quast']

	#Model Objects.
	model_object_user = essential_arguments['model_objects']['user']

	kmer_dict = {'spades': 'auto'}
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


	#print("Found {} file pairs in the input directory.\n".format(len(fastq_files_dict)))
	#################Quality Checks#################
	#print("Started pre-assembly quality check.")

	#Kristine

	#print("Completed quality check.\n")

	#################Passing data over to Genome Assembly Tools#################
	#print("Now running genome assembly tools.")
	status_run_assemblies = run_assemblies(input_directory_path_for_fastq_files, output_genome_assembly, fastq_files_dict, kmer_dict, model_object_user)

	if not status_run_assemblies:
		print("Running assembly tools failed")
		return False

	print("Completed genome assembly tools.\n")
	#################Post Assembly Quality Check#################
	
	#print("Starting with post assembly quality check tools.")
	#print("Starting Quast")

	#quast_output = quast_runner(output_directory_path)

	return True
	

if __name__ == "__main__":
	'''
	For Unit testing the functionality of Genome Assembly group.
	Always make sure that this script is working intact when called specifically.
	'''
	status = main()
	print("Final Status: {}".format(status))

