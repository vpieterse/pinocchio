from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from peer_review import views

urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^fileUpload', views.file_upload, name='fileUpload'),

                  url(r'^maintainRound/$', views.maintain_round, name='maintainRound'),
                  url(r'^createRound/$', views.create_round, name='createRound'),

                  url(r'^maintainTeam/$', views.maintain_team, name='maintainTeam'),
                  url(r'^maintainTeam/(?P<round_pk>[0-9]+)/?$', views.maintain_team, name='maintainTeamR'),

                  url(r'^getQuestionnaireForTeam/$', views.get_questionnaire_for_team,
                      name='getQuestionnaireForTeam'),

                  url(r'^questionnaire/$', views.user_error, name='userError'),
                  url(r'^questionnaire/(?P<round_pk>[0-9]+)/?$', views.questionnaire, name='questionnaire'),
                  url(r'^questionnaire/saveProgress', views.save_questionnaire_progress,
                      name='saveQuestionnaireProgress'),
                  url(r'^questionnaire/getResponses', views.get_responses, name='getResponses'),
                  url(r'^login/$', views.login, name='login'),
                  url(r'^questionnaire/(?P<questionnaire_pk>[0-9]+)/?$', views.questionnaire, name='questionnaire'),
                  url(r'^activeRounds/$', views.active_rounds, name='activeRounds'),
                  url(r'^teamMembers/$', views.team_members, name='teamMembers'),
                  url(r'^accountDetails/(?P<user_id>[0-9]+)$', views.account_details, name='accountDetails'),

                  url(r'^$', views.index, name='index'),
                  url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
                  url(r'^userAdmin/submitForm/?$', views.submit_form),
                  url(r'^userAdmin/submitCSV/$', views.submit_csv, name="submitCSV"),
                  url(r'^userAdmin/userProfile/(?P<userId>[0-9]+)/?$', views.user_profile, name="userProfile"),
                  url(r'^userAdmin/delete/$', views.user_delete, name="userDelete"),
                  url(r'^userAdmin/update/(?P<userId>[0-9]+)/?$', views.user_update),
                  url(r'^userAdmin/resetPassword/(?P<userId>[0-9]+)/?$', views.reset_password),
                  url(r'^userAdmin/updateEmail/$', views.update_email),
                  url(r'^userAdmin/$', views.user_list, name='userAdmin'),

                  url(r'^questionAdmin/save', views.save_question, name='saveQuestion'),
                  url(r'^questionAdmin/delete', views.delete_question, name='deleteQuestion'),
                  url(r'^questionAdmin/edit/(?P<question_pk>[0-9]+)/?$', views.edit_question, name='editQuestion'),
                  url(r'^questionAdmin', views.question_admin, name='questionAdmin'),

                  url(r'^questionnaireAdmin/save$', views.save_questionnaire, name='saveQuestionnaire'),
                  url(r'^questionnaireAdmin/edit/(?P<questionnaire_pk>[0-9]+)/?$', views.edit_questionnaire,
                      name='editQuestionnairre'),
                  url(r'^questionnaireAdmin/delete', views.delete_questionnaire, name='deleteQuestionnaire'),
                  url(r'^questionnaireAdmin/$', views.questionnaire_admin, name='questionnaireAdmin'),

                  url(r'^maintainRound/dump/?$', views.round_dump),
                  url(r'^maintainRound/delete/(?P<round_pk>[0-9]+)/?$', views.round_delete),
                  url(r'^maintainRound/update/(?P<round_pk>[0-9]+)/?$', views.round_update),
                  url(r'^maintainTeam/getTeamsForRound/(?P<round_pk>[0-9]+)/?$', views.get_teams_for_round),
                  url(r'^maintainTeam/getQuestionnaireForRound/(?P<round_pk>[0-9]+)/?$', views.get_questionnaire_for_round),
                  url(
                      r'^maintainTeam/changeUserTeamForRound/(?P<round_pk>[0-9]+)/(?P<user_pk>[0-9]+)/(?P<team_name>[a-zA-Z0-9]+)/?$',
                      views.change_user_team_for_round),
                  url(r'^maintainTeam/getTeams/?$', views.get_teams),
                  url(r'^maintainTeam/changeTeamStatus/(?P<team_pk>[0-9]+)/(?P<status>[a-zA-Z0-9]+)/?$',
                      views.change_team_status),
                  url(r'^maintainTeam/submitTeamCSV/$', views.submit_team_csv, name="submitTeamCSV"),
                  url(r'^report/?$', views.report),
                  url(r'^report/getUser/(?P<userId>[0-9]+)/?$', views.get_user),
                  url(r'^login/auth/$', views.auth, name="auth"),

                  url(r'^maintainRound/(?P<error>[0-9]+)/?$', views.maintain_round_with_error,
                      name="maintainRoundWithError"),
                  url(r'^maintainRound/delete/(?P<round_pk>[0-9]+)/?$', views.round_delete),
                  url(r'^maintainRound/update/(?P<round_pk>[0-9]+)/?$', views.round_update),
                  url(r'^maintainRound/$', views.maintain_round, name='maintainRound'),
                  url(r'^createRound/$', views.create_round, name='createRound'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
