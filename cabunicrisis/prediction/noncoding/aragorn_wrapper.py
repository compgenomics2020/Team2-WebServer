"""
Run aragon for each contigs assembled
Output: fasta file

    last edited: 03/19/2020
    
"""
#!/usr/bin/python3
import os,subprocess

def aragorn_script(input_path,assembly_file,output_folder_path,flag,name):
    if flag =="2":
        assembly_input=input_path+assembly_file
        if assembly_file not in os.listdir(input_path):
            return False
    else:
        assembly_input_path=input_path+assembly_file
        assembly_input=input_path+assembly_file+"/"+name
        if name not in os.listdir(assembly_input_path):
            return False
        if name not in os.listdir(assembly_input_path):
            return False
    #output_tool is the folder it will create in the output_folder_path based on the tool which is running
    output_tool=output_folder_path+"/aragon/"
    #output_folder_path is the folder in which the output folders will be generated in. It will check whether those folders are present or will generate them. 
    output_folder=output_tool+assembly_file
    if "aragon" in os.listdir(output_folder_path):
        if assembly_file in os.listdir(output_tool):
            if not len(os.listdir(output_folder)) == 0:
                print("Output Directory {} contains files,please delete them before running the tool for the same file".format(output_folder))
                return False
        else:
            os.mkdir(output_folder)
    else:
        os.mkdir(output_tool)
        os.mkdir(output_folder)
    #each output folder generated will have three sequences which will be produced.
    output_fasta=output_folder+"/"+assembly_file+"_output.fa"
    try:
        print("Running ARAGORN for:" ,assembly_file)
            #aragorn` running with genome-type bacteria
        bash_output=subprocess.check_output(["aragorn", "-l", "-t", "-gc1", "-w ", assembly_input, "-fo", output.fasta])
    except subprocess.CalledProcessError:
        print("Error running ARAGORN please check the installation and files ")
        return False
    
    print("Completed running ARAGORN for",assembly_file)
    return True

if __name__=="__main__":
    pass
    #aragorn_script  
