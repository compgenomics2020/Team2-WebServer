import uuid
from django.db import models

# Create your models here.

class User(models.Model):
	uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	email = models.EmailField(max_length = 254)
	job_status = models.BooleanField(default = False)
	creation_date = models.DateField(auto_now_add = True , blank = True)

	def __str__(self):
		return (str(self.email) + "with ID: " + str(self.uuid))


class RawFastqFiles(models.Model):
	user = models.ForeignKey(User, related_name = "user")
	path = models.CharField(max_length=512)

	def __str__(self):
		return (str(self.path))


class TrimmedFiles(models.Model):
	raw_file = models.ForeignKey(RawFastqFiles, related_name = "raw_file")
	path = models.CharField(max_length=512)	

	def __str__(self):
		return (str(self.path))


class GenomeAssembly(models.Model):
	raw_untrimmed_file = models.ForeignKey(RawFastqFiles, related_name = "raw_untrimmed_file")
	raw_trimmed_file = models.ForeignKey(TrimmedFiles, related_name = "raw_trimmed_file")
	contigs_file_path = models.CharField(max_length=512)

	def __str__(self):
		return (str(self.path))


class Quast(models.Model):
