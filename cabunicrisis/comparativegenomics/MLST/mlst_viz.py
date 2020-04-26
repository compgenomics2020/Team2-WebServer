#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt

'''
This script creates a simple visualisation of the sequence types detected by the MLST tool for the web server.
'''

def mlst_viz(mlst_result_path,output_path):
	
	#Reading the mlst results
	st_dic={}
	count=0
	st_count=0
	with open(mlst_result_path,"r") as inp:
		for line in inp:
			col=line.split("\t")
			col1=col[0].split(".")
			sample_name=col1[1].replace("/","")
			st=col[2]
			count=count+1
			if st not in st_dic.keys():
				st_count=st_count+1
				st_dic[st]=[sample_name]
			else:
				st_dic[st].append(sample_name)
	
	#Getting the sample number of each ST to determine the radius of the circle
	st_size={}
	for key in st_dic.keys():
		st_size[key]=len(st_dic[key])/float(count)
	
	#Plotting the circles	
	cent_x=0
	rad=0
	
	fig, ax = plt.subplots()
	for st in st_size.keys():
		colors = np.random.rand(3,)
		cent_x=cent_x+1+st_size[st]
		centre=(cent_x,1)
		cent_y=0
		plt.annotate(xy=(cent_x-0.25,2.5),s="ST"+st,fontsize=9,verticalalignment="center",horizontalalignment="center")
		for item in st_dic[st]:
			cent_y=cent_y-0.5
			plt.annotate(xy=(cent_x-0.25,cent_y),s=item,fontsize=6.5,verticalalignment="center",horizontalalignment="center")
		rad=rad+(3*st_size[st])+2
		circle=plt.Circle(centre,(2*st_size[st]),color=colors)
		ax.add_artist(circle)
		ax.axis("equal")
		cent_x=cent_x+st_size[st]+1
	
	fig.suptitle('Sequence Types detected by MLST', fontsize=20, fontweight='bold')	
	plt.figtext(0.5,0.05, "Samples belonging to a particular ST are listed beneath each circle", fontsize=6,verticalalignment="center",horizontalalignment="center")		

	ax.set_xlim(-2,rad)
	ax.set_ylim(-(count/(st_count)),4)
	plt.plot([-2,rad], [-(count/(st_count)),4], alpha=0)
	plt.axis("off")
	out_file=output_path+'/'+"mlst_viz.png"
	fig.savefig(out_file)
		


def main():
	mlst_input=sys.argv[1]
	mlst_viz_output=sys.argv[2]
	mlst_viz(mlst_input,mlst_viz_output)
if __name__ == "__main__":
        main()
