from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *

def login_required(function):
	def wrap(request,*args,**kwargs):
		if 'id' in request.session:
			return function(request,*args,**kwargs)
		else:
			messages.info(request,'Login to continue')
			return redirect('user_login')
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def is_mentee(function):
	def wrap(request,*args,**kwargs):
		if request.session['role'] == 'mentee':
			return function(request,*args,**kwargs)
		else:
			messages.info(request,'Sorry! You are not logged in as mentee')
			return redirect('/user_login/')
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def is_mentor(function):
	def wrap(request,*args,**kwargs):
		if request.session['role'] == 'mentor':
			return function(request,*args,**kwargs)
		else:
			messages.info(request,'Sorry! You are not logged in as mentor')
			return redirect('/user_login/')
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def is_verified_user(function):
	def wrap(request,*args,**kwargs):
		my_form = login_form(request.POST)
		if my_form.is_valid():
			role = my_form.cleaned_data['role']
			username = my_form.cleaned_data['username']
			if role == "mentee":
				if mentee_model.objects.filter((Q(username=username)|Q(email=username)),verified=False).exists():
					obj = mentee_model.objects.get((Q(username=username)|Q(email=username)),verified=False)
					return redirect('email_verify',role='mentee',username=obj.username)
			elif role == "mentor":
				if mentor_model.objects.filter((Q(username=username)|Q(email=username)),verified=False).exists():
					obj = mentor_model.objects.get((Q(username=username)|Q(email=username)),verified=False)
					return redirect('email_verify',role='mentor',username=obj.username)
			elif role == "others":
				pass
		return function(request,*args,**kwargs)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap