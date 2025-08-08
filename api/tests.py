from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import BlogPost, Project

class APITests(APITestCase):

    def setUp(self):
        # Create 5 instances of each model to test the "latest 4" logic
        for i in range(5):
            BlogPost.objects.create(title=f'Blog Post {i}', content=f'Content {i}')
            Project.objects.create(title=f'Project {i}', description=f'Description {i}')

    def test_contact_form_submission(self):
        """
        Ensure we can create a new contact object and an email is sent.
        """
        url = reverse('contact-list')
        data = {'name': 'Test User', 'email': 'test@example.com', 'message': 'Hello there'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Test that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'New Contact Form Submission from Test User')

    def test_get_latest_blog_posts(self):
        """
        Ensure the blog endpoint returns only the 4 most recent posts.
        """
        url = reverse('blogpost-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # We created 5 posts, but the API should only return 4
        self.assertEqual(len(response.data), 4)
        # Check that the latest post (Post 4) is in the response
        self.assertEqual(response.data[0]['title'], 'Blog Post 4')

    def test_get_all_projects(self):
        """
        Ensure the main project endpoint returns all 5 projects.
        """
        url = reverse('project-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_get_latest_projects(self):
        """
        Ensure the custom 'latest' project endpoint returns only 4 projects.
        """
        url = reverse('project-latest') # This uses the custom action name
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['title'], 'Project 4')