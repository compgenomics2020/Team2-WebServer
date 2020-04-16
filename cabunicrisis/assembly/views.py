from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import User, RawFastqFiles
from .pipeline import main as pipeline_main
import uuid
import os

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
		dir_user = dir_data + user_uuid + '/'
		dir_raw_fastq = dir_user + 'raw-fastq/'
		dir_trimmed = dir_user + 'trimmed-files'
		dir_genome_assembly = dir_user + 'genome-assembly'
		dir_quast = dir_user + 'quast'

		#Creating a directory for user.
		os.mkdir(dir_user)

		#Creating a directory for raw fastq files.
		os.mkdir(dir_raw_fastq)
		os.mkdir(dir_trimmed)
		os.mkdir(dir_genome_assembly)
		os.mkdir(dir_quast)

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
			with open(dir_raw_fastq + file.name, "w") as f:
				f.write(str(file.read()))	
				number_of_files+=1
			#Creating the file model object and entry in the database.
			model_object_raw_fastq_file = RawFastqFiles(user = model_object_user, path = dir_raw_fastq + file.name)
			model_object_raw_fastq_file.save()

		#Run Pipeline.
		essential_arguments_for_pipeline = {'input_directory': dir_raw_fastq, 
											'output_trimmed_files': dir_trimmed, 
											'output_genome_assembly': dir_genome_assembly, 
											'output_quast': dir_quast, 
											'model_objects': {'user': model_object_user}}
		pipeline_status = pipeline_main(essential_arguments_for_pipeline)

		raw_html = render(request, 'assembly/assembly_homepage.html', {'uuid_data': user_uuid, 'number_of_files': number_of_files})
		return HttpResponse(raw_html)

def job_status(request):
	return HttpResponse("Genome Assembly Job Status")


def pipeline_home(request):
	return HttpResponse("Pipeline Home Page")


