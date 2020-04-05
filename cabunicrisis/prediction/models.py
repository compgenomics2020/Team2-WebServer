from django.db import models
from assembly.models import GenomeAssembly, User

# Create your models here.

class SingleCodingGenePrediction(models.Model):
	user = ForeignKey(User, related_name = "gene_predictions")
	contigs_file_path = models.ForeignKey(GenomeAssembly, related_name = "contig_file")
	gene_predicted_path=models.CharField(max_length=512)
	def __str__(self):
                return (str(self.path))

class CodingGenePrediction(models.Model):
	contigs_file_path = models.ForeignKey(GenomeAssembly, related_name = "contig_file")
	final_result_path = models.ForeignKey(SingleCodingGenePrediction, related_name = 'single_tool_result', null=True)
	result_prod_path = models.ForeignKey(SingleCodingGenePrediction, related_name = 'single_tool_result', null=True)
	tool_choices = models.CharField(max_length = 32, choices = [('1', 'GeneMarkS2'), ('2', 'Prodigal'),('3','Merge Results of both')]
	merge_path=models.CharField(max_length=512,null=True)
	#The following field holds an absolute path of the result file.
	#tool_result_path = models.CharField(max_length = 512)
	def __str__(self):
                return (str(self.path))

class SingleNCGenePrediction(models.Model):
        user = ForeignKey(User, related_name = "ncgene_predictions")
        contigs_file_path = models.ForeignKey(GenomeAssembly, related_name = "contig_file")
        ncgene_predicted_path=models.CharField(max_length=512)
        def __str__(self):
                return (str(self.path))

class CodingGenePrediction(models.Model):
        contigs_file_path = models.ForeignKey(GenomeAssembly, related_name = "contig_file")
        final_result_infernal_path = models.ForeignKey(SingleCodingGenePrediction, related_name = 'single_tool_result', null=True)
        final_result_all_path = models.ForeignKey(SingleCodingGenePrediction, related_name = 'single_tool_result', null=True)
        tool_choices = models.CharField(max_length = 32, choices = [('1', 'Infernal'), ('2', 'All')]
	
        #The following field holds an absolute path of the result file.
        #tool_result_path = models.CharField(max_length = 512)
        def __str__(self):
                return (str(self.path))


#"""
#def pipeline():
#	#Focus on coding genes.
#	#Two options.

#	#1. GM
#	#2. PD
#	#3. Both

#	#User picks option 3.
#	
#	result_GM: number of results files? 50?
#	result_PD: number of results files? 50?
#
#	======> Merge the results.
#	
#	merged_results = number of files? 50?
#
#	print(merged_results)
#	['/home/.../merged_file_1.txt', ..., '/home/.../merged_file_50.txt']
	
#	zip()

#	if merged_result:
		#Create MergedCodingGenePrediction
		
#		for file_path in merged_results:
#			obj = MergedCodingGenePrediction.objects.create(user = user_object, contigs_file_path = file_path)
		
		######Next##### 

		#Create CodingGenePrediction
#		for GM_file_path in results_GM:
#			obj = CodingGenePrediction.objects.create(..., final_result = Null)
#			###OR###
#			obj = CodingGenePrediction.objects.create(..., final_result = file_path)
#
#	else:
		
		#Create CodingGenePrediction
