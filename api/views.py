from django.shortcuts import render
from django.http import HttpResponse

from .models import Users, Polls, PollOptions, Votes

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
		userKey = hashlib.md5(deviceId + datetime.utcnow().isoformat()).hexdigest()

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
			newPoll.pollId = hashlib.md5(str(newPoll.id) + datetime.utcnow().isoformat()).hexdigest()
			newPoll.save()

			# Temporary: For MVP, just yes or no. Eventually user will be able to make their own options.
			yes = PollOptions(poll=newPoll, option="Yes")
			no = PollOptions(poll=newPoll, option="No")

			yes.save()
			yes.optionId = hashlib.md5(str(yes.id) + datetime.utcnow().isoformat()).hexdigest()
			yes.save()

			no.save()
			no.optionId = hashlib.md5(str(no.id) + datetime.utcnow().isoformat()).hexdigest()
			no.save()

			returnContent["statusCode"] = 200
			returnContent["pollId"] = newPoll.pollId

		except Users.DoesNotExist:
			returnContent["statusCode"] = 403
			returnContent["reason"] = "User does not exist."
	else:
		returnContent["statusCode"] = 400
		returnContent["reason"] = "Not all data given."

	return HttpResponse(json.dumps(returnContent), status=returnContent["statusCode"])

def voteOnPoll(request, userKey, pollId, optionId):
	returnContent = {}

	# Not implemented in the most efficient way.
	try:
		user = Users.objects.get(userKey=userKey)
		try:
			poll = Polls.objects.get(pollId=pollId)
			try:
				pollOption = PollOptions.objects.get(optionId=optionId)

				vote, created = Votes.objects.update_or_create(poll=poll, user=user, vote=pollOption)
				returnContent["statusCode"] = 200	

			except PollOptions.DoesNotExist:
				returnContent["statusCode"] = 403
				returnContent["reason"] = "Poll option does not exist."
		except Polls.DoesNotExist:
			returnContent["statusCode"] = 403
			returnContent["reason"] = "Poll does not exist."
	except Users.DoesNotExist:
		returnContent["statusCode"] = 403
		returnContent["reason"] = "User does not exist."

	return HttpResponse(json.dumps(returnContent), status=returnContent["statusCode"])

def getPolls(request):
	returnContent = {}
	if {'lng', 'lat', 'radius'} <= set(request.GET):
		# cheating, currently just returns all polls regardless of distance
		returnedPolls = []
		polls = Polls.objects.all()
		for poll in polls:
			pollData = {"question": poll.question, "created": poll.created.strftime("%s"), "pollId": poll.pollId}
			pollOptions = PollOptions.objects.filter(poll=poll)

			returnedVotes = {}
			for pollOption in pollOptions:
				returnedVotes[pollOption.option] = {"optionId": pollOption.optionId, "count": 0}

			votes = Votes.objects.filter(poll=poll)
			for vote in votes:
				returnedVotes[vote.vote.option]["count"] += 1

			pollData["votes"] = returnedVotes
			returnedPolls.append(pollData)

		returnContent["statusCode"] = 200
		returnContent["polls"] = returnedPolls
	else:
		returnContent["statusCode"] = 403
		returnContent["reason"] = "lat/lng and radius not specified"

	return HttpResponse(json.dumps(returnContent), status=returnContent["statusCode"])














