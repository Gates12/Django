from django.contrib import admin  # Import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, SpamReportViewSet, RegisterView  # Import the RegisterView

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'spam', SpamReportViewSet, basename='spamreport')

# Add the router and the register endpoint to the URLs
urlpatterns = [
    path('admin/', admin.site.urls),  # Add admin URL
    path('register/', RegisterView.as_view(), name='register'),  # Add the register URL
    path('', include(router.urls)),  # Include the router's URLs
]
