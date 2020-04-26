#!/usr/bin/env python3
'''
  *******************************************************************
  **************-Create phylogeny from kSNP results-*****************
  *******************************************************************

  The usage for this script is: python3 make_phylogeny.py <path/to/input_file.tre> </path/to/output/location>
  Please import required packages prior to usage.

  By: Courtney Astore
  Last updated: 04/12/2020

'''
import sys
import PyQt5
from ete3 import Tree, TreeStyle

#-------------- Read in .tre file data and read in as a string ------------------
def read_TreeFile(tree_file):
    with open(tree_file, 'r') as f:
        tree_data = f.read().replace('\n', '') # read in tree data as a single string
    return(tree_data)

#-------------- Generate a circular tree plot  ------------------
def Generate_CircleTree(treeData, output_path):
# Define output file name and its path
    file_name = "circle_tree.png"
    out_file = output_path + "/" + file_name

# Build tree & incorporate desired parameters for visualization
    t = Tree(treeData)
    circular_style = TreeStyle()
    circular_style.mode = "c"
    circular_style.scale = 20

# Produce/draw output figure: phylogeny
    t.render(file_name, w=183, units="mm", tree_style=circular_style)

#-------------- Generate just a normal horizantal tree plot ------------------
def Generate_NormalTree(treeData, output_path):
    file_name = "normal_tree.png"
    out_file = output_path + "/" + file_name

# Build tree & incorporate desired parameters for visualization
    t = Tree(treeData)
    #t.populate(50, random_dist=True)
    ts = TreeStyle()
    ts.show_leaf_name = True
    #ts.show_branch_length = True
    #ts.show_branch_support = True
    ts.scale = 20 # 120 pixels per branch length unit
    t.render(file_name, w=183, units="mm", tree_style=ts)

def main():
    tree_file = sys.argv[1]
    output_path = sys.argv[2]

    treeData = read_TreeFile(tree_file)
    makeCircleTree = Generate_CircleTree(treeData, output_path)
    makeNormalTree = Generate_NormalTree(treeData, output_path)

if __name__ == "__main__":
    main()
