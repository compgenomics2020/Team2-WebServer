#!/usr/bin/env python3

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help = "Please input your file")
    args = parser.parse_args()

    input_file = args.f

    f = pd.read_csv(input_file, sep=',', low_memory=False)

    df = pd.DataFrame(f)
    df.set_index('ID', inplace=True)

    df['Date'] = df["SampleDate"].astype("datetime64")

    df1 = df.replace(np.nan, ' ', regex=True)

    column_values = df1[['Food1','Food2','Food3','Food4']].values.ravel().tolist()

    c = dict()
    for i in set(column_values):
        c[i] = column_values.count(i)

    new_dict = {key:val for key, val in c.items() if key != ' '}

    plt.figure(figsize=(20, 5))
    plt.bar(range(len(new_dict)), list(new_dict.values()), align='center', color=['red', 'orangered','orange', 'gold','yellow', 'limegreen','green','lightseagreen', 'aqua','blue', 'purple', 'violet', 'deeppink','pink'])

    plt.xticks(range(len(new_dict)), list(new_dict.keys()))
    plt.xlabel('Food Type', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.savefig('epi_food.png')
'''
    plt.figure(figsize=(20, 5))
    plt.hist(df['Date'])

    #plt.legend(frameon=False, fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.savefig('epi_graph.png')
'''
if __name__ == "__main__":
    main()
