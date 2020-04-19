#!/usr/bin/env python2
#MAKE SURE TO USE PYTHON 2
import os
import subprocess

download_db = './download_eggnog_data.py '
input_file = '../cdhit/faa_rep_seq.faa'
output_file = 'eggnog_results'

#download necessary databses
make_db = subprocess.check_output(["python2", "{}".format(download_db))])

#run faa cluster against eggnog bacteria db with diamond method (& sign makes it run in the background)
output =  subprocess.check_output(["python2", "./emapper.py", "-i", input_file, "-output", output_file, "-d", "bact", "-m", "diamond", ">", "log", "&")]
