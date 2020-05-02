"""
Run Gene Prediction Pipe

    last edited: 03/21/2020

"""

#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import subprocess
import shutil
from .coding.genemarks2_wrapper import genemarks2_script
from .coding.prodigal_wrapper import prodigal_script
from .coding.union_outputs import merge_predict
from .coding.blastn import blastn_script
from .coding.rename_faa_fna import rename
from .coding.rename_gff import rename_gff
from .noncoding.aragorn_wrapper import aragorn_script
from .noncoding.barrnap_wrapper import barrnap_script
from .models import Coding_Rename_Path
import json

#############################################################################################################################################################################################
############################### https://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text/22157136#22157136 ########################################

# Helps to format the argparse options
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


#############################################################################################################################################################################################

#Check if the tool which needs to be run is present or not
def check_tools(run_tool):
    tools_to_run=[]
    if(run_tool==1):
        tools_to_run.append("gms2.pl")
    elif(run_tool==2):
        tools_to_run.append("prodigal")
    else:
        #bedtools, samtools and transeq are the tools needed to merge the results hence are needed to be called
        tools_to_run.extend(["gms2.pl","prodigal","bedtools"])
    #print(tools_to_run)
    for tools in tools_to_run:

        try:
            #Calling the genemarks2,prodigal or both by name.
            bash_output = subprocess.check_output([tools])
        except (FileNotFoundError, subprocess.CalledProcessError) as error:
            print("The tool {}, was not present on the system. Please check again".format(tools))
            return False
        print("{} is present".format(tools))
    return True


#################################################################################################################################################################################################

#check whether input files folder is present and not empty or not
def check_input(folder_name):
    if os.path.isdir(folder_name):
        if len(os.listdir(folder_name))!=0:
            print("The folder {} is not empty".format(folder_name))
            return True
        else:
            print("The folder {} is empty".format(folder_name))
            return False
    else:
        print("The folder {} is not present".format(folder_name))
        return False


##############################################################################################################################################################################################

# Running GeneMarkS-2 and/or Prodigal based on the options given by the user, it takes in the input path to the files, output path, type of the species( either bacteria or auto for genemarks-2) and which tool to run or both to run
def running_tools(input_path,output_path,type_species,run_tool,input_option,name="contigs.fasta"):
    list_of_files=[]
    list_failed=[]
    #List all the directories present in the input path, where the wrapper goes into those directories and runs the contigs files
    #print(os.listdir(input_path))
    for folder in sorted(os.listdir(input_path)):

       #print(folder)
       if (run_tool=="1" or run_tool=="3"):
            genemarks2_output=genemarks2_script(input_path,folder,output_path,type_species,input_option,name)
            if genemarks2_output != False:
                list_of_files.append(folder)
            else:
                list_failed.append(folder)
                continue
       if(run_tool=="2" or run_tool=="3"):
            prodigal_output=prodigal_script(input_path,folder,output_path,input_option,name)
            if prodigal_output != False and run_tool!=3:
                list_of_files.append(folder)
            if run_tool!=3 and prodigal_output==False:
                list_failed.append(folder)
                continue
            #if prodigal_output == False:
                #return False
    list_of_files=list(set(list_of_files))
    list_failed=list(set(list_failed))
    return True,list_of_files,list_failed


############################################################################################################################################################################################

# Blast validation function
def blast_results(run_tool,out):

    #Checks if gene_marks2 is called or prodigal or the union of both
    if run_tool=="1":
        #Sets the genemarks2 generated output to be the input to be given to the blast script
        genemarks2_output=out+"/genemarks2/"
        #Lists all the files in the genemarks2 output directory
        for folder_file in os.listdir(genemarks2_output):
            #Runs the blast script
            blast_out_genemarks2=blastn_script(genemarks2_output, folder_file, out,run_tool)
            if blast_out_genemarks2 == False:
                return False

    #Same if only prodigal is called
    elif run_tool=="2":
        prodigal_output=out+"/prodigal/"
        for folder_file in os.listdir(prodigal_output):
            blast_out_prodigal=blastn_script(prodigal_output,folder_file, out,run_tool)
            if blast_out_prodigal == False:
                return False

    #Same if both the tools are called and the merge results are obtained
    else:
        union_input_path=out+"/merge_out/union_fna"
        for folder_file in os.listdir(union_input_path):
            blast_out=blastn_script(union_input_path ,folder_file, out,run_tool)
            if blast_out == False:
                return False
    return True


#################################################################################################################################################################################################

# Run the rename script to generate output files with known and unknown genes
def rename_scripts(list_of_files,out,run_tool):
    blast_input_path=out+"/blast"
    output_check=out+"/known_unknown/"
    #os.mkdir(output_check)
    #Checks if gene_marks2 is called or prodigal or the union of both
    if run_tool=="1":
        for files in list_of_files:
            genemarks2_output=out+"/genemarks2/"+files
            condition=rename(genemarks2_output,blast_input_path,files, out,"fna",run_tool)
            if condition == False:
                return False
            condition=rename(genemarks2_output, blast_input_path, files, out,"faa",run_tool)
            if not condition:
                return False
            condition=rename_gff(genemarks2_output,blast_input_path,files,out,run_tool)
            if not condition:
                return False
    #Same if only prodigal is called
    elif run_tool=="2":
        prodigal_output=out+"/prodigal/"
        for folder_file in os.listdir(prodigal_output):
            prodigal_output=out+"/prodigal/"+folder_file
            condition=rename(prodigal_output,blast_input_path,folder_file, out,"fna",run_tool)
            if condition== False:
                return False
            condition=rename(prodigal_output,blast_input_path,folder_file, out,"faa",run_tool)
            if condition== False:
                return False
            condition=rename_gff(prodigal_output,blast_input_path,folder_file,out,run_tool)
            if not condition:
                return False
    #Same if both the tools are called and the merge results are obtained
    else:
        union_path_fna=out+"/merge_out/union_fna"
        union_path_faa=out+"/merge_out/union_faa"
        union_path_gff=out+"/merge_out/union_gff"
        for files in list_of_files:
            condition=rename(union_path_fna, blast_input_path, files, out, "fna",run_tool)
            if not condition:
                return False
            condition=rename(union_path_faa, blast_input_path, files, out,"faa",run_tool)
            if not condition:
                return False
            condition=rename_gff(union_path_gff,blast_input_path,files,out,run_tool)
            if not condition:
                return False
        shutil.rmtree(union_path_fna)
        shutil.rmtree(union_path_faa)
    return True

def graph(list_of_files,list_of_hits,x_name,out):
    objects = list_of_files
    y_pos = np.arange(len(objects))
    performance = list_of_hits
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Hits')
    plt.title(x_name)
    name=out+"/"+x_name+".png"
    plt.savefig(name)

def hits_list(list_of_files,run_tool,out):
    blast_input_path=out+"/blast"
    list_blast_hits=[]
    #list_of_files=[]
    list_total_hits=[]
    for files in os.listdir(blast_input_path):
        blast_dir=blast_input_path+"/"+files
        p = subprocess.Popen(['wc', '-l', blast_dir], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        #list_of_files.append(files)
        list_blast_hits.append(int(result.strip().split()[0]))
    graph(list_of_files,list_blast_hits,"Blast Results",out)

    if run_tool=="1" or run_tool=="3":
        genemark_hits=[]
        for files in list_of_files:
            genemarks2_output=out+"/genemarks2/"+files+"/"+files+"_output.gff"
            p = subprocess.Popen(['wc', '-l', genemarks2_output], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            result, err = p.communicate()
            if p.returncode != 0:
                raise IOError(err)
            genemark_hits.append(int(result.strip().split()[0]))

        graph(list_of_files,genemark_hits,"GeneMarkS-2 Results",out)

        genemarks2_output=out+"/genemarks2/"
        shutil.rmtree(genemarks2_output)

    #Same if only prodigal is called
    if run_tool=="2" or run_tool=="3":
        prodigal_hits=[]
        for files in list_of_files:
            prodigal_output=out+"/prodigal/"+files+"/"+files+"_output.gff"
            p = subprocess.Popen(['wc', '-l', prodigal_output], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            result, err = p.communicate()
            if p.returncode != 0:
                raise IOError(err)
            prodigal_hits.append(int(result.strip().split()[0]))

        graph(list_of_files,prodigal_hits,"Prodigal Results",out)

        prodigal_output=out+"/prodigal/"
        shutil.rmtree(prodigal_output)

    #Same if both the tools are called and the merge results are obtained
    if run_tool=="3":
        union_path_gff=out+"/merge_out/union_gff/"
        merge_hits=[]
        for files in list_of_files:
            union_output=union_path_gff+files+"_union.gff"
            p = subprocess.Popen(['wc', '-l', union_output], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            result, err = p.communicate()
            if p.returncode != 0:
                raise IOError(err)
            merge_hits.append(int(result.strip().split()[0]))

        graph(list_of_files,merge_hits,"Union Results",out)

        merge_folder=out+"/merge_out/"
        shutil.rmtree(union_path_gff)
        shutil.rmtree(merge_folder)
    #shutil.rmtree(blast_input_path)

#################################################################################################################################################################################################

# Running Aragon and Barrnap based on the options given by the user, it takes in the input path to the files, output path
def noncoding_run(input_path,output_path,flag,name="contigs.fasta"):
    #List all the directories present in the input path, where the wrapper goes into those directories and runs the contigs files
    for folder in os.listdir(input_path):
        barrnap_output=barrnap_script(input_path,folder,output_path,flag,name)
        aragon_output=aragorn_script(input_path,folder,output_path,flag,name)
        if aragon_output==False:
            return False
    return True
#################################################################################################################################################################################################

######## main of the script which takes in the input ######################################

def main(model_object_user,model_object_rename,gene_output,input_option,input_assembly=None,input_plasmids=None,input_files77=None,input_files99=None,coding_tools="3"):


    ################################# User Input ######################################################################
    # parser = argparse.ArgumentParser(description="Backbone script",formatter_class=SmartFormatter)
#
    # parser.add_argument("-io","--input-option",default="1",help="R|Default Option is 1, options available\n"
    # "1 Take input from the genome assembly results \n"
    # "2 Input your own assembly files \n"
    # "3 Plasmid Input from Genome Assembly")
    # parser.add_argument("-nc", "--name-contigs", default="contigs.fasta" ,help="Name of the contig files,called when option 2 for input-option is selected, default considered is contigs.fasta",required=False)
    # parser.add_argument("-ia", "--input-assembly", help="Path to the directory that contains input file manually,called when option 2 for input-option is selected",required=False)
    # parser.add_argument("-ip", "--input-plasmids", help="Path to the directory that contains input file for plasmid spades output called when Plasmid Input from Genome Assembly called ",required=False)
    # parser.add_argument("-if77", "--input-files77", help="Path to the directory that contains input file for spades output of 21,33,55,77, called when default option for input-option is selected",required=False)
    # parser.add_argument("-if99", "--input-files99", help="Path to the directory that contains input file for spades output of 21,33,55,77,99,127,called when default option for input-option is selected",required=False)
    # parser.add_argument("-go", "--gene-output", help="Path to a directory that will store the output gff files, fna files and faa files.", required=True)
    # parser.add_argument("-tr","--coding-tools",default="3",help="R|Default Option is 3, options available to run are\n"
    # "1 Only GeneMarkS-2 \n"
    # "2 Only Prodigal \n"
    # "3 Both and getting a union of the genes")
    # parser.add_argument("-ts", "--type-species", help="if running Gene_MarkS-2, mention species to be either bacteria or auto")
#
    #
    #
    # args = vars(parser.parse_args())
    ##################################### User input ends and variables are assigned #############################################################


    output_path=gene_output
    run_tool=coding_tools
    if run_tool=="1" or run_tool=="3":
        type_species="auto"
    flag=input_option
    name="contigs.fasta"
    #print(flag)


    ##############################################################################################################################################
    #checks whether genemarks2 and prodigal tools, if either or both are called are present or not.
    if not check_tools(run_tool):
        return False

    ##### If the user wants to take in his own input###############################################################################################
    if flag == "2":
        input_path=input_assembly

        if check_input(input_path):
            # checks the input folder for manual input, and then runs the tools. Considers input folder to contain specific sequence folder which in turn contains the name variable (name of the contigs)
            # Runs prodigal or genemarks2 or both depending on the user's choice calls the function run_out
            run_out,list_of_files,list_failed=running_tools(input_path,output_path,type_species,run_tool,flag,name)
            #If run out is false, it just returns false and the function returns the appropriate error message
            if not run_out:
                return False


            #If the user has chosen to run both gene marks2 and prodigal, we get the merge results of it by calling the script function merge_predict from the union script
            if run_tool=="3":
                genemarks2_output=output_path+"/genemarks2/"
                prodigal_output=output_path+"/prodigal/"
                merge_output=output_path+"/merge_out"
                #### If the merge output directory doesnt exist, it makes a directory called merge out where the output files will be located,
                # or just deletes the folder if it is present
                if os.path.exists(merge_output) == False:
                    os.mkdir(merge_output)
                else:
                    shutil.rmtree(merge_output)
                    os.mkdir(merge_output)
                # Runs the function merge_predict
                merge=merge_predict(genemarks2_output,prodigal_output,input_path)
                #If merge is false, it just returns false and the function returns the appropriate error message
                if not merge:
                    return False


            blast_output=blast_results(run_tool,output_path)
            if not blast_output:
                return False
            rename_output=rename_scripts(list_of_files,output_path,run_tool)
            if not rename_output:
                return False
            hits_list(list_of_files,run_tool,output_path)
            print(list_failed)

            ###########################################################################################################
            ######Non coding tools, runs infernal or aragon,rnammer or infernal tools and calls the function nc_run_out
            nc_run_out=noncoding_run(input_path,output_path,flag,name)
            #If nc_run_out is false, it just returns false and the function returns the appropriate error message
            if not nc_run_out:
                return False
            ###########################################################################################################
            model_object_rename.list_failed = json.dumps(list_failed)
            model_object_rename.save()
            model_object_user.job_status = True
            model_object_user.save()
        else:
            return False
    ##################################################################################################################################################
    elif flag== "1":
        input_folder77=input_files77
        input_folder99=input_files99
        if check_input(input_folder77) and check_input(input_folder99):
            ###########################Coding tools, GeneMarkS2 and Prodigal, merge the results or keep them seperate blast out the results and
            # there are two input paths as there are two folders given to us by the genome assembly group according to the kmer count
            # Runs prodigal or genemarks2 or both depending on the user's choice calls the function run_out
            run_out,list_of_files_77,list_failed_77=running_tools(input_folder77,output_path,type_species,run_tool,flag,name)
            #If run_out is false, it just returns false and the function returns the appropriate error message
            run_out,list_of_files_99,list_failed_99=running_tools(input_folder99,output_path,type_species,run_tool,flag,name)
            list_of_files=list_of_files_77+list_of_files_99
            list_failed=list_failed_77+list_failed_99
            #If the user has chosen to run both gene marks2 and prodigal, we get the merge results of it by calling the script function merge_predict from the union script
            if run_tool=="3":
                genemarks2_output=output_path+"/genemarks2/"
                prodigal_output=output_path+"/prodigal/"
                merge_output=output_path+"/merge_out"
                #### If the merge output directory doesnt exist, it makes a directory called merge out where the output files will be located,
                # or just deletes the folder if it is present
                if os.path.exists(merge_output) == False:
                    os.mkdir(merge_output)
                else:
                    shutil.rmtree(merge_output)
                    os.mkdir(merge_output)
                # Runs the function merge_predict
                merge=merge_predict(genemarks2_output,prodigal_output,input_folder77,merge_output,input_folder99)
                #If merge is false, it just returns false and the function returns the appropriate error message
                if not merge:
                    return False
            # Running the individual results or
            blast_output=blast_results(run_tool,output_path)
            if not blast_output:
                return False
            rename_output=rename_scripts(list_of_files,output_path,run_tool)
            if not rename_output:
                return False
            hits_list(list_of_files,run_tool,output_path)
            ###########################################################################################################
            ######Non coding tools, runs infernal or aragon,rnammer or infernal tools and calls the function nc_run_out
            nc_run_out1=noncoding_run(input_folder99,output_path,flag,name)
            if not nc_run_out1:
                return False
            nc_run_out=noncoding_run(input_folder77,output_path,flag,name)
            #If nc_run_out is false, it just returns false and the function returns the appropriate error message
            if not nc_run_out:
                return False
            ###########################################################################################################
            model_object_rename.list_failed = json.dumps(list_failed)
            model_object_rename.save()
            model_object_user.job_status = True
            model_object_user.save()
        else:
            return False
    else:
        input_path=input_plasmids

        if check_input(input_path):
            # checks the input folder for plasmids, and then runs the tools.
            # Runs prodigal or genemarks2 or both depending on the user's choice calls the function run_out
            run_out,list_of_files,list_failed=running_tools(input_path,output_path,type_species,run_tool,flag,name)
            #If run out is false, it just returns false and the function returns the appropriate error message
            #If the user has chosen to run both gene marks2 and prodigal, we get the merge results of it by calling the script function merge_predict from the union script
            if run_tool=="3":
                genemarks2_output=output_path+"/genemarks2/"
                prodigal_output=output_path+"/prodigal/"
                merge_output=output_path+"/merge_out"
                #### If the merge output directory doesnt exist, it makes a directory called merge out where the output files will be located,
                # or just deletes the folder if it is present
                if os.path.exists(merge_output) == False:
                    os.mkdir(merge_output)
                else:
                    shutil.rmtree(merge_output)
                    os.mkdir(merge_output)
                # Runs the function merge_predict
                merge=merge_predict(genemarks2_output,prodigal_output,input_path)
                #If merge is false, it just returns false and the function returns the appropriate error message
                if not merge:
                    return False
            blast_output=blast_results(run_tool,output_path)
            if not blast_output:
                return False
            rename_output=rename_scripts(list_of_files,output_path,run_tool)
            if not rename_output:
                return False
            ###########################################################################################################
            model_object_rename.list_failed = json.dumps(list_failed)
            model_object_rename.save()
            model_object_user.job_status = True
            model_object_user.save()
        else:
            return False
################################################################################################################################################################################################################
if __name__=="__main__":
    main()
