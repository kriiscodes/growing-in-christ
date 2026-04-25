from django.urls import path

from . import views

app_name = 'growth'

urlpatterns = [
    path('check-in/', views.checkin, name='checkin'),
    path('takeaway/', views.takeaway, name='takeaway'),
    path('midweek-reflection/', views.midweek_reflection, name='midweek_reflection'),
    path('history/', views.growth_history, name='growth_history'),
]
