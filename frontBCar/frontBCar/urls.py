"""frontBCar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from bcarApp import views
from bcarApp.views import DownloadFileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('autoCar/', views.autoCar, name = 'autoCar'),
    path('baby/', views.baby, name = 'baby'),
    path('clothing/', views.clothing, name = 'clothing'),
    path('immovable/', views.immovable, name = 'immovable'),
    path('job/', views.job, name = 'job'),
    path('animal/', views.animal, name = 'animal'),
    path('service/', views.service, name = 'service'),
    path('electron/', views.electron, name = 'electron'),
    path('phone/', views.phone, name = 'phone'),
    path('Household/', views.Household, name = 'Household'),
    path('health/', views.health, name = 'health'),
    path('computer/', views.computer, name = 'computer'),
    path('device/', views.device, name = 'device'),
    path('download/', DownloadFileView.as_view(), name='download_file'),

]
