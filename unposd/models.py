# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Groups(models.Model):
	''' Groups model '''

	group_id = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=50)
	topic_count = models.IntegerField(default=0)
	iconserver = models.IntegerField(default=0)
	privacy = models.CharField(max_length=20, null=True)
	members_count = models.IntegerField(default=0)
	total_photos = models.IntegerField(default=0)
	iconfarm = models.IntegerField(default=0)
	members = models.CharField(max_length=100, null=True)

class Photos(models.Model):
	''' Photos model '''

	group_id = models.CharField(max_length=30, null=True)
	photo_id = models.CharField(max_length=20, primary_key=True)
	title = models.CharField(max_length=50)
	views = models.IntegerField(default=0)
	datetaken = models.DateTimeField(blank=True, null=True)
	# dateuploaded = models.DateTimeField(blank=True)
	originalformat = models.CharField(max_length=10, null=True)
	iconserver = models.IntegerField(default=0, null=True)
	iconfarm = models.IntegerField(default=0, null=True)
	location = models.CharField(max_length=30, null=True)
	nsid = models.CharField(max_length=20, null=True)
	tags = models.CharField(max_length=100, null=True)
	url = models.CharField(max_length=100)
	user = models.CharField(max_length=30, null=True)
