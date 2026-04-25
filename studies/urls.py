from django.urls import path

from . import views

app_name = 'studies'

urlpatterns = [
    path('weekly-word/', views.weekly_word, name='weekly_word'),
    path('archive/', views.archive, name='archive'),
    path('archive/<int:pk>/', views.archive_week, name='archive_week'),
]
