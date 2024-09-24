from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('api/', include('api.urls')),  # Include the URLs from the 'api' app
]