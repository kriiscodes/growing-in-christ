from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('service-worker.js', views.service_worker, name='service_worker'),
    path('manifest.webmanifest', views.manifest, name='manifest'),
    path('offline/', views.offline, name='offline'),
]
