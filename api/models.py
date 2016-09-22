from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	user_id = models.CharField(max_length=200)
	created = models.DateTimeField()
	username = models.CharField(max_length=100)

class Poll(models.Model):
	text = models.CharField(max_length=500)
	created = models.DateTimeField()
	poll_id = models.CharField(max_length=200)

class Votes(models.Model):
	poll_id = models.CharField(max_length=200)
	user_id = models.CharField(max_length=200)
	result = models.IntegerField()
	created = models.DateTimeField()