from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import FunctionalAnnotation
import uuid
import os

def annotation_home(request):
    #Landing page of Functional Annotation isolated functionality.
    if request.method == 'GET':
            raw_html = render(request, 'annotation/annotation_homepage.html')
            response = HttpResponse(raw_html)
            return response

def pipeline_home(request):
        return HttpResponse("Pipeline Home Page")
