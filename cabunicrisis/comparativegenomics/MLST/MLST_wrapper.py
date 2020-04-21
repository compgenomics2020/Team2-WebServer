 """
MLST (Multilocus Sequnce Typing) Analysis for Campylobactor spp. using "mlst" (input: contig/.fasta files)
    
    created by: Kara Keun Lee
    last edited: 04/15/2020
    
"""
#!/usr/bin/env python3

import os
import subprocess as sp

def mlst(input_contigs_path, output_mlst_path):
    
    # check the input directory provided contain contig files:
    if not os.listdir(input_contigs_path) :
        print("There are no contig files in the given input directory. Please check and try again.")
        return None

    # check if output directories exist:
        # Yes --> check if outputs already exist and if so, ask to delete before proceeding 
        # No --> make new output directory
    if os.path.exists(output_mlst_path) == False:
        sp.call(["mkdir",output_mlst_path])
    else:
        if os.listdir(output_mlst_path):
            print("Output directory already exists with contents. Please delete previous files before continuing")
            return None
    
    # specify output file path & name (in text, csv, and ST-only file):
    mlst_out = output_mlst_path+"/mlst_output.txt"
    mlst_out_csv = output_mlst_path+"/mlst_output.csv"
    mlst_out_STonly = output_mlst_path+"/mlst_output_STonly.txt"
    
    # run mlst:
    sp.call(["cd",input_contigs_path])
    sp.call(["mlst","--legacy","--scheme","campylobacter","./*",">",mlst_out])
    sp.call(["mlst","--csv","--legacy","--scheme","campylobacter","./*",">",mlst_out_csv])
    
    # create a .txt file with only sample IDs & STs to be used for visualization:
    id_st=[]
    with open("output_legacy.txt") as f:
        for line in f:
            columns = line.strip().split("\t")
            ID= columns[0]
            ST= columns[2]
            if ID!="FILE":
                id_st.append([ID[2:], ST])
            else:
                id_st.append([ID, ST])
        
    #for i in id_st:
        #print('\t'.join(map(str,i)))
        
    with open(mlst_out_STonly, 'w') as out: 
        for i in id_st:
            out.write('\t'.join(map(str,i))+'\n')    
            
if __name__=="__main__":
    pass

