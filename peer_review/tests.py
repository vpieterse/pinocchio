from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class UserTests(TestCase):
	def test_test(self):
		"""
		2 + 2 should equal 4
		"""
		ans = 2 + 2
		self.assertEqual(ans, 4)

	def setUp(self):
		self.client = Client()
		self.client.login(username='admin@admin.com', password='admin')

	# Simple test to see if questionAdmin is rendered
	def test_questionAdmin(self):
		url = reverse('questionAdmin')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'peer_review/questionAdmin.html')
		print('questionAdmin rendered correctly')

	# Simple test to see if questionnaireAdmin is rendered
	def test_questionnaireAdmin(self):
		url = reverse('questionnaireAdmin')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'peer_review/questionnaireAdmin.html')
		print('questionnaireAdmin rendered correctly')
