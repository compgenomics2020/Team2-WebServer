from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import User
# Create your views here.

def index(request):
	#Landing page of Predictive Webserver.

	#A lot of these variables are defined according to Shivam's style of coding.
	#Please feel free to change them carefully, if required.
	raw_html = render(request, 'homepage.html')
	response = HttpResponse(raw_html)
	
	return response

def usr_view(request,usr_id):
	#Landing page of Predictive Webserver.

	#A lot of these variables are defined according to Shivam's style of coding.
	#Please feel free to change them carefully, if required.
	
	
	return HttpResponse("You are now in your homepage"% usr_id)

def test_index(request):
	#Landing page of Predictive Webserver.

	#A lot of these variables are defined according to Shivam's style of coding.
	#Please feel free to change them carefully, if required.
	
	
	return render(request, 'assembly/index.html', {'usr_id' : User.uuid})
