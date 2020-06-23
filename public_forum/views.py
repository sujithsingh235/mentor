from django.shortcuts import render,redirect
from .models import questions
import datetime
from django.http import HttpResponse

#from .forms import new_question_form

# Create your views here.

def public_forum_view(request):
	ques = questions.objects.all().order_by('-posted_time')
	context = {
		'questions' : ques
	}
	return render(request,'public_forum/public_forum.html',context)

def new_question_view(request):
	if request.method == "GET":
		return render(request,'public_forum/create_new_question.html')
	question = questions()
	question.question = request.POST.get('question')
	print(question.question)
	question.description = request.POST.get('desc')
	question.user = request.user
	question.posted_time = datetime.datetime.now()
	question.save()
	return redirect('/public/forum/')

def question_brief_view(request,id):
	question = questions.objects.get(id=id)
	context = {
		'question' : question
	}
	return render(request,'public_forum/question_brief.html',context)