from django.core.mail import send_mail
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Contact, BlogPost, Project, Testimonial
from .serializers import ContactSerializer, BlogPostSerializer, ProjectSerializer, TestimonialSerializer

# A ViewSet for creating contacts and sending email notifications.
# It only allows the 'create' (POST) action.
class ContactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny] # Anyone can submit the form

    def perform_create(self, serializer):
        # Save the contact instance
        contact_instance = serializer.save()

        # Send an email notification
        subject = f"New Contact Form Submission from {contact_instance.name}"
        message = f"Name: {contact_instance.name}\n" \
                  f"Email: {contact_instance.email}\n" \
                  f"Message: {contact_instance.message}"
        from_email = 'your-website@example.com'  # Use a no-reply or info email
        recipient_list = ['your-predefined-email@example.com']  # CHANGE THIS to your email

        send_mail(subject, message, from_email, recipient_list)


# A read-only ViewSet that returns the 4 latest blog posts.
class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Order by creation date (descending) and take the first 4
        return BlogPost.objects.all().order_by('-created_at')[:4]


# A read-only ViewSet for projects with a custom action for the latest projects.
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # The default list endpoint will return all projects
        return Project.objects.all().order_by('-created_at')

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        An extra endpoint at /api/projects/latest/ that returns the 4 latest projects.
        """
        latest_projects = self.get_queryset()[:4]
        serializer = self.get_serializer(latest_projects, many=True)
        return Response(serializer.data)


# A read-only ViewSet that returns the 4 latest testimonials.
class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Order by creation date (descending) and take the first 4
        return Testimonial.objects.all().order_by('-created_at')[:4]