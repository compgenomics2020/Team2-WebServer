from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('',views.index,name='index'),

	path('<int : usr_id>/',views.usr_view,name = 'usr_path')

	path('<int : usr_id>/assemblyResult_view',views.assemblyResult_view,name = 'assemblyResult_path')

]