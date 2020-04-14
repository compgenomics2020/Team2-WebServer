from django.db import models
from assembly.models import GenomeAssembly, User

# Create your models here.
class Input_Files(models.Model):
	USER_INPUT = 'user_upload'
	GENOME_INPUT = 'genome_assembly_input'
	INPUT_CHOICES = ((USER_INPUT, 'user_upload'),(GENOME_INPUT, 'genome_assemby_input'),)
	type = models.CharField(max_length=20,choices=INPUT_CHOICES)
	user = models.ForeignKey(User, related_name = "assemble_files",blank=True, on_delete=models.CASCADE)
	contigs_user_path= models.CharField(max_length=512,blank=True)
	contigs_file_path=models.ForeignKey(GenomeAssembly, related_name = "contig_files",blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return (str(self.path))

class Blast_Results(models.Model):
	contigs_file_path = models.ForeignKey(Input_Files, related_name = "contig_files", on_delete=models.CASCADE)
	path = models.CharField(max_length=512)
	def __str__(self):
	    return (str(self.path))

class Coding_Rename_Path(models.Model):
	blast_file_path= models.ForeignKey(Input_Files, related_name = "blast_files", on_delete=models.CASCADE)
	path = models.CharField(max_length=512)	
	def __str__(self):
		return (str(self.path))

class Nc_Final(models.Model):
	contigs_file_path = models.ForeignKey(Input_Files, related_name = "contig_files", on_delete=models.CASCADE)
	path= models.CharField(max_length=512)
	def __str__(self):
		return (str(self.path))
