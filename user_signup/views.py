import random
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404

from .models import *
from .decorators import *
from .forms import *
# Create your views here.

def sub_field_view(request):
	if request.method == "GET":
		field_id = request.GET.get('field')
		subfield = sub_field.objects.filter(field_id=field_id).order_by('sub_field_name')
		context = {
			'sub_field' : subfield
		}
		return render(request,'user_signup/sub_field.html',context)

#Mentee signup form
def mentee_signup_view(request):
	my_form = mentee_signup_form(request.POST or None)
	if my_form.is_valid():
		form_obj = my_form.cleaned_data
		form_obj.pop('confirm_password')
		form_obj['otp'] = random.randrange(100000,999999)
		print(form_obj)
		obj,created = mentee_model.objects.update_or_create(email=form_obj['email'],defaults=form_obj)
		print("obj :",obj,"created :",created)
		return redirect('email_verify',role='mentee',username=form_obj['username'])
	context = {
		'form' : my_form
	}
	return render(request,'user_signup/signup.html',context)

# here comes a decorator which redirects a non verified user with an verified email id of another user
#email verify view
def email_verify(request,role,username):
	initial = {'username':username,'role':role}
	if request.method == "POST":
		ev_form = email_verify_form(request.POST)
		if ev_form.is_valid():
			username = ev_form.cleaned_data['username']
			role = ev_form.cleaned_data['role']
			otp = ev_form.cleaned_data['otp']
			if role == 'mentee':
				obj = get_object_or_404(mentee_model,username=username)
			elif role == 'mentor':
				obj = get_object_or_404(mentor_model,username=username)
			elif role == 'other':
				pass
			if otp == obj.otp:
				obj.verified = True
				obj.save()
				return redirect('user_login')
			else:
				messages.error(request,"invalid otp")
	ev_form = email_verify_form(initial=initial)
	context = {
		'form': ev_form,
	}
	return render(request,'user_signup/verify_otp.html',context)


#Login view
@is_verified_user
def user_login(request):
	if 'id' in request.session:
		if request.session['role'] == 'mentee':
			return redirect('/mentee_home/')
		elif request.session['role'] == 'mentor':
			return redirect('/mentor_home/')
	else:
		my_form = login_form(request.POST or None)
		if my_form.is_valid():
			form_obj = my_form.cleaned_data
			print(form_obj)
			username = form_obj['username']
			# Login As Mentee:
			if form_obj['role'] == 'mentee':
				obj = get_object_or_404(mentee_model,(Q(username=username)|Q(email=username)),verified=True)
			# Login as Mentor :
			elif form_obj['role'] == 'mentor':
				obj = get_object_or_404(mentor_model,(Q(username=username)|Q(email=username)),verified=True)
			# Login as Others :
			elif form_obj['role'] == 'others':
				pass
			if form_obj['password'] == obj.password:
				#session variable
				request.session['id'] = obj.id
				request.session['email'] = obj.email
				request.session['username'] = obj.username
				request.session['role'] = form_obj['role']
				return redirect('user_login')
			else:
				messages.error(request,'Invalid Password')
		context = {
			'form': my_form,
		}
		return render(request,'user_signup/login.html',context)


# mentor signup view NEED TO BE CHANGED :
def mentor_signup_view(request):
	my_form=mentor_signup(request.POST or None)
	if my_form.is_valid():
		form_obj = my_form.cleaned_data
		form_obj.pop('confirm_password')
		form_obj['otp']=random.randrange(100000,999999)
		print(my_form.cleaned_data)
		if mentor_model.objects.filter(mobile=form_obj['mobile']).exists():
			mentor_model.objects.filter(mobile=form_obj['mobile']).update(**form_obj)
			print('existing mentor updated - not yet verified')
		else:
			p = mentor_model.objects.create(**form_obj)
			print('new mentor created - not yet verified')
		verify_form = otp_verify_form({'mobile':form_obj['mobile'],'role':'mentor'})
		context= {
			'form' : verify_form
		}
		return render(request,'user_signup/verify_otp.html',context)
	context = {
		'form' : my_form
	}
	return render(request,'user_signup/mentor_signup.html',context)

#Mentee signup form
def mentor_signup_view(request):
	my_form = mentor_signup_form(request.POST or None)
	if my_form.is_valid():
		form_obj = my_form.cleaned_data
		form_obj.pop('confirm_password')
		form_obj['otp'] = random.randrange(100000,999999)
		print(form_obj)
		obj,created = mentor_model.objects.update_or_create(email=form_obj['email'],defaults=form_obj)
		print("obj :",obj,"created :",created)
		return redirect('email_verify',role='mentor',username=form_obj['username'])
	context = {
		'form' : my_form
	}
	return render(request,'user_signup/signup.html',context)

@login_required
def logout(request):
	del request.session['id']
	del request.session['email']
	del request.session['username']
	del request.session['role']
	return redirect('/')

# def temp_signup_view(request):
# 	my_form = temp_user_form()
# 	if request.method == "POST":
# 		my_form = temp_user_form(request.POST)
# 		if my_form.is_valid():
# 			print(my_form.cleaned_data)
# 			user = my_form.save(commit=False)
# 			user.otp = random.randrange(100000,999999)
# 			try:
# 				obj=mentee_model.objects.get(mobile=user.mobile)
# 				obj.password=user.password
# 				obj.otp=user.otp
# 				obj.save()
# 				form = otp_verify_form(instance=obj)
# 				context = {
# 				'form' : form,
# 				'mobile' : obj.mobile
# 				}
# 			except Exception as e:
# 				print(e)
# 				user.save()
# 				form = otp_verify_form()
# 				context = {
# 				 'form' : form,
# 				 'mobile' : user.mobile
# 				}
# 			return render(request,'verify_otp.html',context)
# 		else:
# 			print(my_form.errors)
# 	context = {
# 	"form": my_form
# 	}
# 	return render(request,'signup.html',context)

@is_mentee
def temp_view(request):
	messages.error(request,'sorry')
	messages.success(request,'successfull')
	return render(request,'base.html')

def temp_view2(request):
	return HttpResponse('hello')