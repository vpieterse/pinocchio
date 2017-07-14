from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from peer_review.view.maintainTeam import maintain_team, get_teams_for_round, change_user_team_for_round, \
    change_team_status, submit_team_csv, get_teams
from peer_review.view.questionAdmin import save_question, edit_question, question_admin, delete_question
from peer_review.view.questionnaire import save_questionnaire_progress, get_responses
from peer_review.view.questionnaireAdmin import save_questionnaire, questionnaire_preview, delete_questionnaire, \
    questionnaire_admin, edit_questionnaire
from peer_review.view.roundManagement import maintain_round
from peer_review.view.userAdmin import submit_csv
from peer_review.view.userFunctions import user_reset_password, active_rounds, get_team_members, account_details, \
    member_details
from peer_review.view.userManagement import forgot_password
import peer_review.view.userManagement
from peer_review import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls), name='admin'),

    url(r'^forgotPassword', forgot_password,
        name='forgotPassword'),
    url(r'^login/resetPass', user_reset_password,
        name='resetPass'),
    url(r'^recoverPassword/(?P<key>.*)', views.recover_password,
        name='recoverPassword'),

    url(r'^changePassword/', views.change_password, name='changePassword'),

    url(r'^maintainRound/$', maintain_round, name='maintainRound'),
    url(r'^createRound/$', views.create_round, name='createRound'),

    url(r'^maintainTeam/$', maintain_team, name='maintainTeam'),
    # url(r'^maintainTeam/(?P<round_pk>[0-9]+)/?$', views.maintain_team, name='maintainTeamR'),

    url(r'^getQuestionnaireForTeam/$', views.get_questionnaire_for_team,
        name='getQuestionnaireForTeam'),

    url(r'^questionnaire/(?P<round_pk>[0-9]+)/?$', peer_review.view.questionnaire.questionnaire, name='questionnaire'),
    url(r'^questionnaire/saveProgress', save_questionnaire_progress,
        name='saveQuestionnaireProgress'),
    url(r'^questionnaire/getResponses', get_responses, name='getResponses'),
    url(r'^login/$', views.login, name='login'),
    # url(r'^questionnaire/(?P<questionnaire_pk>[0-9]+)/?$', views.questionnaire, name='questionnaire'),
    url(r'^activeRounds/$', active_rounds, name='activeRounds'),
    url(r'^teamMembers/$', get_team_members, name='teamMembers'),
    url(r'^accountDetails/$', account_details, name='accountDetails'),
    url(r'^accountDetails/(?P<user_id>[a-zA-Z0-9]+)/?$', member_details, name='memberDetails'),

    url(r'^$', views.index, name='index'),
    url(r'^userAdmin/submitForm/?$', peer_review.view.userManagement.submit_new_user_form,
        name='submitUserForm'),
    url(r'^userAdmin/submitCSV/$', peer_review.view.userAdmin.submit_csv, name='submitCSV'),
    url(r'^userAdmin/delete/$', views.user_delete, name='userDelete'),
    url(r'^userAdmin/userProfile/(?P<user_id>[0-9a-zA-Z]+)/?$', views.user_profile, name="userProfile"),
    url(r'^userAdmin/update/(?P<user_id>[0-9a-zA-Z]+)/?$',
        peer_review.view.userManagement.user_update,
        name='userUpdate'),
    # url(r'^userAdmin/resetPassword/(?P<userId>[0-9a-zA-Z]+)/?$',
    # views.reset_password, name='resetPassword'),
    url(r'^userAdmin/updateEmail/$', views.update_email, name='updateEmail'),
    url(r'^userAdmin/$', views.user_list, name='userAdmin'),

    url(r'^questionAdmin/save', save_question, name='saveQuestion'),
    url(r'^questionAdmin/delete', delete_question, name='deleteQuestion'),
    url(r'^questionAdmin/edit/(?P<question_pk>[0-9]+)/?$', edit_question, name='editQuestion'),
    url(r'^questionAdmin', question_admin, name='questionAdmin'),

    url(r'^questionnaireAdmin/save$', save_questionnaire, name='saveQuestionnaire'),
    url(r'^questionnaireAdmin/edit/(?P<questionnaire_pk>[0-9]+)/?$', edit_questionnaire,
        name='editQuestionnaire'),
    url(r'^questionnairePreview/(?P<questionnaire_pk>[0-9]+)/?$', questionnaire_preview,
        name='previewQuestionnaire'),
    url(r'^questionnaireAdmin/delete', delete_questionnaire, name='deleteQuestionnaire'),
    url(r'^questionnaireAdmin/$', questionnaire_admin, name='questionnaireAdmin'),

    url(r'^maintainRound/dump/?$', views.round_dump, name='dumpRound'),
    url(r'^maintainRound/delete/$', views.round_delete, name='deleteRound'),
    url(r'^maintainRound/update/(?P<round_pk>[0-9]+)/?$', views.round_update, name='updateRound'),
    url(r'^maintainTeam/getTeamsForRound/(?P<round_pk>[0-9]+)/?$', get_teams_for_round,
        name='getTeamsForRound'),
    url(r'^maintainTeam/getQuestionnaireForRound/(?P<round_pk>[0-9]+)/?$',
        views.get_questionnaire_for_round,
        name='getQuestionnaireRound'),
    url(
        r'^maintainTeam/changeUserTeamForRound/(?P<round_pk>[0-9]+)/(?P<user_id>[0-9a-zA-Z]+)/(?P<team_name>[a-zA-Z0-9]+)/?$',
        change_user_team_for_round, name='changeUserTeamForRound'),
    url(r'^maintainTeam/getTeams/?$', get_teams, name='getTeams'),
    url(r'^maintainTeam/changeTeamStatus/(?P<team_pk>[0-9]+)/(?P<status>[a-zA-Z0-9]+)/?$',
        change_team_status, name='changeTeamStatus'),
    url(r'^maintainTeam/submitTeamCSV/$', submit_team_csv, name='submitTeamCSV'),
    url(r'^report/?$', views.report, name='report'),
    url(r'^report/getUser/(?P<user_id>[0-9a-zA-Z]+)/?$', views.get_user, name='getUserReport'),
    url(r'^login/auth/$', views.auth, name='auth'),

    url(r'^maintainRound/delete/$', views.round_delete),
    url(r'^maintainRound/(?P<error>[0-9]+)/?$', views.maintain_round_with_error,
        name='maintainRoundWithError'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'peer_review.view.errorViews.page_not_found'
handler500 = 'peer_review.view.errorViews.page_not_found'
