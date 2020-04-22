import os,sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def main(argv):
    in_dir = argv[0]
    out_dir = argv[1]

    files = set([file.split('.')[0] for file in os.listdir(in_dir)])
    tools = set([tool.split('_')[-1] for tool in files])
    names = set([name.split('_')[0] for name in files])

    for tool in tools:
        tool_dict = {}
        for name in names:
            print(tool)
            print(name)
            input_file = next((x for x in files if (tool in x and name in x)), None)
            print(input_file)
            files.remove(input_file)
            input_file = in_dir + "/" + input_file + ".gff"
            if tool != 'signalp':
                with open(input_file) as f:
                    wc = sum(1 for line in f)
                    tool_dict[name] = wc
            else:
                with open(input_file) as f:
                    lipo = sum(1 for line in f if ("lipoprotein_signal_peptide" in line))
                    sp = sum(1 for line in f if ("signal_peptide" in line))
                    tool_dict[name] = (lipo,sp)

        csv_file = out_dir + '/' + tool + '.csv'
        png_file = out_dir + '/' + tool + '.png'
        if tool != 'signalp':
            with open(csv_file, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=["Proteome", "Count"])
                writer.writeheader()
                for name in tool_dict:
                    writer.writerow([name, int(tool_dict[name])])

            f = pd.read_csv(csv_file, sep=',', low_memory=False)
            df = pd.DataFrame(f)
            df.set_index('Proteome', inplace=True)
            fig = plt.figure(figsize=(30,10))
            ax = fig.add_subplot(111)
            ax2 = ax.twinx()
            width = 0.3

            df.Count.plot(kind='bar', color='red', ax=ax, width=width, position=1)

            ax.set_ylabel(tool + ' Count', fontsize=16)
            ax2.set_ylabel('Lipoprotein Count', fontsize=16)
            ax.set_xlabel('Sequence', fontsize=16)
            #plt.title('Histogram of ', fontsize=12)
            count_patch = mpatches.Patch(color='green', label=tool + ' Count')
            plt.legend(handles=[countpatch], frameon=False, fontsize=16)
            plt.xticks(fontsize=16)
            plt.yticks(fontsize=16)
            plt.tight_layout()
            plt.savefig(png_file)

        else:
            with open(csv_file, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=["Proteome", "Lipoprotein", "SingalPeptide"])
                writer.writeheader()
                for name in tool_dict:
                    (lipo, sp) = tool_dict[name]
                    writer.writerow([name, int(lipo), int(sp)])

            f = pd.read_csv(csv_file, sep=',', low_memory=False)
            df = pd.DataFrame(f)
            df.set_index('Proteome', inplace=True)
            fig = plt.figure(figsize=(30,10))
            ax = fig.add_subplot(111)
            ax2 = ax.twinx()
            width = 0.3

            df.SignalPeptide.plot(kind='bar', color='red', ax=ax, width=width, position=1)
            df.Lipoprotein.plot(kind='bar', color='blue', ax=ax2, width=width, position=0)

            ax.set_ylabel('Signal Peptide Count', fontsize=16)
            ax2.set_ylabel('Lipoprotein Count', fontsize=16)
            ax.set_xlabel('Sequence', fontsize=16)
            #plt.title('Histogram of ', fontsize=12)
            signal_patch = mpatches.Patch(color='red', label='Signal Peptide')
            lipo_patch = mpatches.Patch(color='blue', label='Lipoprotein')
            plt.legend(handles=[signal_patch,lipo_patch], frameon=False, fontsize=16)
            plt.xticks(fontsize=16)
            plt.yticks(fontsize=16)
            plt.tight_layout()
            plt.savefig(png_file)



if __name__ == "__main__":
	main(sys.argv[1:])
