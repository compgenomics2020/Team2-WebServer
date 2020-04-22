#!/usr/bin/env python

import subprocess,os,sys

input_folder="/home/projects/group-b/Team2-FunctionalAnnotation/tmp"
files=os.listdir(input_folder)
for name in files:
	if name.endswith("op.gff")==True:
		input_file=input_folder+"/"+name
		print(name)
		command="cat "+input_file+" | wc -l"
		os.system(command)
	
