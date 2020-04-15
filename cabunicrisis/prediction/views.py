from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import Input_Files
import uuid

# Create your views here.

def prediction_home(request):
        #Landing page of Gene Prediction isolated functionality.

        #Upload files forms.
        if request.method == 'GET':
                raw_html = render(request, 'prediction/prediction.html')
                response = HttpResponse(raw_html)
                return response

        if request.method == 'POST':
                user_uuid = uuid.uuid4()
                for file in request.FILES.getlist('contigs.fasta'):
                        with open("blah.txt", "w") as f:
                                f.write(str(file.read()))
                        #print(file.name)
                return HttpResponse("Yes")


def pipeline_home(request):
        return HttpResponse("Pipeline Home Page")
