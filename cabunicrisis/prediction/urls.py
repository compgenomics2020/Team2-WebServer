from django.conf.urls import url
from django.urls import path
from .views import prediction_home, prediction_upload_files

urlpatterns = [
	path('home/', prediction_home, name = "prediction_home"),
	path('upload/', prediction_upload_files, name = "prediction_upload_files"),
]