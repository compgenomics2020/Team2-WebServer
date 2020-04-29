from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import Input_Files_contigs,Blast_Results,Coding_Rename_Path,Plasmids_Output,NC_Aragon,NC_Barrnap 
from assembly.models import User
from .backbone import main as prediction_main
#from .models import Input_Files
import uuid
import os

# Create your views here.

def prediction_home(request):
        #Landing page of Gene Prediction isolated functionality.
        #Upload files forms.
        if request.method == 'GET':
                raw_html = render(request, 'prediction/prediction.html')
                response = HttpResponse(raw_html)
                return response



        if request.method == 'POST':
        #Create a UUID for user.
                user_uuid = str(uuid.uuid4())
                #Directory names.
                dir_data = 'prediction/data/'
                dir_user = dir_data + user_uuid + '/'
                dir_contig = dir_user + '/' + 'contigs/'
                dir_output=dir_user+'/'+'output'
                #Creating a directory for user.
                os.mkdir(dir_user)
                #Creating a directory for fasta files.
                os.mkdir(dir_contig)
                #Creating a directory for output folder
                os.mkdir(dir_output)
                #Creating a directory for blast in output folder
                dir_blast=dir_output+"/blast"
                #Creating a directory for known_unknown in output folder
                dir_known_unknown=dir_output+"/known_unknown"
                #Creating a directory for aragon in output folder
                dir_aragon=dir_output+"/aragon"
                #Creating a directory for barnap in output folder
                dir_barrnap=dir_output+"/barrnap"

                os.mkdir(dir_blast)
                os.mkdir(dir_known_unknown)
                os.mkdir(dir_aragon)
                os.mkdir(dir_barrnap)

                #Getting user's email.
                email = request.POST['email']
                #Get number of files.
                number_of_files = 0

                model_object_user = User(uuid = user_uuid, email = email,if_pipeline=False)
                model_object_user.save()
                
                #Accessing and saving the files sent by user.
                for file in request.FILES.getlist('contig-files'):
                        with open(dir_contig + file.name, "wb") as f:
                                f.write(str(file.read()))
                                number_of_files+=1

                model_object_input_files_contig=Input_Files_contigs(user=model_object_user,type_choice="user_upload",contigs_user_path=dir_contig)
                model_object_input_files_contig.save()
                model_object_blast= Blast_Results(contigs_file_path=model_object_input_files_contig,path=dir_blast)
                model_object_blast.save()
                model_object_rename= Coding_Rename_Path(blast_file_path=model_object_blast,path=dir_known_unknown)
                model_object_rename.save()
                model_object_aragon= NC_Aragon(contigs_file_path=model_object_input_files_contig,path=dir_aragon)
                model_object_aragon.save()
                model_object_barrnap= NC_Barrnap(contigs_file_path=model_object_input_files_contig,path=dir_barrnap)
                model_object_barrnap.save()

                #Run Pipeline.
                prediction_main(model_object_user,model_object_rename,dir_output,"2",dir_contig,None,None,None,coding_tools="3")

                raw_html = render(request,'prediction/prediction.html' , {'uuid_data': user_uuid, 'number_of_files': number_of_files})
                return HttpResponse(raw_html)


def pipeline_home(request):
        return HttpResponse("Pipeline Home Page")
