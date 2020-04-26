from django.conf.urls import url
from django.urls import path
from .views import assembly_home, pipeline_home, download_contig_files

urlpatterns = [
	path('home/', assembly_home, name = "assembly_home"),
	path('download/', download_contig_files, name = "download_contig_files")
]