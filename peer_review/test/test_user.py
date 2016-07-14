from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from peer_review.models import User

from peer_review.views import *
import json

#
#from django.test.utils import setup_test_environment
#setup_test_environment()
#


class UserTests(TestCase):
    def test_test(self):
        """
        2 + 2 should equal 4
        """
        ans = 2 + 2
        self.assertEqual(ans, 4)

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('bob@bob.com', 'bob', userId=str(1234), surname="bob", initials="B")
        self.user = User.objects.create_user('joe@joe.com', 'joe', userId=str(5678), surname="Joe", initials="J")
        #self.user2 = User.objects.create_user('joe@joe.com', 'joe')

    # Simple test to see if questionAdmin is rendered
    def test_questionAdmin(self):
        self.client.login(username='bob@bob.com', password='bob')
        url = reverse('questionAdmin')
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'peer_review/questionAdmin.html')

    # Simple test to see if questionnaireAdmin is rendered
    def test_questionnaireAdmin(self):
        self.client.login(username='bob@bob.com', password='bob')
        url = reverse('questionnaireAdmin')
        response = self.client.get(url, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'peer_review/questionnaireAdmin.html')

    def test_user_list(self):
        self.client.login(username='bob@bob.com', password='bob')
        url = reverse('userAdmin')
        response = self.client.get(url, follow = True)
        print(response.context['users']())
        self.assertIn(self.user, response.context['users']())

    # Unit Test
    def test_get_user(self):
        # Tests if user logged in, if not checked if error page rendered correctly
        self.client.login(username='joe@joe.com', password='joe')
        response = self.client.get('/accountDetails/1234')
        request = response.wsgi_request
        print("Status Code: " + str(response.status_code))
        if response.status_code == 200:
            print(json.loads(get_user(request, request.user.userId).content.decode()))
        else:
            self.assertTemplateUsed(response, 'peer_review/userError.html')