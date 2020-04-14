from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import User
import uuid


# Create your views here.

def assembly_home(request):
	#Landing page of Genome Assembly isolated functionality.

	#Upload files forms.
	raw_html = render(request, 'homepage.html')
	response = HttpResponse(raw_html)
	
	return response

def upload_files(request):
	#Check for files.

	#Create a UUID for user.
	user_uuid = uuid.uuid4()

	#Create Raw files model.

	#Return the link to status page.
	return HttpResponse("Upload files status page.")


def pipeline_home(request):
	return HttpResponse("Pipeline Home Page")