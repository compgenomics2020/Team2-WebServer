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
	user = models.ForeignKey(User, related_name = "raw_files", on_delete=models.CASCADE)
	path = models.CharField(max_length=512)

	def __str__(self):
		return (str(self.path))


class TrimmedFiles(models.Model):
	raw_file = models.OneToOneField(RawFastqFiles, on_delete=models.CASCADE, related_name = "trimmed_file")
	path = models.CharField(max_length=512)	

	def __str__(self):
		return (str(self.path))


class GenomeAssembly(models.Model):
	user = models.ForeignKey(User, related_name = "assembly", on_delete=models.CASCADE)
	raw_untrimmed_file = models.ForeignKey(RawFastqFiles, related_name = "raw_untrimmed_file", on_delete=models.CASCADE)
	raw_trimmed_file = models.ForeignKey(TrimmedFiles, related_name = "raw_trimmed_file", null = True, on_delete=models.CASCADE)
	path = models.CharField(max_length=512)
	job_status = models.BooleanField(default = False)

	def __str__(self):
		return (str(self.path))


class Quast(models.Model):
	user = models.ForeignKey(User, related_name = "quast", on_delete=models.CASCADE)
	assembly = models.ForeignKey(GenomeAssembly, related_name = "quast", null = True, on_delete=models.CASCADE)
	path = models.CharField(max_length=512)
	l_50 = models.CharField(max_length = 16)
	n_50 = models.CharField(max_length = 16)


	def __str__(self):
		return (str(self.path))




