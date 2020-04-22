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
		subprocess.check_output(["rgi", "tab", "-i", output_file + ".json"])
	except subprocess.CalledProcessError as err:
		print("Error running CARD. Check the input files.")
		print("Error thrown: " + err.output)
		return False
	return True

if __name__ == "__main__":
	prot_file = sys.argv[0]
	output_dir = sys.argv[1]
	db_dir = sys.argv[2]

	main(prot_file, output_dir + "/faa", db_dir)
