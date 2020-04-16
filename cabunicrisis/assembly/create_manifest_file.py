#!/usr/bin/env python
import argparse
from bs4 import BeautifulSoup
import os


def create_manifest_file(input_html_path, manifest_file_path):
	#See if file already exist.
	if os.path.exists(manifest_file_path):
		print("Manifest file already present, using that...")
		return False

	#Skip if input file does not exist.
	if not os.path.exists(input_html_path):
		print("Can't parse the input html file.")
		return False

	#Create a delicious soup.
	with open(input_html_path) as f:
		soup = BeautifulSoup(f, "html.parser")

	table = soup.find(id="general_stats_table")
	table_body = table.tbody

	#Find rows in table.
	table_rows = table_body.find_all('tr')

	#print(table_rows[0])

	manifest = {}

	for table_row in table_rows:
		#First column is table heading.
		file_name = table_row.th.text.strip("")
		
		#Reading columns.
		columns = table_row.find_all('td')
		#Read lenth is in 3rd column.
		read_length = int(columns[2].text.replace(" bp", ""))
		
		manifest[file_name] = read_length

	with open(manifest_file_path, "w") as f:
		for file_name, read_length in manifest.items():
			f.write(file_name + '\t' + str(read_length) + '\n')

	return True
		

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input-html-file", help="Path to MultiQc's pre-trim html file.", required=True)
	parser.add_argument("-o", "--output-manifest-file", help="Path to output tsv file.", required=True)

	args = vars(parser.parse_args())

	input_html_path = args['input_html_file']
	output_manifest_file = args['output_manifest_file']

	#Check if tmp exist.
	if not os.path.exists('tmp'):
		os.mkdir('tmp')

	create_manifest_file(input_html_path, output_manifest_file)




