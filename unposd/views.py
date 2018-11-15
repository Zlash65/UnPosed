# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
	# return render(request, 'base.html')
	return redirect('/unposd/photos')

def logout_view(request):
	logout(request)
	return redirect('/unposd/login')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/unposd')
	else:
		form = UserCreationForm()

		args = {"form": form}
		return render(request, 'login/reg_form.html', args)

def groups(request):
	from unposd.models import Groups
	groups = list(Groups.objects.extra(where=["members like '%%%{0}%%%'"
		.format(request.user.username)]))

	args = {"data": groups}
	return render(request, 'main/groups_list.html', args)

def photos_list(request, group_id):
	from unposd.models import Photos
	photos = list(Photos.objects.filter(user=request.user.username).filter(group_id=group_id))

	# tags_view = {}
	# for d in photos:
	# 	tags_view[d.photo_id] = len(d.tags.split(' | '))

	args = {
		"data": photos,
		# "tags_view": tags_view
	}
	return render(request, 'main/photos_list.html', args)

def photos_display(request, photo_id):
	from unposd.models import Photos
	photo = Photos.objects.filter(user=request.user.username).filter(photo_id=photo_id)[0]

	args = {"photo": photo}
	return render(request, 'main/photos_display.html', args)

def photos(request):
	from unposd.models import Photos
	group_id = request.GET.get('group','')

	if group_id:
		photos = list(Photos.objects.filter(user=request.user.username).filter(group_id=group_id))

		# tags_view = {}
		# for d in photos:
		# 	tags_view[d.photo_id] = len(d.tags.split(' | '))

		args = {
			"data": photos,
			# "tags_view": tags_view
		}
		return render(request, 'main/photos_list.html', args)
	else:
		photos = list(Photos.objects.filter(user=request.user.username))

		# tags_view = {}
		# for d in photos:
		# 	tags_view[d.photo_id] = len(d.tags.split(' | '))

		args = {
			"data": photos,
			# "tags_view": tags_view
		}
		return render(request, 'main/photos_list.html', args)

