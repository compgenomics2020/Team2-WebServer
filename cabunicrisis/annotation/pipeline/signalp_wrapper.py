#!/usr/bin/env python3
'''
Wrapper script for SignalP 5.0, an ab-initio tool for detecting signal peptides in bacterial proteomes.

SignalP requires contig fasta files as input. We will be using the contig files generated by the Genome Assembly group.

WARNING: Using "gene" sequences will not give the desired results.
this is an important script
36-96939
'''

import subprocess,os,sys,shutil

def signalp_runner(input_directory_path,faa_file):
    #Creating file path
	input_file=input_directory_path + faa_file

    #Creating a subdirectory in the output directory
    #output_subdir=output_directory_path

    try:
        print("SignalP 5.0 "+faa_file)
        subprocess.check_output(signalp_path, "-fasta", input_file,
			"-org", "gram-", "-format", "short", "-gff3")

    except subprocess.CalledProcessError as err:
        print("Error running SignalP. Check the input files.")
        print("Error thrown: "+err.output)
        return False

    print("Completed running SignalP")
    return True

def main(argv):
    inputpath=argv[0] # input directory of files
    outputpath=argv[1] # input subdirectory path to create
    files=os.listdir(inputpath)

	if os.path.exists(outputpath):
		shutil.rmtree(outputpath)
	os.mkdir(outputpath)

    if len(files) == 0:
        print("No files present in the directory.")
    for name in files:
        signalp_runner(inputpath,name) # input_directory_path,faa_file,output_directory_path
		name_gff3 = name.split(".")[0] + ".gff3"
		shutil.move(inputpath + name_gff3, outputpath + name_gff3)

if __name__ == "__main__":
        main(sys.argv[1:])
