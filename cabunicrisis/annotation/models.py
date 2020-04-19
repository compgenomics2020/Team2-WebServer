from django.db import models
from assembly.models import GenomeAssembly, User
from prediction.models import CodingGenePrediction

class PredictionGffFiles(models.Model):
	pred_gff = models.ForeignKey(CodingGenePrediction, related_name = "pred_gff_files")
	path = models.CharField(max_length=512)
	file = models.FileField(upload = 'raw_gff_files/')

	def __str__(self):
		return (str(self.path))

class PredictionFnaFiles(models.Model):
	pred_fna = models.ForeignKey(CodingGenePrediction, related_name = "pred_fna_files")
	path = models.CharField(max_length=512)
	file = models.FileField(upload = 'raw_fna_files/')

	def __str__(self):
		return (str(self.path))

class PredictionFaaFiles(models.Model):
	pred_faa = models.ForeignKey(CodingGenePrediction, related_name = "pred_faa_files")
	path = models.CharField(max_length=512)
	file = models.FileField(upload = 'raw_faa_files/')

	def __str__(self):
		return (str(self.path))

class PredictionFnaFiles(models.Model):
	pred_fna = models.ForeignKey(CodingGenePrediction, related_name = "pred_fna_files")
	path = models.CharField(max_length=512)
	file = models.FileField(upload = 'raw_fna_files/')

	def __str__(self):
		return (str(self.path))

class ClusteredFiles(models.Model):
	clust_files = models.ForeignKey(CodingGenePrediction, related_name = "pred_fna_files")
	path = models.CharField(max_length=512)
	file = models.FileField(upload = 'raw_fna_files/')

	def __str__(self):
		return (str(self.path))
