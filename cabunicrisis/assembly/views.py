from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import User
import uuid


# Create your views here.

def assembly_home(request):
	#Landing page of Genome Assembly isolated functionality.

	#Upload files forms.
	if request.method == 'GET':
		raw_html = render(request, 'assembly/assembly_homepage.html')
		response = HttpResponse(raw_html)
		return response

	if request.method == 'POST':
		user_uuid = uuid.uuid4()
		for file in request.FILES.getlist('raw-fastq-files'):
			with open("blah.txt", "w") as f:
				f.write(str(file.read()))	
			#print(file.name)
		return HttpResponse("Yes")

def assembly_upload_files(request):
	#Check for files.
	#Create a UUID for user.

	#Create Raw files model.

	#Return the link to status page.
	return HttpResponse("Upload files status page.")


def pipeline_home(request):
	return HttpResponse("Pipeline Home Page")


