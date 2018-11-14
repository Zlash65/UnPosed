# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
	return render(request, 'base.html')

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
