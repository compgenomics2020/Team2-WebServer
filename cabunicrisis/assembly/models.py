import uuid
from django.db import models

# Create your models here.


####Important####
#It's stupid to save files manually and then make the entry instead of using django's file field.
#I didn't use it because it appeared better to create a subdir for every user.

class User(models.Model):
	uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	email = models.EmailField(max_length = 254)
	job_status = models.BooleanField(default = False)
	if_pipeline = models.BooleanField(default = False)
	creation_date = models.DateField(auto_now_add = True , blank = True)

	def __str__(self):
		return (str(self.email) + " with ID: " + str(self.uuid))


class GenomeAssembly(models.Model):
	user = models.ForeignKey(User, related_name = "raw_files", on_delete=models.CASCADE)
	raw_files_dir_path = models.CharField(max_length=512)
	trimmed_files_dir_path = models.CharField(max_length=512)
	contig_files_dir_path = models.CharField(max_length=512)
	quast_files_dir_path = models.CharField(max_length=512)

	def __str__(self):
		return (str(self.user.email) + " with raw files: " + str(self.raw_files_dir_path))


