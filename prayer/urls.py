from django.urls import path

from . import views

app_name = 'prayer'

urlpatterns = [
    path('', views.prayer_home, name='prayer_home'),
    path('new/', views.new_prayer, name='new_prayer'),
    path('<int:pk>/', views.prayer_detail, name='prayer_detail'),
    path('<int:pk>/edit/', views.edit_prayer, name='edit_prayer'),
    path('<int:pk>/delete/', views.delete_prayer, name='delete_prayer'),
    path('<int:pk>/mark-answered/', views.mark_answered, name='mark_answered'),
]
