from django.shortcuts import render
from django.http import HttpResponse

from .models import Users

# Create your views here.

def index(request):
	return HttpResponse("You're at the api index.")

def createNewUser(request):
	users = Users.objects.all().order_by('-pk')
	if users.count() == 0: #table is empty
		pk = 0
	else:
		pk = users[0].pk

	pk += 1 # get the next one

	

	return HttpResponse("Hello, world. You're at the createNewUSer index.")