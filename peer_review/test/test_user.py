from django.core.urlresolvers import reverse
from django.test import TestCase, Client

# from peer_review.models import User

from peer_review.views import *
import json


class UserTests(TestCase):
    def test_test(self):
        """
        2 + 2 should equal 4
        """
        ans = 2 + 2
        self.assertEqual(ans, 4)

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('b@bob.com', 'bob', 'bob', user_id=str(1234), surname="bob", initials="B")
        self.user = User.objects.create_user('j@joe.com', 'joe', 'joe', user_id=str(5678), surname="Joe", initials="J")
        User.objects.create_superuser('admin@admin.com', 'admin', user_id=str(1111))
        # self.user2 = User.objects.create_user('joe@joe.com', 'joe')

    # Simple test to see if questionAdmin is rendered
    def test_questionAdmin(self):
        self.client.login(username='1111', password='admin')
        url = reverse('questionAdmin')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'peer_review/questionAdmin.html')

    # Simple test to see if questionnaireAdmin is rendered
    def test_questionnaireAdmin(self):
        self.client.login(username='1111', password='admin')
        url = reverse('questionnaireAdmin')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'peer_review/questionnaireAdmin.html')

    def test_user_list(self):
        self.client.login(username='1111', password='admin')
        url = reverse('userAdmin')
        response = self.client.get(url, follow=True)
        self.assertIn(self.user, response.context['users']())

    # Unit Test
    def test_get_user(self):
        # Tests if current user is recognised
        # print("--- get_user Test ---\n")
        self.client.login(username='1111', password='admin')
        response = self.client.get('/accountDetails/1234')
        request = response.wsgi_request
        logged_user = json.loads(get_user(request, request.user.user_id).content.decode())
        expected_user = json.loads(get_user(request, "1111").content.decode())  # Joe user_id
        # print("Logged user: " + str(logged_user))
        # print("Expected user: " + str(expected_user))
        self.assertEqual(logged_user, expected_user)
        # print("\n--- END ---\n")

    def test_authentication(self):
        # Test redirection when access is granted and denied
        # print("--- Authentication Test ---\n")
        self.client.login(username='5678', password='joe')
        response = self.client.get('/accountDetails/')
        # print("Granted Status Code: " + str(response.status_code))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'peer_review/accountDetails.html')
        # Logout and try false details
        self.client.logout()
        self.client.login(username='1234', password='bobby')
        response = self.client.get('/accountDetails/')
        # print("Denied Status Code: " + str(response.status_code))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
        # self.assertTemplateUsed(response, 'peer_review/userError.html')
        # print("\n--- END ---\n")