from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('studies.urls')),
    path('prayer/', include('prayer.urls')),
    path('journal/', include('journal.urls')),
    path('announcements/', include('announcements.urls')),
    path('growth/', include('growth.urls')),
    path('', include('core.urls')),
]
