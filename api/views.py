from __future__ import division

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Users, Polls, PollOptions, Votes

from datetime import datetime, timedelta
import json
from math import asin, cos, degrees, radians
from hexahexacontadecimal import hhc
from random import randint

# Create your views here.

def index(request):
	return HttpResponse("You are at the api index")

def createNewUser(request):
	returnContent = {}

	newUser = None
	userKey = getRandomId("Users")

	if "username" in request.GET:
		username = request.GET.get("username")
		if usernameAvailable(username):
			newUser = Users(userKey=userKey, username=username)
		else:
			returnContent["statusCode"] = 400
			returnContent["reason"] = "Username is already taken"
	else:
		newUser = Users(userKey=userKey)

	if newUser != None:
		newUser.save()

		returnContent["statusCode"] = 200
		returnContent["userKey"] = userKey
	
	return JsonResponse(returnContent, status=returnContent["statusCode"])

def isUsernameAvailable(request):
	returnContent = {}

	if "username" in request.GET:
		if usernameAvailable(request.GET.get("username")):
			returnContent["available"] = True
		else:
			returnContent["available"] = False
		returnContent["statusCode"] = 200
	else:
		returnContent["statusCode"] = 400
		returnContent["reason"] = "No username provided."

	return JsonResponse(returnContent, status=returnContent["statusCode"])


def usernameAvailable(username):
	return Users.objects.filter(username=username).count() == 0

@csrf_exempt
def createNewPoll(request, userKey):
	returnContent = {}
	data = json.loads(request.body)
	if {'question', 'lng', 'lat'} <= set(data):
		try:
			user = Users.objects.get(userKey=userKey)

			newPoll = Polls(user=user, question=data.get("question"), loc_lat=data.get("lat"), loc_lng=data.get("lng"))
			newPoll.pollId = getRandomId("Polls")
			newPoll.save()

			# Temporary: For MVP, just yes or no. Eventually user will be able to make their own options.
			yes = PollOptions(poll=newPoll, option="Yes", optionId=getRandomId("PollOptions"))
			yes.save()
			no = PollOptions(poll=newPoll, option="No", optionId=getRandomId("PollOptions"))
			no.save()

			returnContent["statusCode"] = 200
			returnContent["pollId"] = newPoll.pollId

		except Users.DoesNotExist:
			returnContent["statusCode"] = 403
			returnContent["reason"] = "User does not exist."
	else:
		returnContent["statusCode"] = 400
		returnContent["reason"] = "Not all data given."

	return JsonResponse(returnContent, status=returnContent["statusCode"])

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

	return JsonResponse(returnContent, status=returnContent["statusCode"])

def getPolls(request):
	returnContent = {}
	if {'lng', 'lat', 'radius'} <= set(request.GET):

		polls = retrievePollsAtLocation(float(request.GET.get("lng")), float(request.GET.get("lat")), int(request.GET.get("radius")))
		# polls = Polls.objects.all().order_by("-created")

		returnContent["statusCode"] = 200
		returnContent["polls"] = formatPollData(polls);
	else:
		returnContent["statusCode"] = 403
		returnContent["reason"] = "lat/lng and radius not specified"

	return JsonResponse(returnContent, status=returnContent["statusCode"])

def getPollsForUser(request, userKey):
	returnContent = {}

	try:
		user = Users.objects.get(userKey=userKey);
		polls = Polls.objects.filter(user=user).order_by("-created")

		returnContent["statusCode"] = 200
		returnContent["polls"] = formatPollData(polls);

	except Users.DoesNotExist:
		returnContent["statusCode"] = 403
		returnContent["reason"] = "User does not exist."

	return JsonResponse(returnContent, status=returnContent["statusCode"])

def formatPollData(pollData):
	formattedData = []

	for poll in pollData:
		pollData = {"question": poll.question, "pollId": poll.pollId}

		curtime = datetime.utcnow()
		diff = curtime - poll.created.replace(tzinfo=None)

		pollData["createdAgo"] = int(diff.total_seconds())

		if poll.user.username != "":
			pollData["username"] = poll.user.username

		pollOptions = PollOptions.objects.filter(poll=poll)

		returnedVotes = {}
		for pollOption in pollOptions:
			returnedVotes[pollOption.option] = {"optionId": pollOption.optionId, "count": 0}

		votes = Votes.objects.filter(poll=poll)
		for vote in votes:
			returnedVotes[vote.vote.option]["count"] += 1

		pollData["votes"] = returnedVotes
		formattedData.append(pollData)

	return formattedData

# adapted from http://www.movable-type.co.uk/scripts/latlong-db.html
def retrievePollsAtLocation(lng, lat, radius):

	return Polls.objects.raw('''SELECT
						    	*, (
									6371 * acos (
									cos ( radians(%(lat)s) )
									* cos( radians( loc_lat ) )
									* cos( radians( loc_lng ) - radians(%(lng)s) )
									+ sin ( radians(%(lat)s) )
									* sin( radians( loc_lat ) ) )
								) AS distance
							FROM api_polls
							HAVING distance < %(radius)s
							ORDER BY created DESC
							LIMIT 100;
            				 ''', {"lat":lat, "lng":lng, "radius":radius})
	

	# maxLat = lat + degrees(radius / earthRadius)
	# minLat = lat - degrees(radius / earthRadius)
	# maxLng = lng + degrees(asin(radius / earthRadius) / cos(radians(lat)))
	# minLng = lng - degrees(asin(radius / earthRadius) / cos(radians(lat)))
	# return Polls.objects.raw('''SELECT * 
	# 							FROM (
	# 								SELECT *
	# 								FROM api_polls
	# 								WHERE loc_lat BETWEEN %(minLat)s AND %(maxLat)s
	# 								AND loc_lng BETWEEN %(minLng)s AND %(maxLng)s
	# 							) As FirstCut
	# 							WHERE acos(sin(%(lat)s)*sin(radians(loc_lat)) + cos(%(lat)s)*cos(radians(loc_lat))*cos(radians(loc_lng)-%(lng)s)) * %(earthRadius)s < %(radius)s
	# 							ORDER BY created DESC;
 #            				 ''', {"lat":lat, "lng":lng, "radius":radius, "maxLat":maxLat, "minLat":minLat, "maxLng":maxLng, "minLng":minLng, "earthRadius":earthRadius})

def getRandomId(modelObject):
	size = 8

	check = True
	while(check):
		rand = hhc(randint(0, 66**size))
		if modelObject == "Users":
			check = Users.objects.filter(userKey=rand).count() > 0
		elif modelObject == "PollOptions":
			check = PollOptions.objects.filter(optionId=rand).count() > 0
		elif modelObject == "Polls":
			check = Polls.objects.filter(pollId=rand).count() > 0
		else:
			return -1
		
	return rand



