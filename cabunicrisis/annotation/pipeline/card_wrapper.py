#!/usr/bin/env python
import os
import subprocess

### FIRST ACTIVATE CONDA ENVIRONMENT RGI USING: conda activate rgi
### In case script throws error the first time, run it again

def rgi_runner_plasmids(inp, outp, tab_inp):

	card_db = '../../../CARD_work/data'
	path_to_json = '../../../CARD_work/card.json'
	load = subprocess.check_output(["rgi", "load", "--card_json", "{}".format(path_to_json), "--local"])
	output = subprocess.check_output(["rgi", "main", "-i", inp, "-o", outp, "-t", "protein", "--local", "--clean"])
	
	# optional step
	tab = subprocess.check_output(["rgi", "tab", "-i", tab_inp])

def rgi_runner(inp, outp, tab_inp):

	card_db = '../../../CARD_work/data'
	path_to_json = '../../../CARD_work/card.json'
	load = subprocess.check_output(["rgi", "load", "--card_json", "{}".format(path_to_json), "--local"])
	output = subprocess.check_output(["rgi", "main", "-i", inp, "-o", outp, "-t", "protein", "--local", "--clean"])
	
	# optional step
	tab = subprocess.check_output(["rgi", "tab", "-i", tab_inp])


def main():

	# Check for output directories

	files = os.listdir('/home/projects/group-b/Team2-FunctionalAnnotation/output/CARD')
	output_dir = ['CARD_plasmids_results', 'CARD_results']
	for i in output_dir:
		if i not in files:
			os.mkdir(i)

	os.chdir('/home/projects/group-b/Team2-FunctionalAnnotation/output/CARD')
	# for plasmids
	if len(os.listdir('CARD_plasmids_results')) <=1:
		os.chdir('CARD_plasmids_results')
		plasmid_directory = '/home/projects/group-b/gene_prediction/plasmid_out/union_faa'
		print(os.listdir(plasmid_directory))
		for i in os.listdir(plasmid_directory):
			print(i)
			input_files = plasmid_directory + '/' + i
			x = i.split('_')[0]
			output_file_name = 'results_plasmid_{}'.format(x)
			tab_input = '../../../CARD_work/{}.json'.format(output_file_name)
			run_CARD_plasmids = rgi_runner_plasmids(input_files, output_file_name, tab_input)	
		
		location = os. getcwd()
		plasmids_heatmap = subprocess.check_output(["rgi", "heatmap", "-i", location])		

	os.chdir('/home/projects/group-b/Team2-FunctionalAnnotation/output/CARD')
	# for protein cluster file
	if len(os.listdir('CARD_results')) <= 1:
		os.chdir('CARD_results')
		input_files = '/home/projects/group-b/Team2-FunctionalAnnotation/output/cdhit/faa_rep_seq.faa'
		output_file_name = 'results'
		tab_input = '../../../CARD_work/{}.json'.format(output_file_name)
		run_CARD_plasmids = rgi_runner(input_files, output_file_name, tab_input)	
		location = os.getcwd()
		heatmap = subprocess.check_output(["rgi", "heatmap", "-i", location])		

	

if __name__ == "__main__":
	main()