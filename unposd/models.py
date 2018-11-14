# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Groups(models.Model):
	group_id = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=50)
	topic_count = models.IntegerField(default=0)
	iconserver = models.IntegerField(default=0)
	privacy = models.CharField(max_length=20)
	members = models.IntegerField(default=0)
	total_photos = models.IntegerField(default=0)
	iconfarm = models.IntegerField(default=0)
	user = models.CharField(max_length=30)

class Photos(models.Model):
	group_id = models.ForeignKey("Groups", null=True)
	photo_id = models.CharField(max_length=20, primary_key=True)
	title = models.CharField(max_length=50)
	views = models.IntegerField(default=0)
	datetaken = models.DateTimeField(blank=True)
	# dateuploaded = models.DateTimeField(blank=True)
	originalformat = models.CharField(max_length=10)
	iconserver = models.IntegerField(default=0)
	iconfarm = models.IntegerField(default=0)
	location = models.CharField(max_length=30)
	nsid = models.CharField(max_length=20)
	tags = models.CharField(max_length=100)
	user = models.CharField(max_length=30)
