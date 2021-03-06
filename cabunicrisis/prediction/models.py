from django.db import models
from assembly.models import GenomeAssembly, User
#from multiselectfield import MultiSelectField


# Create your models here.
class Input_Files_contigs(models.Model):
	USER_INPUT = 'user_upload'
	GENOME_INPUT = 'genome_assembly_input'
	INPUT_CHOICES = ((USER_INPUT, 'user_upload'),(GENOME_INPUT, 'genome_assemby_input'),)
	user = models.ForeignKey(User, related_name = "assembled_files",blank=True, on_delete=models.CASCADE)
	type_choice = models.CharField(max_length=32,choices=INPUT_CHOICES)
	contigs_user_path= models.CharField(max_length=512,blank=True)
	contigs_file_path=models.ForeignKey(GenomeAssembly, related_name ="input_files",blank=True, on_delete=models.CASCADE)
	
	def __str__(self):
		if self.type_choice=="user_upload":
			return (str(self.contigs_user_path))
		else:
			return (str(self.contigs_file_path))
	
class Blast_Results(models.Model):
	contigs_file_path = models.ForeignKey(Input_Files_contigs, related_name = "blast_results", on_delete=models.CASCADE)
	path = models.CharField(max_length=512)
	def __str__(self):
	    return (str(self.path))

class Coding_Rename_Path(models.Model):
	blast_file_path= models.ForeignKey(Blast_Results, related_name = "coding_rename_path", on_delete=models.CASCADE)
	rename_dir_path = models.CharField(max_length=512)
	list_failed=models.TextField(null=True)
	def __str__(self):
		return (str(self.rename_dir_path))
	
class Plasmids_Output(models.Model):
	plasmids_file_path= models.ForeignKey(GenomeAssembly, related_name = "plasmid_assembly_file", on_delete=models.CASCADE)
	path = models.CharField(max_length=512)	
	def __str__(self):
		return (str(self.path))
	
class NC_Aragon(models.Model):
	contigs_file_path = models.ForeignKey(Input_Files_contigs, related_name = "nc_aragon", on_delete=models.CASCADE)
	path= models.CharField(max_length=512)
	def __str__(self):
		return (str(self.path))
	
class NC_Barrnap(models.Model):
	contigs_file_path = models.ForeignKey(Input_Files_contigs, related_name = "nc_barrnap", on_delete=models.CASCADE)
	path= models.CharField(max_length=512)
	def __str__(self):
		return (str(self.path))