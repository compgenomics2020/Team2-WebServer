
#!/usr/bin/python3
import os,subprocess


def barrnap_script(input_path,assembly_file,output_folder_path,type_species,flag,name):
    #Get the contigs file from all the different assemblies generated
    #input= input_path is the folder in which different contigs are kept example:21,33,55,77 and assembly_file is the actual folder i.e CGT2049. name just takes those contigs files 
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
    output_tool=output_folder_path+"/barrnap/"
    #output_folder_path is the folder in which the output folders will be generated in. It will check whether those folders are present or will generate them. 
    output_folder=output_tool+assembly_file
    if "barrnap" in os.listdir(output_folder_path):
        if assembly_file in os.listdir(output_tool):
            if not len(os.listdir(output_folder)) == 0:
                print("Output Directory {} contains files,please delete them before running the tool for the same file".format(output_folder))
                return False
        else:
            os.mkdir(output_folder)
    else:
        os.mkdir(output_tool)
        os.mkdir(output_folder)
    #each output folder generated will have three sequences which will be produced, example file generate: output_folder_path/CGT2149/CGT2149_nucleotide.fnn
    output_rrna=output_folder+"/"+assembly_file+"_rrna.fa"
    output_gff=output_folder+"/"+assembly_file+"_rrna.gff"
    try:
        print("Running Barrnap for:" ,assembly_file)
        with open(output_gff,"w+") as file:
            bash_output=subprocess.check_output(["barrnap","--quiet","-o","rrna.fa","contigs.fasta"],stdout=file)
    except subprocess.CalledProcessError:
        print("Error running Barrnap please check the installation and files ")
        return False
    print("Completed running Barrnap for",assembly_file)
    return True
if __name__=="__main__":
    pass
    #barrnap_script  