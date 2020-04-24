from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.db import models
from .models import User, GenomeAssembly
from .pipeline import main as pipeline_main
import uuid
import os
import threading

# Create your views here.

def assembly_home(request):
	#Landing page of Genome Assembly isolated functionality.
	#Jobs can be submitted for isolated genome assembly jobs.
	if request.method == 'GET':
		raw_html = render(request, 'assembly/assembly_homepage.html')
		response = HttpResponse(raw_html)
		return response

	if request.method == 'POST':
		#Create a UUID for user.
		user_uuid = str(uuid.uuid4())
		#Directory names.
		dir_data = 'data/'


		#Creating a directory for user.
		dir_user = os.path.join(dir_data, user_uuid)
		os.mkdir(dir_user)

		#For input and output.
		dir_input = os.path.join(dir_user, 'input')
		dir_output = os.path.join(dir_user, 'output')

		os.mkdir(dir_input)
		os.mkdir(dir_output)

		#For fastq uploads.
		dir_fastq = os.path.join(dir_input, 'fastq')
		os.mkdir(dir_fastq)

		#For Assembly, trimmed files, quast.
		dir_trimmed = os.path.join(dir_output, 'trimmed')
		dir_assembly = os.path.join(dir_output, 'assembly')
		dir_quast = os.path.join(dir_output, 'quast')
		dir_plasmids = os.path.join(dir_output, 'plasmids')


		os.mkdir(dir_trimmed)
		os.mkdir(dir_assembly)
		os.mkdir(dir_quast)
		os.mkdir(dir_plasmids)


		#Getting user's email.
		email = request.POST['email']
		
		#Get number of files.
		number_of_files = 0

		#Create User model.
		model_object_user = User(uuid = user_uuid, email = email, if_pipeline = False)
		model_object_user.save()

		#Create Raw files model.
		#Accessing and saving the files sent by user.
		for file in request.FILES.getlist('raw-fastq-files'):
			#Check if fastq file is legitimate.
			legitimate = check_if_fastq_file(file)
			if not legitimate:
				continue
			
			with open(os.path.join(dir_fastq, file.name), "wb") as f:
				f.write(file.read())	
				number_of_files+=1
			

		#Create a GenomeAssembly Object.
		model_object_genome_assembly = GenomeAssembly(user = model_object_user, 
														raw_files_dir_path = dir_fastq, 
														trimmed_files_dir_path = dir_trimmed,
														contig_files_dir_path = dir_assembly,
														quast_files_dir_path = dir_quast,
														plasmid_files_dir_path = dir_plasmids )
		model_object_genome_assembly.save()

		#Run Pipeline.
		essential_arguments_for_pipeline = {'input_directory_path_for_fastq_files': dir_fastq, 
											'output_trimmed_files': dir_trimmed, 
											'output_genome_assembly': dir_assembly,
											'output_plasmids': dir_plasmids, 
											'output_quast': dir_quast, 
											'model_objects': {'user': model_object_user, 'assembly': model_object_genome_assembly}}
		#pipeline_status = pipeline_main(essential_arguments_for_pipeline)

		pipeline_thread = threading.Thread(target=pipeline_main, kwargs=essential_arguments_for_pipeline) 
		pipeline_thread.start() 


		raw_html = render(request, 'assembly/assembly_homepage.html', {'uuid_data': user_uuid, 'number_of_files': number_of_files})
		return HttpResponse(raw_html)


def pipeline_home(request):
	return HttpResponse("Pipeline Home Page")



def job_status(request):
	if request.method == 'GET':
		raw_html = render(request, 'status/status.html', {'user': False})
		response = HttpResponse(raw_html)
		return response

	if request.method == 'POST':
		#Get email or uuid sent by the user.
		email = request.POST['email']
		uuid = request.POST['uuid']
		try:
			model_object_user = User.objects.get(uuid = uuid)
		except ValidationError:
			raw_html = render(request, 'status/status.html', {'user': False})
			response = HttpResponse(raw_html)
			return response

		model_object_genome_assembly = model_object_user.assembly.all()[0]		
		#Get the assembly contig files.
		number_of_contig_files = len(contig_file_paths(dir_assembly))

		raw_html = render(request, 'status/status.html', {'user': model_object_user, 
															'assembly': model_object_genome_assembly, 
															'number_of_contig_files': number_of_contig_files})
		return HttpResponse(raw_html)


def get_contig_file_paths(dir_assembly):
	dir_spades = os.path.join(dir_assembly, 'spades')
	sample_paths = [os.path.join(dir_spades, sample) for sample in os.listdir(dir_spades)]
	contig_file_paths = []
	for sample_path in sample_paths:
		if os.path.exists(os.path.join(sample_path, 'contigs.fasta')):
			contig_file_paths.append(os.path.join(sample_path, 'contigs.fasta'))
	return contig_file_paths


def download_contig_files(request):
	return



def check_if_fastq_file(file):
	return True
