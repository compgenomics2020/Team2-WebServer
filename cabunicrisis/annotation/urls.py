from django.conf.urls import url
from django.urls import path
from .views import annotation_home, pipeline_home

urlpatterns = [
	path('home/', annotation_home, name = "annotation_home"),
]
