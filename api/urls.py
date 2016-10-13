from django.conf.urls import url
from . import views

app_name = 'api'
urlpatterns = [
	# ex: /api/
    url(r'^$', views.index, name="index"),
    # ex: /api/createNewUser/
    url(r'^createNewUser/$', views.createNewUser, name="CreateNewUser"),
    url(r'^isUsernameAvailable/$', views.isUsernameAvailable, name="isUsernameAvailable"),
    # ex: /api/createNewPoll/<userKey>/
    url(r'^createNewPoll/(?P<userKey>[0-9a-f]+)/$', views.createNewPoll, name="createNewPoll"),
    # ex: /api/getPolls/
    url(r'^getPolls/$', views.getPolls, name="getPolls"),
    # ex: /api/voteOnPoll/<userKey>/<pollId>/
    url(r'^voteOnPoll/(?P<userKey>[0-9a-f]+)/(?P<pollId>[0-9a-f]+)/(?P<optionId>[0-9a-f]+)/$', views.voteOnPoll, name="getPolls")
]
