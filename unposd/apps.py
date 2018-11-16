# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
import flickrapi, os, urllib
from random import randint
import sys

api_key = 'f2dde0fc40550083e8c8ccd08d1d0a6e'
api_secret = 'f680d9cb8a600510'

# instantiating flickrapi with api key and secret and response form for data
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

class UnposdConfig(AppConfig):
	name = 'unposd'
	verbose_name = "UnPosed"
	ready_has_run = False

	def ready(self):
		if self.ready_has_run:
			return

		if db_table_exists("unposd_groups") and db_table_exists("unposd_photos"):
			from unposd.models import Groups
			if not len(Groups.objects.all()):
				print("Setting up database with dummy data...")
				print("Please wait for a couple of minute...")
				create_dummy_users()
				initial_setup()

		self.ready_has_run = True

def db_table_exists(table_name):
	from django.db import connection
	return table_name in connection.introspection.table_names()

def initial_setup():
	users = [['jane'], ['john'], ['jane', 'john']]
	# group_id shortlisted to create a dummy environment
	groups = ["4522828@N24", "2740203@N20", "1986740@N21",
		"56407608@N00", "535624@N24", "3007017@N22"]

	# create an images directory where images will be stored
	if not os.path.exists("unposd/static/images"):
		os.makedirs("unposd/static/images")

	for group in groups:
		# make a directory for each group
		if not os.path.exists("unposd/static/images/" + group):
			os.makedirs("unposd/static/images/"+group)

		# fetch 30 photos from each group and store it locally and make its entry in database
		random = randint(20,30)
		photos = flickr.photos.search(group_id=group, per_page=random).get("photos")
		no_of_photos = 0

		for photo in photos.get("photo"):
			sys.stdout.write('Setting up photos and members for group %s [%s%s]\r' \
				% (group, "="*(no_of_photos+1), " "*(len(photos.get("photo"))-(no_of_photos+1))))
			sys.stdout.flush()

			image = "https://farm{0}.staticflickr.com/{1}/{2}_{3}_n.jpg".format(photo.get("farm"),
				photo.get("server"), photo.get("id"), photo.get("secret"))
			target = "unposd/static/images/{0}/{1}.jpg".format(group, photo.get("id"))

			ph = get_photo_info(photo.get("id"))
			ph.update({
				"url": target,
				"group_id": group,
				"user": users[0:2][randint(0,1)][0]
			})

			if insert_photo(ph):
				no_of_photos += 1
				urllib.urlretrieve(image, target)

		insert_group(group, no_of_photos, users[randint(0,2)])
		print()

def insert_group(group, total_photos, members):
	''' insert group data in db '''
	from unposd.models import Groups
	group = get_group_info(group)
	groups = Groups()
	groups.group_id = group.get("group_id")
	groups.name = group.get("name")
	groups.iconserver = group.get("iconserver")
	groups.privacy = group.get("privacy")
	groups.iconfarm = group.get("iconfarm")
	groups.members = '|'.join(members)
	groups.members_count = len(members)
	groups.total_photos = total_photos

	try:
		groups.save()
	except Exception, e:
		# print(e)
		pass

def insert_photo(photo):
	''' insert photo data in db '''
	from unposd.models import Photos
	photos = Photos()
	photos.photo_id = photo.get("photo_id")
	photos.title = photo.get("title")
	photos.group_id = photo.get("group_id")
	# photos.datetaken = photo.get("datetaken")
	photos.originalformat = photo.get("originalformat")
	photos.iconserver = photo.get("iconserver")
	photos.iconfarm = photo.get("iconfarm")
	photos.location = photo.get("location")
	photos.nsid = photo.get("nsid")
	photos.url = photo.get("url")
	photos.user = photo.get("user")
	photos.tags = ' | '.join(list(photo.get("tags")[0:5]))

	try:
		photos.save()
		return True
	except Exception, e:
		# print(e)
		return False

def search_group_by_text(txt, per_page=5):
	''' fetches list of groups based on the text provided'''
	if not txt: raise "No text provided to search for groups"

	groups = flickr.groups.search(text=txt, per_page=per_page).get("groups").get("group")

	return groups

def get_group_info(group_id):
	''' fetches detail of a group '''
	if not group_id: return False

	group = flickr.groups.getInfo(group_id=group_id).get("group")

	return {
		"name": group.get("name").get("_content"),
		"group_id": group.get("nsid"),
		# "description": group.get("description").get("_content"),
		# "topic_count":  group.get("topic_count").get("_content"),
		"iconserver":  group.get("iconserver"),
		"privacy":  group.get("privacy").get("_content"),
		# "members":  group.get("members").get("_content"),
		# "total_photos":  group.get("pool_count").get("_content"),
		"iconfarm":  group.get("iconfarm")
	}

def get_photo_info(photo_id):
	''' fetches detail of a photo '''
	if not photo_id: return False

	photo = flickr.photos.getInfo(photo_id=photo_id).get("photo")

	tags = []
	for tag in photo.get("tags").get("tag"):
		tags.append(tag.get("_content"))

	return {
		"photo_id": photo.get("id"),
		"title": photo.get("title").get("_content"),
		# "description": photo.get("description").get("_content"),
		# "views": photo.get("views"),
		# "dateuploaded": photo.get("dateuploaded"),
		"datetaken": photo.get("dates").get("taken"),
		"originalformat":  photo.get("originalformat"),
		"iconserver":  photo.get("owner").get("iconserver"),
		"location":  photo.get("owner").get("location"),
		"iconfarm":  photo.get("owner").get("iconfarm"),
		"nsid": photo.get("owner").get("nsid"),
		"tags": tags
	}

def create_dummy_users():
	from django.contrib.auth.models import User
	users = [
		{"uname": "allen", "pwd": "asdf1234", "is_superuser": True, "is_staff": True},
		{"uname": "john", "pwd": "johndoe1", "is_superuser": False, "is_staff": False},
		{"uname": "jane", "pwd": "janedoe1", "is_superuser": False, "is_staff": False}
	]

	for d in users:
		try:
			User.objects.create_user(username=d.get("uname"), password=d.get("pwd"),
				is_superuser=d.get("is_superuser"), is_staff=d.get("is_staff"))
		except Exception, e:
			pass
	# User.objects.create_user(username='allen', password='asdf1234', is_superuser=True, is_staff=True)
	# User.objects.create_user(username='john', password='johndoe1')
	# User.objects.create_user(username='jane', password='janedoe1')
