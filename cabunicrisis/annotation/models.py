from django.db import models
from assembly.models import User
from prediction.models import Blast_Results

class FunctionalAnnotation(models.Model):
	user = models.ForeignKey(User, related_name = "functional_annotation", on_delete=models.CASCADE)
	input_dir = models.ForeignKey(Blast_Results, related_name = "functional_annotation", on_delete=models.CASCADE)
	graphs = models.CharField(max_length=512)
	output_dir = models.CharField(max_length=512)

	def __str__(self):
		return (str(self.path))


# inputs: combined directory of fna/faa/gff directories - ex: dir/fna/*.fna
# the subdirectories are called faa and fna and gff.

# pipeline: faa/fna -> clustering + gff -> homology.
# faa + fna + gff -> ab initio.
# above two lines -> merged annotations into one directory.

# output: directory of 50 gff files

# START of pipeline
# Paarth gives the following:
# user_uuid = user_model_object.uuid <- correct path of directories
# input_dir = blast_results_model_object.path
# "data/" + user_uuid + "/" + "Annotation" <- output directory of directories (add /graphs, /output_dir)

# END of PIPELINE
# model_object_genome_assembly = GenomeAssembly(user = model_object_user,
# 												raw_untrimmed_file_1 = model_object_raw_fastq_file,
# 												path = contigs_file_path)
#
# model_object_genome_assembly.save()

# TODO:
# must add signalp/bin to $PATH
