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
        self.user = User.objects.create_user('bob@bob.com', 'bob')
        self.user2 = User.objects.create_user('joe@joe.com', 'joe')

    # Simple test to see if questionAdmin is rendered
    def test_questionAdmin(self):
        self.client.login(username='bob@bob.com', password='bob')
        url = reverse('questionAdmin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'peer_review/questionAdmin.html')

    # Simple test to see if questionnaireAdmin is rendered
    def test_questionnaireAdmin(self):
        self.client.login(username='bob@bob.com', password='bob')
        url = reverse('questionnaireAdmin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'peer_review/questionnaireAdmin.html')

    def test_user_list(self):
        self.client.login(username='bob@bob.com', password='bob')
        url = reverse('userAdmin')
        response = self.client.get(url)
        #print(response.context['users']())
        self.assertIn(self.user, response.context['users']())

    def test_get_user(self):
        self.client.login(username='bob@bob.com', password='bob')
        response = self.client.get('/users/')
        request = response.wsgi_request
        response2 = get_user(request, 1)
        print "User Email: " + response2.email.encode('ascii','ignore')
        print "H-Password: " + response2.password.encode('ascii','ignore')