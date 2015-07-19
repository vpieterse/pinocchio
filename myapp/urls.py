from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /myapp/
    url(r'^list', views.list, name='list'),
    url(r'^questionAdmin', views.questionAdmin, name='questionAdmin'),

]