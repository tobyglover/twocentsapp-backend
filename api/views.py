from django.shortcuts import render
from django.http import HttpResponse

from .models import Users, Polls, PollOptions

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

		if "username" in request.GET:
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

	if {'question', 'lng', 'lat'} <= set(request.GET):
		try:
			user = Users.objects.get(userKey=userKey)

			newPoll = Polls(user=user, question=request.GET.get("question"), loc_lat=request.GET.get("lat"), loc_lng=request.GET.get("lng"))
			newPoll.save()
			newPoll.pollKey = hashlib.sha224(str(newPoll.id) + datetime.utcnow().isoformat()).hexdigest()
			newPoll.save()

			# Temporary: For MVP, just yes or no. Eventually user will be able to make their own options.
			yes = PollOptions(poll=newPoll, option="Yes").save()
			no = PollOptions(poll=newPoll, option="No").save()

			returnContent["statusCode"] = 200
			returnContent["pollId"] = newPoll.pollKey

		except Users.DoesNotExist:
			returnContent["statusCode"] = 403
			returnContent["reason"] = "User does not exist."
	else:
		returnContent["statusCode"] = 400
		returnContent["reason"] = "Not all data given."

	return HttpResponse(json.dumps(returnContent), status=returnContent["statusCode"])