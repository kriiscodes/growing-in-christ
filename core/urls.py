from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('service-worker.js', views.service_worker, name='service_worker'),
    path('manifest.webmanifest', views.manifest, name='manifest'),
    path('offline/', views.offline, name='offline'),
    path('overview/', views.leader_overview, name='leader_overview'),
    path('overview/<int:user_id>/', views.leader_member_detail, name='leader_member_detail'),
]
