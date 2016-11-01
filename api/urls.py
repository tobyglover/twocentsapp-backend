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
    url(r'^createNewPoll/(?P<userKey>[a-zA-Z0-9_-.~]+)/$', views.createNewPoll, name="createNewPoll"),
    # ex: /api/getPolls/
    url(r'^getPolls/$', views.getPolls, name="getPolls"),
    url(r'^getPollsForUser/(?P<userKey>[a-zA-Z0-9_-.~]+)/$', views.getPollsForUser, name="getPollsForUser"),
    # ex: /api/voteOnPoll/<userKey>/<pollId>/
    url(r'^voteOnPoll/(?P<userKey>[a-zA-Z0-9_-.~]+)/(?P<pollId>[a-zA-Z0-9_-.~]+)/(?P<optionId>[a-zA-Z0-9_-.~]+)/$', views.voteOnPoll, name="getPolls")
]
