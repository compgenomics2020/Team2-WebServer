#!/usr/bin/env python3

'''
  *******************************************************************
  **************-Run kSNP3.1 software on isolates-*******************
  *******************************************************************

  The usage for this script is: python3 make_phylogeny.py <path/to/input_file> </path/to/output/location>
  Please import required packages prior to usage.

  Input_file example: tab seperated file 
  /path/to/isolate1.fasta	isolate1
  /path/to/isolate2.fasta	isolate2
  /path/to/isolate3.fasta	isolate3
  .				.
  .				.
  .				.

  By: Courtney Astore
  Last updated: 04/12/2020

'''

import subprocess,os,sys

#def create_InputFile(input_directory_path):
#	list_of_file_paths = [f for f in os.listdir(input_directory_path) if os.path.isfile( os.path.join(input_directory_path, f) )]
#	list_of_IDs = []
#	for i in list_of_file_paths:
#		tmp = i.split("/",1)
		


def kSNP_runner(input_directory_path,output_directory_path):
        #Creating file path
	input_file=input_directory_path + faa_file
	output_dir = output_directory_path + "/OUT"
        try:
            print("kSNP3.1 "+ input_file)
            os.system("kSNP3 -in " + input_file + " -k 25 -outdir " + output_dir + "-ML")
	
        except subprocess.CalledProcessError as err:
            print("Error running kSNP3.1. Check the input files")
            print("Error thrown: "+err.output)
            return False

        print("Completed running kSNP3.1")
        return True
	
def main():
        inputpath=sys.argv[1] # input directory of files
        outputpath=sys.argv[2] # input subdirectory path to create
        
	#files=os.listdir(inputpath)

        #if len(files) == 0:
        #    print("No files present in the directory.")

        #for name in files:
        #     kSNP_run = kSNP_runner(inputpath,name,outputpath) # input_directory_path,faa_file,output_directory_path
	kSNP_Run = kSNP_runner(inputpath,outputpath) 
  
if __name__ == "__main__":
        main()
