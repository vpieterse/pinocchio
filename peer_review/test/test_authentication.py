from datetime import datetime, timezone, timedelta
from django.core.urlresolvers import reverse
from django.test import TestCase
from peer_review.models import User, Questionnaire, RoundDetail, TeamDetail, Question, QuestionType, QuestionGrouping


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('joe@joe.com', 'joe', 'joe', userId=str(5678), surname="Joe", initials="J")
        self.admin = User.objects.create_superuser('admin@admin.com', 'admin', userId=str(1111))
        self.questionnaire = Questionnaire.objects.create(intro='Hello, this is a question',
                                                          label='This is the description')
        self.question = Question.objects.create(questionText="Hey I'm a question",
                                                questionLabel="I'm the label",
                                                pubDate=datetime.now(timezone(timedelta(hours=2))),
                                                questionType=QuestionType.objects.create(name="Rank"),
                                                questionGrouping=QuestionGrouping.objects.create(grouping="ALL"))
        start_date = datetime.now(timezone(timedelta(hours=2)))
        end_date = datetime.now(timezone(timedelta(hours=2)))
        self.round = RoundDetail.objects.create(name='test round', questionnaire=self.questionnaire,
                                                startingDate=start_date, endingDate=end_date,
                                                description='Hey there, we have a round')
        self.team = TeamDetail.objects.create(user=self.user, roundDetail=self.round, teamName="Red")

    def test_admin_authentication(self):
        # pages = ['resetPassword'] # these are pages that need to be included once those pages are finished
        admin_pages = ['maintainRound', 'createRound', 'maintainTeam', 'submitUserForm', 'submitCSV',
                       'userDelete', 'userUpdate|userId='+str(self.user.userId),
                       'updateEmail', 'userAdmin', 'saveQuestion', 'deleteQuestion',
                       'editQuestion|question_pk='+str(self.question.pk),
                       'questionAdmin', 'saveQuestionnaire',
                       'editQuestionnaire|questionnaire_pk='+str(self.questionnaire.pk),
                       'previewQuestionnaire|questionnaire_pk='+str(self.questionnaire.pk),
                       'deleteQuestionnaire', 'questionnaireAdmin', 'dumpRound',
                       'getTeamsForRound|round_pk='+str(self.round.pk),
                       'getQuestionnaireRound|round_pk='+str(self.round.pk),
                       'changeUserTeamForRound|round_pk='+str(self.round.pk) +
                       '|userId='+str(self.user.userId) +
                       '|team_name='+str(self.team.teamName), 'getTeams',
                       'changeTeamStatus|team_pk='+str(self.team.pk)+'|status=C',
                       'submitTeamCSV', 'report', 'getUserReport|userId='+str(self.user.userId),
                       'maintainRoundWithError|error=2',
                       'deleteRound|round_pk='+str(self.round.pk), 'updateRound|round_pk='+str(self.round.pk)]
        # print("not logged in")
        self.client.logout()
        # NOT LOGGED IN
        # This should allow visitor pages and not allow user pages or admin pages
        self.check_pages_blocked(admin_pages)

        # print("logged in with user")
        self.client.login(username='5678', password='joe')
        # LOGGED IN AS USER
        # This should allow user pages and not allow admin pages
        self.check_pages_blocked(admin_pages)

    def test_user_authentication(self):
        self.client.logout()
        user_pages = ['userProfile|userId='+str(self.user.userId),
                      'getQuestionnaireForTeam', 'questionnaire|round_pk='+str(self.round.pk),
                      'saveQuestionnaireProgress', 'getResponses',
                      'activeRounds', 'teamMembers', 'accountDetails']
        # NOT LOGGED IN
        # This should allow visitor pages and not allow user pages or admin pages
        self.check_pages_blocked(user_pages)

    def check_pages_blocked(self, pages):
        for page in pages:
            arg_split = page.split("|")
            page = arg_split[0]
            arguments = {}
            for args in arg_split[1:]:
                name_value = args.split("=")
                arguments[name_value[0]] = name_value[1]
            if len(arguments) > 0:
                response = self.client.get(reverse(page, kwargs=arguments))
            else:
                response = self.client.get(reverse(page))
            if response.status_code == 302:
                # print("When we go to " + page + ", we are redirected to " + response.url)
                self.assertRedirects(response, '/login/')
            else:
                # print(page + str(response.status_code))
                self.assertEquals(response.status_code, 403)