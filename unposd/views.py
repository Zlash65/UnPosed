# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

max_per_page = 6

def home(request):
	''' / routes to displaying all the photos list '''
	return redirect('/unposd/photos')

def login(request, alert=None):
	''' displaying login page with or without authentication alert '''

	if request.method == 'POST' and not alert:
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			from django.contrib.auth import login
			login(request, form.get_user())
			return redirect('/unposd/photos')
		else:
			args = {"form": form}
			return render(request, 'login/login.html', args)
	else:
		form = AuthenticationForm(request)

		args = {"form": form, "alert": alert}
		return render(request, 'login/login.html', args)

def logout_view(request):
	''' destroy csrf token and route to login page '''
	logout(request)
	return redirect('/unposd/login')

def register(request):
	''' create a new user '''
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return login(request, alert="Login using the registered credentials.")
		else:
			args = {"form": form, "alert": "Wrong data inserted. Please try again!"}
			return render(request, 'login/reg_form.html', args)
	else:
		form = UserCreationForm()

		args = {"form": form}
		return render(request, 'login/reg_form.html', args)

def groups(request):
	''' displays list of groups that the logged in user is associated with '''

	from unposd.models import Groups
	page = int(request.GET.get('page', '1'))
	groups = list(Groups.objects.extra(where=["members like '%%%{0}%%%'"
		.format(request.user.username)]))

	# args = {"data": groups}
	args = get_paging_index(groups, page)

	return render(request, 'main/groups_list.html', args)

def photos_list(request, group_id):
	''' displays list of photos in the selected that are associated with the logged in user '''

	from unposd.models import Photos
	page = int(request.GET.get('page', '1'))
	photos = list(Photos.objects.filter(user=request.user.username).filter(group_id=group_id))

	# tags_view = {}
	# for d in photos:
	# 	tags_view[d.photo_id] = len(d.tags.split(' | '))

	# args.update({"tags_view": tags_view})
	args = get_paging_index(photos, page)

	return render(request, 'main/photos_list.html', args)

def photos_display(request, photo_id):
	''' displays data of the selected photo with details such as tags, views, etc '''
	from unposd.models import Photos
	photo = Photos.objects.filter(user=request.user.username).filter(photo_id=photo_id)[0]
	photo.views += 1
	photo.save()

	args = {"photo": photo}
	return render(request, 'main/photos_display.html', args)

def photos(request):
	''' displays all the photos associated with the logged in user '''

	from unposd.models import Photos

	# def get_tags(photos):
	# 	tags_view = {}
	# 	for d in photos:
	# 		tags_view[d.photo_id] = len(d.tags.split(' | '))
		
	group_id = request.GET.get('group','')
	page = int(request.GET.get('page', '1'))

	if group_id:
		photos = list(Photos.objects.filter(user=request.user.username).filter(group_id=group_id))

		# args["tags_view"] = get_tags(photos)
		args = get_paging_index(photos, page)

		return render(request, 'main/photos_list.html', args)
	else:
		photos = list(Photos.objects.filter(user=request.user.username))

		# args["tags_view"] = get_tags(photos)
		args = get_paging_index(photos, page)

		return render(request, 'main/photos_list.html', args)

def get_paging_index(data, page):
	''' create a paging like view '''
	start_index, end_index = ((page-1)*max_per_page), (page*max_per_page)

	args = {"last": False}
	if end_index < len(data):
		args["data"] = data[start_index:end_index]
	else:
		args["data"], args["last"] = data[start_index:end_index], True

	args["page"] = page

	return args
