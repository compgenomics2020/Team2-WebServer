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
#from assembly.views import home
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from cabunicrisis.core import views as core_views

    
urlpatterns = [
    #path('admin-xyzzy/', admin.site.urls),
    #path('home/', home, name = 'home_page'),
    #path('assembly/', include('assembly.urls')),
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.LoginView, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^uploads/simple/$', core_views.simple_upload, name='simple_upload'),
    url(r'^uploads/form/$', core_views.model_form_upload, name='model_form_upload'),
    url(r'^admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)