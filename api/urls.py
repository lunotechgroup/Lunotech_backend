from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'contact', views.ContactViewSet, basename='contact')
router.register(r'blog', views.BlogPostViewSet, basename='blogpost')
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'testimonials', views.TestimonialViewSet, basename='testimonial')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]