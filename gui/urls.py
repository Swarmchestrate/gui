"""
URL configuration for gui project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('new-capacity/', views.CapacityEditorFormView.as_view(), name='new_capacity'),
    path('new-cloud-capacity/', views.CloudCapacityEditorFormView.as_view(), name='new_cloud_capacity'),
    path('new-edge-capacity/', views.EdgeCapacityEditorFormView.as_view(), name='new_edge_capacity'),
    path('new-application/', views.ApplicationEditorFormView.as_view(), name='new_application'),
]
