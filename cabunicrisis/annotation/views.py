from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import FunctionalAnnotation
from .pipeline import main, process_in_directory
import uuid
import os
import threading

def annotation_home(request):
    #Landing page of Functional Annotation isolated functionality.
    if request.method == 'GET':
        raw_html = render(request, 'annotation/annotation_homepage.html')
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
        input_dir = os.path.join(dir_user, 'input')
        output_dir = os.path.join(dir_user, 'output')

        os.mkdir(dir_input)
        os.mkdir(dir_output)

        #For sorting input into faa/fna/gff dirs
        fna_dir = os.path.join(dir_input, 'fna')
        faa_dir = os.path.join(dir_input, 'faa')
        gff_dir = os.path.join(dir_input, 'gff')

        os.mkdir(fna_dir)
        os.mkdir(faa_dir)
        os.mkdir(gff_dir)

        #Getting user's email.
        email = request.POST['email']

        #Get number of files.
        number_of_files = 0

        #Create User model.
        model_object_user = User(uuid = user_uuid, email = email, if_pipeline = False)
        model_object_user.save()

        #Create FunctionalAnnotation files model.
        #Accessing and saving the files sent by user.
        input_files = request.FILES.getlist('all-files')
        #Check if input files are legitimate, make input directory suitable for pipeline.
        # legitimate, message_or_numfiles = process_in_directory(input_files, input_dir)
        check_thread = threading.Thread(process_in_directory, [input_files, input_dir])
        check_thread.start()
        [legitimate, message_or_numfiles] = check_thread
        if not legitimate:
            print(message_or_numfiles)

        # Add to path so that we can run some tools
        pwd = os.getcwd()
        tmhmm_path = os.path.join(pwd, "tmhmm-2.0c/bin")
        if tmhmm_path not in os.environ["PATH"]:
            os.environ["PATH"] += tmhmm_path
        signalp_path = os.path.join(pwd, "signalp-5.0b/bin")
        if signalp_path not in os.environ["PATH"]:
            os.environ["PATH"] += signalp_path

        pipeline_thread = threading.Thread(target=main, args=[input_dir, output_dir, "/projects/VirtualHost/predictb/databases/annotation"])
        pipeline_thread.start()

        raw_html = render(request, 'annotation/annotation_homepage.html', {'uuid_data': user_uuid, 'number_of_files': message_or_numfiles})
        return HttpResponse(raw_html)


def pipeline_home(request):
        return HttpResponse("Pipeline Home Page")


# TODO: WHAT ABOUT STATUS?
