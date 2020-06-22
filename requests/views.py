from django.shortcuts import render
from django.contrib import messages

from .forms import *

# Create your views here.

def send_request(request):
	req_form = requets_form(request.POST)
	if req_form.is_valid():
		print('hello')
		messages.success(request,'okk')
	return redirect('mentor_detail',mentor_id=req_form.cleaned_data['mentor_id'])