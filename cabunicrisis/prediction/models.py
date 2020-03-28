from django.db import models
from assembly.models import GenomeAssembly, User

# Create your models here.

class MergedCodingGenePrediction(models.Model):
	user = ForeignKey(User, related_name = "gene_predictions")
	contigs_file_path = models.ForeignKey(GenomeAssembly, related_name = "contig_file")


class CodingGenePrediction(models.Model):
	contigs_file_path = models.ForeignKey(GenomeAssembly, related_name = "contig_file")
	final_result = models.ForeignKey(MergedCodingGenePrediction, related_name = 'single_tool_result', null=True)
	tool_choices = models.CharField(max_length = 32, choices = [('GM', 'Gene Mark'), ('PD', 'Prodigal')])
	
	#The following field holds an absolute path of the result file.
	tool_result_path = models.CharField(max_length = 512)


class NonCodingGenePrediction(models.Model):
	user = ForeignKey(User, related_name = "gene_predictions")
	contigs_file_path = models.ForeignKey(GenomeAssembly, related_name = "contig_file")



"""
def pipeline():
	#Focus on coding genes.
	#Two options.

	#1. GM
	#2. PD
	#3. Both

	#User picks option 3.
	
	result_GM: number of results files? 50?
	result_PD: number of results files? 50?

	======> Merge the results.
	
	merged_results = number of files? 50?

	print(merged_results)
	['/home/.../merged_file_1.txt', ..., '/home/.../merged_file_50.txt']
	
	zip()

	if merged_result:
		#Create MergedCodingGenePrediction
		
		for file_path in merged_results:
			obj = MergedCodingGenePrediction.objects.create(user = user_object, contigs_file_path = file_path)
		
		######Next##### 

		#Create CodingGenePrediction
		for GM_file_path in results_GM:
			obj = CodingGenePrediction.objects.create(..., final_result = Null)
			###OR###
			obj = CodingGenePrediction.objects.create(..., final_result = file_path)

	else:
		
		#Create CodingGenePrediction


6 contig file?

GM: 6
Merged: 6

GM_2, Merged_2

"""