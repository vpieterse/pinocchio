from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from peer_review import views

urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^fileUpload', views.fileUpload, name='fileUpload'),
                  url(r'^createQuestion/$', views.createQuestion, name='createQuestion'),
                  url(r'^maintainRound/$', views.maintainRound, name='maintainRound'),
                  
                  url(r'^maintainTeam/$', views.maintainTeam, name='maintainTeam'),
                  url(r'^questionnaireAdmin/$', views.questionnaireAdmin, name='questionnaireAdmin'),
                  url(r'^questionnaireAdmin/saveQuestionnaire/$', views.saveQuestionnaire, name='saveQuestionnaire'),
                  url(r'^questionnaireAdmin/getQuestionnaireList/$', views.getQuestionnaireList, name='getQuestionnaireList'),
                  url(r'^questionnaireAdmin/getQuestionnaire/(?P<qPk>[0-9]+)/?$', views.getQuestionnaire, name='getQuestionnaire'),
                  url(r'^questionnaireAdmin/deleteQuestionnaire/(?P<qPk>[0-9]+)/?$', views.deleteQuestionnaire, name='deleteQuestionnaire'),

		      url(r'^questionnaire/$', views.userError, name='userError'),
		      url(r'^questionnaire/(?P<questionnairePk>[0-9]+)/?$', views.questionnaire, name='questionnaire'),

                  url(r'^$', views.index, name='index'),
                  url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
                  url(r'^userAdmin/submitForm/?$', views.submitForm),
                  url(r'^userAdmin/submitCSV/$', views.submitCSV, name="submitCSV"),
                  url(r'^userAdmin/delete/(?P<userPk>[0-9]+)/?$', views.userDelete),
                  url(r'^userAdmin/update/(?P<userPk>[0-9]+)/?$', views.userUpdate),
                  url(r'^userAdmin/resetPassword/(?P<userPk>[0-9]+)/?$', views.resetPassword),
                  url(r'^userAdmin/$', views.userList),
                  url(r'^questionAdmin/delete/$', views.questionDelete, name='questionDelete'),
                  url(r'^questionAdmin/getQuestion/$', views.getQuestion, name = 'getQuestion'),
                  url(r'^questionAdmin/getQuestionList/$', views.getQuestionList, name = 'getQuestionList'),
                  url(r'^questionAdmin/getChoices/$', views.getChoices, name = 'getChoices'),
                  url(r'^questionAdmin/getRank/$', views.getRank, name = 'getRank'),
                  url(r'^questionAdmin/getRates/$', views.getRates, name = 'getRates'),
                  url(r'^questionAdmin/getFreeformItems/$', views.getFreeformItems, name = 'getFreeformItems'),
                  url(r'^questionAdmin', views.questionAdmin, name='questionAdmin'),
                  url(r'^maintainRound/delete/(?P<roundPk>[0-9]+)/?$', views.roundDelete),
                  url(r'^maintainRound/update/(?P<roundPk>[0-9]+)/?$', views.roundUpdate),
                  url(r'^maintainTeam/getTeamsForRound/(?P<roundPk>[0-9]+)/?$', views.getTeamsForRound),
                  url(r'^maintainTeam/changeUserTeamForRound/(?P<roundPk>[0-9]+)/(?P<userPk>[0-9]+)/(?P<teamName>[a-zA-Z0-9]+)/?$', views.changeUserTeamForRound),
                  url(r'^maintainTeam/getTeams/$', views.getTeams),
                  url(r'^maintainTeam/changeTeamStatus/(?P<teamPk>[0-9]+)/(?P<status>[a-zA-Z0-9]+)/?$', views.changeTeamStatus),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
