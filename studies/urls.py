from django.urls import path

from . import views

app_name = 'studies'

urlpatterns = [
    path('weekly-word/', views.weekly_word, name='weekly_word'),
]
