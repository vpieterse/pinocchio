from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /peer_review/
    url(r'^$', views.index, name='index'),
    # ex: /peer_review/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail')

]