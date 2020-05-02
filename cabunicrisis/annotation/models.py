from django.db import models
from assembly.models import User

class FunctionalAnnotation(models.Model):
	user = models.ForeignKey(User, related_name = "functional_annotation", on_delete=models.CASCADE, null=True)
	input_dir = models.CharField(max_length=512)
	graphs = models.CharField(max_length=512)
	output_dir = models.CharField(max_length=512)

	def __str__(self):
		return (str(self.user.email) + " with fna/faa/gff files: " + str(self.input_dir))
