from django.core.urlresolvers import reverse, resolve
from django.test import TestCase, Client
from django.utils import timezone

from peer_review.models import User, TeamDetail, RoundDetail

from peer_review.views import *
import json
import datetime


class MaintainTeamTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user('bob@bob.com', 'bob', 'bob', 'simons', userId=1)
        self.user2 = User.objects.create_user('joe@joe.com', 'joe', 'joe', 'simons', userId=2)
        self.admin = User.objects.create_superuser('admin', 'admin', userId=2)
        self.round1 = RoundDetail.objects.create(name='Round 1',
                                                 startingDate=datetime.datetime.now(tz=timezone.get_current_timezone()),
                                                 endingDate=datetime.datetime.now(tz=timezone.get_current_timezone()),
                                                 description='Test Round 1')
        self.round2 = RoundDetail.objects.create(name='Round 2',
                                                 startingDate=datetime.datetime.now(tz=timezone.get_current_timezone()),
                                                 endingDate=datetime.datetime.now(tz=timezone.get_current_timezone()),
                                                 description='Test Round 2')
        self.team1 = TeamDetail.objects.create(user=self.user1, roundDetail=self.round1, teamName='Team1', pk=123)
        self.team2 = TeamDetail.objects.create(user=self.user2, roundDetail=self.round1, teamName='Team2', pk=321)

    # Test that the user's team name is changed for the round
    def test_change_user_team_for_round(self):
        self.client.login(username='2', password='admin')

        # Change user1's teamName for round1 to 'Red'
        url = reverse('changeUserTeamForRound', kwargs={'round_pk': self.round1.pk,
                                                        'userId': self.user1.userId, 'team_name': 'Red'})
        response = self.client.get(url)
        # Check if there are no errors
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        team = TeamDetail.objects.filter(user_id=self.user1.userId).get(roundDetail_id=self.round1.pk)
        # Test that the teamName is 'Red'
        self.assertEqual(team.teamName, 'Red')

        # Change user1's teamName for round1 to 'Green'
        url = reverse('changeUserTeamForRound', kwargs={'round_pk': self.round1.pk,
                                                        'userId': self.user1.userId, 'team_name': 'Green'})
        response = self.client.get(url)
        # Check if there are no errors
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        team = TeamDetail.objects.filter(user_id=self.user1.userId).get(roundDetail_id=self.round1.pk)
        # Test that the teamName is 'Green'
        self.assertEqual(team.teamName, 'Green')

    def test_change_team_status(self):
        self.client.login(username='2', password='admin')
        team = TeamDetail.objects.create(roundDetail=self.round1, user=self.user2)
        url = reverse('changeTeamStatus', kwargs={'team_pk': team.pk, 'status': 'U'})

    def test_get_teams_for_round(self):
        self.client.login(username='2', password='admin')

        url = reverse("getTeamsForRound", kwargs={'round_pk': self.round1.pk})
        json_response = json.loads(self.client.get(url).content.decode())

        # Both teams should be in the JSON file as root keys
        self.assertIsNotNone(json_response[str(self.team1.pk)])
        self.assertIsNotNone(json_response[str(self.team2.pk)])

        # Both users should be in their respective teams
        json_response_team1 = json_response[str(self.team1.pk)]
        self.assertEqual(json_response_team1['teamName'], self.team1.teamName)
        self.assertEqual(json_response_team1['userId'], str(self.user1.pk))
        self.assertEqual(json_response_team1['status'], self.team1.status)

        json_response_team2 = json_response[str(self.team2.pk)]
        self.assertEqual(json_response_team2['teamName'], self.team2.teamName)
        self.assertEqual(json_response_team2['userId'], str(self.user2.pk))
        self.assertEqual(json_response_team2['status'], self.team2.status)
