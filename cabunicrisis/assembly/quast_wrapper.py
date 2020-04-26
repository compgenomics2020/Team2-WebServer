#!/usr/bin/env python

import subprocess
import os

def get_files_by_tools(output_directory_path):
	#Returns a dictionary with contig files based on tools.
	masurca_results = []
	spades_results_untrimmed = []
	spades_results_on_trimmed = []
	skesa_results = []
	abyss_results = []
	velvet_results = []
	unicycler_results = []
	
	for root, dirs, files in os.walk(output_directory_path, topdown=True):
		for name in files:
			if name == "genome.ctg.fasta" or name == "contigs.fasta" or name == "contigs.fa" or name == "assembly.fasta":
				path = os.path.join(root, name)
				
				if "masurca" in path:
					if "9-terminator" in path:
						masurca_results.append(path)	
				
				if "spades" in path:
					spades_results.append(path)


	return {"masurca": masurca_results, "spades": spades_results,}

def quast_runner(output_directory_path):
	#Get output files by tools used.
	all_output_files = get_files_by_tools(output_directory_path)
	
	#############################Directory Prechecks#######################
	quast_output_path = output_directory_path.rstrip('/') + '/' + "quast"

	#First check if quast directory is there.
	if "quast" not in os.listdir(output_directory_path):
		os.mkdir(quast_output_path)

	#Paths for output dirs.
	output_dir_paths = {tool: quast_output_path + '/' + tool for tool in list(all_output_files.keys())}

	#Check if quast directory in output directory has tool directories already.
	for output_dir_path in list(output_dir_paths.values()):
		if not os.path.exists(output_dir_path):
			os.mkdir(output_dir_path)

	#Get files that have already been processed.
	with open('tmp/quast_completed.txt') as f:
		raw = f.read()

	already_processed_files = raw.split('\n')
	#print(already_processed_files)	

	for tool_name, files in all_output_files.items():
		print("Processing files for tool: {}".format(tool_name))
		for input_file_path in files:
			#Get directory path for quast file outputs.
			path_els = input_file_path.split('/')
			path_els = path_els[::-1][1:]
			tail_file_path_for_quast = ""
			for path_el in path_els:
				if path_el == tool_name:
					break
				tail_file_path_for_quast = path_el + "-" + tail_file_path_for_quast

			#Minor fix.
			file_path_for_quast = output_dir_paths[tool_name].rstrip('/') + '/' + tail_file_path_for_quast.rstrip('-')

			#Check if file has already been processed.
			if input_file_path in already_processed_files:
				print("File: {} has already been processed by Quast, skipping...".format(input_file_path))
				continue
			if not os.path.exists(file_path_for_quast):
				os.mkdir(file_path_for_quast)

			#######################################################################
			#############################Execute Quast#############################
			try:
				print("Running Quast on: {}".format(input_file_path))
				
				quast_output = subprocess.check_output(["quast", input_file_path, "-o", file_path_for_quast])

				#Write the output files for later use.
				with open('tmp/quast_outputs.txt', 'a') as fo, open("tmp/quast_completed.txt", "a") as fc:
					fo.write(file_path_for_quast + "\n")
					fc.write(input_file_path + "\n")

			except subprocess.CalledProcessError:
				print("==========>Quast could not finish quality check for tool: {} & file: {}".format(tool_name, input_file_path))
				continue



if __name__ == "__main__":
	pass



