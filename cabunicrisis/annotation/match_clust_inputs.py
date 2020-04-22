import sys
from os import listdir
from shutil import copyfile

def main(argv):
    input_dir = argv[0]
    output_dir = argv[1]

    for na in ['n','a']:
        matching = {}

        for filename in listdir(input_dir + '/f'+na+'a'):
            filename = input_dir + '/f' + na + 'a/' + filename
            with open(filename) as fnaa_file:
                for line in fnaa_file:
                    if line[0] == '>':
                        in_matching = line.split()[0]+'...'
                        matching[in_matching] = filename

        copyfile(output_dir + '/f'+na+'a_rep_seq.f'+na+'a.clstr',
                 output_dir + '/f'+na+'a_cluster_membership.txt')

        with open(output_dir + '/f'+na+'a_cluster_membership.txt','r') as clstr:
            c_lines = clstr.readlines()

            for ind in range(len(c_lines)):
                c_line = c_lines[ind].split()
                if c_line[0] != '>Cluster':
                    c_lines[ind] = matching[c_line[2]]+'\n'

        with open(output_dir + '/f'+na+'a_cluster_membership.txt','w') as clstr:
            clstr.writelines(c_lines)

if __name__ == "__main__":
	main(sys.argv[1:])
