from django.conf.urls import url
from . import views

app_name = 'api'
urlpatterns = [
	# ex: /api/
    url(r'^$', views.index, name="index"),
    # ex: /api/createNewUser/
    url(r'^createNewUser/$', views.createNewUser, name="CreateNewUser")
]
