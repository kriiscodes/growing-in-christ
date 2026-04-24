from django.urls import path

from . import views

app_name = 'prayer'

urlpatterns = [
    path('', views.prayer_home, name='prayer_home'),
    path('new/', views.new_prayer, name='new_prayer'),
    path('<int:pk>/mark-answered/', views.mark_answered, name='mark_answered'),
]
