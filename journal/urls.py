from django.urls import path

from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.journal_home, name='journal_home'),
    path('new/', views.new_entry, name='new_entry'),
    path('<int:pk>/', views.journal_detail, name='journal_detail'),
]
