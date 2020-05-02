from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import FunctionalAnnotation
from assembly.models import User
from .pipeline import main, process_in_directory
import uuid
import os
import threading
import queue

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
        if not os.path.exists(dir_data):
            os.mkdir(dir_data)

        #Creating a directory for user.
        dir_user = os.path.join(dir_data, user_uuid)
        os.mkdir(dir_user)

        #For input and output.
        input_dir = os.path.join(dir_user, 'input')
        output_dir = os.path.join(dir_user, 'output')

        os.mkdir(input_dir)
        os.mkdir(output_dir)

        #For sorting input into faa/fna/gff dirs
        fna_dir = os.path.join(input_dir, 'fna')
        faa_dir = os.path.join(input_dir, 'faa')
        gff_dir = os.path.join(input_dir, 'gff')

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

        #Accessing and saving the files sent by user.
        que = queue.Queue()
        input_files = request.FILES.getlist('all-fa-files')
        [legitimate, message_or_numfiles] = process_in_directory(input_files, input_dir)
        if not legitimate:
            print(message_or_numfiles)
            raise Http404("Bad boy, come nicely; the right way!")

        else:
            model_object_functional_annotation = FunctionalAnnotation(user = model_object_user,
                input_dir = input_dir, graphs = os.path.join(output_dir, "plots"),
                output_dir = output_dir)
            model_object_functional_annotation.save()

            # Add to path so that we can run some tools
            pwd = os.getcwd()
            tmhmm_path = os.path.join(pwd, "annotation/tmhmm-2.0c/bin")
            if tmhmm_path not in os.environ["PATH"]:
                os.environ["PATH"] += tmhmm_path
            signalp_path = os.path.join(pwd, "annotation/signalp-5.0b/bin")
            if signalp_path not in os.environ["PATH"]:
                os.environ["PATH"] += signalp_path

            pipeline_thread = threading.Thread(target=main, args=(input_dir, output_dir,
                "/projects/VirtualHost/predictb/databases/annotation", model_object_user,
                model_object_functional_annotation,))
            pipeline_thread.start()

            raw_html = render(request, 'annotation/annotation_homepage.html', {'uuid_data': user_uuid, 'number_of_files': message_or_numfiles})
            return HttpResponse(raw_html)


def pipeline_home(request):
        return HttpResponse("Pipeline Home Page")


# TODO: WHAT ABOUT STATUS?
