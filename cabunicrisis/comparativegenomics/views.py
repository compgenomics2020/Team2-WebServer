from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
#from .models import Input_Files
import uuid
import os

# Create your views here.

def comparative_genomocs_home(request):
        #Landing page of Gene Prediction isolated functionality.
        #Upload files forms.
        if request.method == 'GET':
                raw_html = render(request, 'comparative/comparative.html')
                response = HttpResponse(raw_html)
                return response
        if request.method == 'POST':
        #Create a UUID for user.
                user_uuid = str(uuid.uuid4())
                #Directory names.
                dir_data = 'comparative/data/'
                dir_user = dir_data + user_uuid + '/'
                dir_contig = dir_user + '/' + 'contigs.fasta/'
                #Creating a directory for user.
                os.mkdir(dir_user)
                #Creating a directory for raw fastq files.
                os.mkdir(dir_contig)
                #Getting user's email.
                email = request.POST['email']
                #Get number of files.
                number_of_files = 0
                #Accessing and saving the files sent by user.
                for file in request.FILES.getlist('contig-files'):
                        with open(dir_contig + file.name, "w") as f:
                                f.write(str(file.read()))
                                number_of_files+=1
                #Create Raw files model.
                #Run Pipeline.
                raw_html = render(request,'compare/compare.html' , {'uuid_data': user_uuid, 'number_of_files': number_of_files})
                return HttpResponse(raw_html)
def pipeline_home(request):
        return HttpResponse("Pipeline Home Page")
