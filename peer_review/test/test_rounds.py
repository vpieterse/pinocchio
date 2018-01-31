from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from peer_review.models import RoundDetail
from peer_review.test.TestSetup import TestSetup


class RoundTests(TestCase):
    def test_test(self):
        """
        2 + 2 should equal 4
        """
        ans = 2 + 2
        self.assertEqual(ans, 4)

    def setUp(self):
        self.client = Client()
        self.ts = TestSetup()

    def test_round_dump(self):
        self.client.login(username='1111', password='admin')

        url = reverse('dumpRound')
        response = self.client.post(url, {'roundPk': self.ts.round2.id})

        self.assertEqual(response.status_code, 200)
        # data = json.loads(response.content.decode())
        content = response.content
        self.assertEquals(content, b'"ResponseID","Respondent","QuestionTitle","LabelTitle","SubjectUser","Answer"' +
                       b'\n"2","12345","I\'m the label","","6789","We have a different answer"' +
                       b'\n"4","12345","I\'m the label for the question","","6789","choice 2"' +
                       b'\n"6","12345","I\'m a label for this question","","6789","Bananas"\n')

    def test_round_create(self):
        self.client.login(username='1111', password='admin')

        url = reverse('createRound')
        response = self.client.get(url)
        self.assertIn(response.status_code, [302])

    def test_round_delete(self):
        self.client.login(username='1111', password='admin')
        url = reverse('deleteRound')
        response = self.client.post(url, {'pk': self.ts.round4.pk})
        self.assertEquals(response.status_code, 302)
        gone_round = RoundDetail.objects.filter(id=self.ts.round4.pk)
        self.assertEquals(len(gone_round), 0)

    def test_round_update(self):
        self.client.login(username='1111', password='admin')
        post_starting_date = '2016-06-27 11:12+02:00'
        post_description = 'New description, better than the old'
        post_questionnaire = 1
        post_name = 'A better round name'
        post_ending_date = '2016-06-29 11:12+02:00'
        response = self.client.post('/maintainRound/update/'+str(self.ts.round4.pk),
                                    {'startingDate': post_starting_date,
                                     'description': post_description,
                                     'questionnaire': post_questionnaire,
                                     'roundName': post_name,
                                     'endingDate': post_ending_date})
        round_test = RoundDetail.objects.get(pk=self.ts.round4.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(round_test.description, 'New description, better than the old')

