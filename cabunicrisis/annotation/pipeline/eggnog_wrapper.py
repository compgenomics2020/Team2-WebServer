#!/usr/bin/env python2
#MAKE SURE TO USE PYTHON 2
import subprocess
import sys

def main(argv):
    eggnog_dir = argv[0]
    input_file = argv[1]
    output_file = argv[2]

    #download necessary databses
    make_db = subprocess.check_output(["python2", eggnog_dir + "/download_eggnog_data.py"])

    #run faa cluster against eggnog bacteria db with diamond method (& sign makes it run in the background)
    output =  subprocess.check_output(["python2", eggnog_dir + "/emapper.py", "-i", input_file, "-output", output_file, "-d", "bact", "-m", "diamond", ">", "log", "&"])

if __name__ == "__main__":
	main(sys.argv[1:])
