from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	user = models.CharField(max_length=200)
	created = models.DateTimeField()
	username = models.CharField(max_length=100)

class Poll(models.Model):
	poll = models.CharField(max_length=200)
	user = models.CharField(max_length=200)
	question = models.CharField(max_length=500)
	loc_lat = models.DecimalField(max_digits=9, decimal_places=6)
	loc_long = models.DecimalField(max_digits=9, decimal_places=6)
	created = models.DateTimeField()

class Votes(models.Model):
	poll = models.CharField(max_length=200)
	user = models.CharField(max_length=200)
	vote = models.IntegerField()
	created = models.DateTimeField()