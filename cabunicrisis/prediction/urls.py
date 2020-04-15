from django.conf.urls import url
from django.urls import path
from .views import prediction_home, pipeline_home

urlpatterns = [
	path('home/', prediction_home, name = "prediction_home"),
	path('upload/', pipeline_home, name = "pipeline_home"),
]
