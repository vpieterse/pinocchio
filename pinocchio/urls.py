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
                  url(r'^questionAdmin/update/$', views.questionUpdate, name='questionUpdate'),
                  url(r'^questionAdmin/delete/$', views.questionDelete, name='questionDelete'),
                  url(r'^questionAdmin/getQuestion/(?P<questionPk>[0-9]+)/?$', views.getQuestion),
                  url(r'^questionAdmin/getChoices/(?P<questionPk>[0-9]+)/?$', views.getChoices),
                  url(r'^questionAdmin/getRank/(?P<questionPk>[0-9]+)/?$', views.getRank),
                  url(r'^questionAdmin', views.questionAdmin, name='questionAdmin'),
                  url(r'^maintainRound/delete/(?P<roundPk>[0-9]+)/?$', views.roundDelete),
                  url(r'^maintainRound/update/(?P<roundPk>[0-9]+)/?$', views.roundUpdate),
                  url(r'^maintainTeam/getTeamsForRound/(?P<roundPk>[0-9]+)/?$', views.getTeamsForRound),
                  url(r'^maintainTeam/changeUserTeamForRound/(?P<roundPk>[0-9]+)/(?P<userPk>[0-9]+)/(?P<teamName>[a-zA-Z0-9]+)/?$', views.changeUserTeamForRound),
                  url(r'^maintainTeam/getTeams/$', views.getTeams),
                  url(r'^maintainTeam/changeTeamStatus/(?P<teamPk>[0-9]+)/(?P<status>[a-zA-Z0-9]+)/?$', views.changeTeamStatus),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
