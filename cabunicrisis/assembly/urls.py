from django.conf.urls import url
from django.urls import path
from .views import assembly_home, pipeline_home, assembly_upload_files

urlpatterns = [
	path('home/', assembly_home, name = "assembly_home"),
	path('upload/', assembly_upload_files, name = "assembly_upload_files"),
]