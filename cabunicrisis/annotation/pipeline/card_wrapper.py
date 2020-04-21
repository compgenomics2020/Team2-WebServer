#!/usr/bin/env python
import os
import sys
import subprocess

### FIRST ACTIVATE CONDA ENVIRONMENT RGI USING: conda activate rgi
### In case script throws error the first time, run it again

def main(input_file, output_file, db_dir):
	try:
		subprocess.check_output(["rgi", "load", "--card_json", db_dir + "/card.json", "--local"])
		subprocess.check_output(["rgi", "main", "-i", input_file, "-o", output_file, "-t", "protein", "--local", "--clean"])
		subprocess.check_output(["rgi", "tab", "-i", tab_inp])
	except subprocess.CalledProcessError as err:
		print("Error running CARD. Check the input files.")
		print("Error thrown: " + err.output)
		return False
	return True

if __name__ == "__main__":
	prot_file = sys.argv[0]
	plasmid_dir = sys.argv[1]
	output_dir = sys.argv[2]
	db_dir = sys.argv[3]

	main(prot_file, output_dir + "/CARD_results/results", db_dir)

	for pf in os.listdir(plasmid_dir):
		x = pf.split('_')[0]
		plasmid = plasmid_dir + "/" + pf
		main(plasmid, output_dir + "/CARD_plasmids_results/results_plasmid" + x, db_dir)
