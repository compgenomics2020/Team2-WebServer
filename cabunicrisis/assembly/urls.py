from django.conf.urls import url
from django.urls import path
from .views import assembly_home, pipeline_home

urlpatterns = [
	path('home/', assembly_home, name = "assembly_home"),
]