from django.shortcuts import render,redirect
from django.http import JsonResponse

from user_signup.decorators import *
from user_signup.models import *
from homepage.models import *
from requests.forms import *

# Homepage Views
# Create your views here.

def homepage_view(request):
	print(request.session.keys())
	return render(request,'homepage/homepage.html')

@is_mentee
def mentee_home(request):
	data = mentee_model.objects.get(username=request.session['username'])
	context = {
		'data' : data
	}
	return render(request,'homepage/mentee_home.html',context)

@is_mentor
def mentor_home(request):
	data = mentor_model.objects.get(username=request.session['username'])
	context = {
		'data' : data
	}
	return render(request,'homepage/mentor_home.html',context)


#dynamic filter based page render with jquery ajax(search_mentor.html) :
def search_mentor(request):
	if request.method == "GET":
		return render(request,'homepage/search_mentor.html')
	#response for jquery ajax :
	elif request.method == "POST":
		field = request.POST.get('field')
		if field:
			data = mentor_model.objects.filter(field__field_name=field).values('id','name','occupation','company_name','field','sub_field')
		else:
			data = mentor_model.objects.all().values('id','name','occupation','company_name','field__field_name','sub_field__sub_field_name')
		print(data)
		context = {
			'data': data,
		}
		return render(request,'homepage/mentor_card.html',context)

#single mentor detailed view :
def mentor_detail(request,mentor_id):
	if mentor_model.objects.filter(id=mentor_id).exists():
		initial = {'mentor_id':mentor_id}
		req_form = request_form(initial=initial)
		data = mentor_model.objects.values('id','name','occupation','company_name','field__field_name','sub_field__sub_field_name','pay_per_month').get(id=mentor_id)
		print(data)
		context = {
			'data': data,
			'form': req_form,
		}
		return render(request,'homepage/mentor_detail.html',context)

# viewing my requests
@login_required
def my_requests(request):
	if request.session['role'] == 'mentee':
		req_obj = req.objects.filter(mentee_id=request.session['id']).values()
		for index,x in enumerate(req_obj):
			mentor_obj = mentor_model.objects.values('id','name','occupation','company_name').get(id=x['mentor_id'])
			req_obj[index]['name'] = mentor_obj['name']
			req_obj[index]['occupation'] = mentor_obj['occupation']
			req_obj[index]['company_name'] = mentor_obj['company_name']
		print(req_obj)
		context = {
			'my_requests': req_obj,
		}
		return render(request,'homepage/mentee_requests_list.html',context)
	elif request.session['role'] == 'mentor':
		req_obj = req.objects.filter(mentor_id=request.session['id']).values()
		#getting the details of mentee with the mentee id from the mentee_model :
		for index,x in enumerate(req_obj):
			mentee_obj = mentee_model.objects.values().get(id=x['mentee_id'])
			req_obj[index]['name'] = mentee_obj['name']
		print(req_obj)
		context = {
			'my_requests': req_obj,
		}
		return render(request,'homepage/mentor_requests_list.html',context)

#request sent by mentee to mentor
@is_mentee
def send_req(request,mentor_id):
	mentee_id = request.session['id']
	# checking valid mentor id in url:
	if mentor_model.objects.filter(id=mentor_id).exists():
		#checking if a request is already made :
		if req.objects.filter(mentor_id=mentor_id,mentee_id=mentee_id).exists():
			p = req.objects.get(mentor_id=mentor_id,mentee_id=mentee_id)
			print(p.status)
			p.save()
			print('existing request have been updated')
		else:
			req_obj = {
				'mentor_id': mentor_id,
				'mentee_id': mentee_id,
			}
			p = req.objects.create(**req_obj)
			print('a new request have been sent')
		return redirect('/mentee_home/')
	else:
		print('such mentor Id does not exist')
		pass

# url : /accept_request/
@is_mentor
def accept_req(request):
	if request.method == "POST":
		mentor_id = request.session['id']
		mentee_id = request.POST.get('mentee_id')
		req_id = request.POST.get('req_id')
		if req.objects.filter(mentee_id=mentee_id,mentor_id=mentor_id,req_id=req_id).exists():
			print("Exists...")
			req_obj = req.objects.get(id=req_id)
			req_obj.status = "accepted"
			req_obj.save()
		else:
			print("mentee and mentor id dosent match with the req model..")
		return redirect('/my_requests/')
	else:
		# error 403
		pass