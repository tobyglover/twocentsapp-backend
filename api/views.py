from django.shortcuts import render
from django.http import HttpResponse

from .models import Users

import hashlib
from datetime import datetime
import json

# Create your views here.

def index(request):
	return HttpResponse("You're at the api index.")

def createNewUser(request):
	returnContent = {}

	if "deviceId" in request.GET:
		deviceId = request.GET.get("deviceId")
		userKey = hashlib.sha224(deviceId + datetime.utcnow().isoformat()).hexdigest()

		if "username" in request.GET: # THIS MAY BE A HUGE SECURITY VULNERABILITY
			newUser = Users(userKey=userKey, username=request.GET.get(username))
		else:
			newUser = Users(userKey=userKey)
		newUser.save()

		returnContent["statusCode"] = 200
		returnContent["userKey"] = userKey
	else:	
		returnContent["statusCode"] = 400
		returnContent["reason"] = "No deviceId found."
	
	return HttpResponse(json.dumps(returnContent), status=returnContent["statusCode"])

def createNewPoll(request, userKey):
	returnContent = {}

	return