"""cabunicrisis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from assembly.views import pipeline_home, job_status
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from cabunicrisis.core import views as core_views
	
urlpatterns = [
	#path('admin-xyzzy/', admin.site.urls),
	#path('home/', home, name = 'home_page'),
	path('', core_views.home, name = 'home'),
	path('home/', core_views.home, name = 'home'),
	path('assembly/', include('assembly.urls')),
	#Pipeline is kept in Genome Assembly because that's the first component of the pipeline.
	path('pipeline/', pipeline_home, name = 'pipeline_home'),
	path('status/', job_status, name = 'job_status'),
	path('prediction/', include('prediction.urls')),
]