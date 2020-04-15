from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import User
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
		dir_raw_fastq = dir_user + '/' + 'raw-fastq/'

		#Creating a directory for user.
		os.mkdir(dir_user)

		#Creating a directory for raw fastq files.
		os.mkdir(dir_raw_fastq)

		#Getting user's email.
		email = request.POST['email']
		
		#Get number of files.
		number_of_files = 0

		#Accessing and saving the files sent by user.
		for file in request.FILES.getlist('raw-fastq-files'):
			with open(dir_raw_fastq + file.name, "w") as f:
				f.write(str(file.read()))	
				number_of_files+=1

		#Create Raw files model.



		#Run Pipeline.

		raw_html = render(request, 'assembly/assembly_homepage.html', {'uuid_data': user_uuid, 'number_of_files': number_of_files})
		return HttpResponse(raw_html)

def job_status(request):
	return HttpResponse("Genome Assembly Job Status")


def pipeline_home(request):
	return HttpResponse("Pipeline Home Page")


