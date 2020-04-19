#!/usr/bin/env python
import os
import subprocess

download_db = './FDB_setA_nt.fas'
path_to_db = './VFDB_db'
input_file = '../cdhit/faa_rep_seq.fna'
output_file = 'VFDB_result'

make_db = subprocess.check_output(["makeblastdb", "-in", "{}".format(download_db), "-dbtype", "'nucl'", "-out", "{}".format(path_to_db)])
output =  subprocess.check_output(["blastn", "-db", path_to_db, "-query", input_file, "-out", output_file, "-max_hsps", "1", "-max_target_seqs", "1",
    "-outfmt", "6 qseqid length qstart qend sstart send evalue bitscore stitle", "-perc_identity", "100", "-num_threads", "5")]
