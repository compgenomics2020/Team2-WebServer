from django.db import models
from assembly.models import GenomeAssembly, User
from prediction.models import CodingGenePrediction
# Create your models here.
class Input_Files(models.Model):
	  USER_INPUT = 'user_upload'
	  GENOME_INPUT = 'genome_assembly_input'
	  INPUT_CHOICES = ((USER_INPUT, 'user_upload'),(GENOME_INPUT, 'genome_assemby_input'),)
	  type = models.CharField(max_length=32,choices=INPUT_CHOICES)
	  user = models.ForeignKey(User, related_name = "assemble_files",blank=True, on_delete=models.CASCADE)
	  contigs_user_path= models.CharField(max_length=512,blank=True)
	  contigs_file_path=models.ForeignKey(GenomeAssembly, related_name ="input_files",blank=True, on_delete=models.CASCADE)

	  def __str__(self):
		   return (str(self.path))
