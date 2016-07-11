from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from peer_review.models import User


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
        print(response.context['users']())
        self.assertIn(self.user, response.context['users']())
