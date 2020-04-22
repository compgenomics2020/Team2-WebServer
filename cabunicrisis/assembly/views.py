from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import User
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

		os.mkdir(dir_trimmed)
		os.mkdir(dir_assembly)
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
			#Check if fastq file is legitimate.
			legitimate = check_if_fastq_file(file)
			if not legitimate:
				continue
			with open(os.path.join(dir_fastq, file.name), "w") as f:
				f.write(str(file.read()))	
				number_of_files+=1

		#Run Pipeline.
		essential_arguments_for_pipeline = {'input_directory': dir_fastq, 
											'output_trimmed_files': dir_trimmed, 
											'output_genome_assembly': dir_assembly, 
											'output_quast': dir_quast, 
											'model_objects': {'user': model_object_user}}
		pipeline_status = pipeline_main(essential_arguments_for_pipeline)

		raw_html = render(request, 'assembly/assembly_homepage.html', {'uuid_data': user_uuid, 'number_of_files': number_of_files})
		return HttpResponse(raw_html)

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
		raw_html = render(request, 'status/status.html', {'user': model_object_user})
		return HttpResponse(raw_html)


def pipeline_home(request):
	return HttpResponse("Pipeline Home Page")


