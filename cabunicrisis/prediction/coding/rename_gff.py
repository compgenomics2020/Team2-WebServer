"""
Mark union_gff files with KNOWN (K) or UNKNOWN (U) according to hits in
its corresponding blast file.
    created by: Danielle Temples
    edited by: Paarth Parekh
    last edited: 03/19/2020
    
"""

#!/usr/bin/python
import os, subprocess

def rename_gff(input_path, blast_input_path, input_file, output_path,run_out):
    #blast_input_path = the folder that the formatted blast files are in (ex: blast/formatted_)
    #union_input_path = the folder that the union gff files are in (ex: union_gff)
    #input_file = the specific file number in the folders (ex: CGT2049, CGT2211)
    #blast_input_file = the specific blast file that correlates to the input file (ex: CGT2049_union.fna_blast)
    
    if run_out =="3":
        blast_input_file = blast_input_path+"/"+input_file+"_union.fna_blast"
        #union_input_file = the specific union file that correlates to the input file (ex: CGT2049_union.fna/faa)
        input_file_path = input_path+"/"+input_file+"_union.gff"
        #output_folder= the folder that the known/unknown files will be placed in (folder in input_path named kn_union_fna/faa)
        output_folder = output_path+"/known_unknown/"+"/gff/"
        #output_file = the ku file in the ku folder under the union folders (ex: known_unknown_faa/CGT2049_union.faa)
        #output_file = output_folder+"/"+input_file+"_union."+type
        if input_file+"_union.gff" not in os.listdir(input_path):       #if CGT2049_union.fna/faa does not exist in union_fna/faa
            print("Input Directory does not contain inputted input file {}. Please check before running tool for same file").format(input_file)
            return False
        if input_file+"_union.fna_blast" not in os.listdir(blast_input_path):       #if CGT2049_union.fna_blast does not exist in blast directory
            print("Blast Directory does not contain corresponding file to input file {}. Please check before running tool for same file").format(blast_input_file)
            return False
    else:
        blast_input_file = blast_input_path+"/"+input_file+"_blast"
        #union_input_file = the specific union file that correlates to the input file (ex: CGT2049_union.fna/faa)
        input_file_path = input_path+"/"+input_file+"_output.gff"
        #output_folder= the folder that the known/unknown files will be placed in (folder in input_path named kn_union_fna/faa)
        output_folder = output_path+"/known_unknown/"+"/gff/"
        #output_file = the ku file in the ku folder under the union folders (ex: known_unknown_faa/CGT2049_union.faa)
        #output_file = output_folder+"/"+input_file+"_union."+type
        if input_file+"_output.gff" not in os.listdir(input_path):       #if CGT2049_union.fna/faa does not exist in union_fna/faa
            print("Input Directory does not contain inputted input file {}. Please check before running tool for same file").format(input_file)
            return False
        if input_file+"_blast" not in os.listdir(blast_input_path):       #if CGT2049_union.fna_blast does not exist in blast directory
            print("Blast Directory does not contain corresponding file to input file {}. Please check before running tool for same file").format(blast_input_file)
            return False
    output_check=output_path+"/known_unknown/"
    if "gff" in os.listdir(output_check):    #if known_unknown_(faa or fna) already exists in output_folder/fna folder
        if input_file+".gff" in os.listdir(output_folder):  #if CGT2049_union.faa/fna already exists in output_folder/fna folder
            print("Output Directory {} contains file. Please delete it before running the tool for the same file").format(output_folder)
            return False
        else:
            output_file = output_folder+input_file+".gff"   #make file in known_unknown_fna/faa folder called CGT2049_union.faa/fna
            subprocess.call("cp "+input_file_path+" "+ output_file,shell=True)  #copy contents from input file to output file (union_faa/CGT2049_union.faa -> output_folder/known_unknown_faa/CGT_union_faa)
    else:
        os.mkdir(output_folder)     #make ku_union_fna/faa folder if it does not exist
        output_file = output_folder+input_file+".gff"   #make file in known_unknown_fna/faa folder called CGT2049_union.faa/fna
        subprocess.call("cp "+input_file_path+" "+output_file,shell=True)  #copy contents from input file to output file (union_faa/CGT2049_union.faa -> output_folder/known_unknown_faa/CGT_union_faa)

    original = open(output_file, 'r').readlines()
    hits = open(blast_input_file, 'r').readlines()
    match = []
    start = []
    stop = []
    write_output=open(output_file,"w")
    for l in hits:
            tabbed_line = l.split('\t')
            before = tabbed_line[0]
            match.append(before.partition(":")[0])
            start.append(before[before.find(":")+1:before.find("-")])
            stop.append(before[before.find("-")+1:])
    for line in original:
            if line.startswith("#"):
                    continue
            data = line.split('\t')[0]
            num1 = line.split('\t')[3]
            num2 = line.split('\t')[4]
            if data in match and num1 in start and num2 in stop:
                    write_output.write(line.replace("\t", " K" + "\t", 1))
            else:
                    write_output.write(line.replace("\t", " U" + "\t", 1))
    write_output.close()
    return True
if __name__=="__main__":
    pass
