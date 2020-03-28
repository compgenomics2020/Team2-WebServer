from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
# Create your views here.

def home(request):
	#Landing page of Predictive Webserver.

	#A lot of these variables are defined according to Shivam's style of coding.
	#Please feel free to change them carefully, if required.
	raw_html = render(request, 'homepage.html')
	response = HttpResponse(raw_html)
	
	return response
