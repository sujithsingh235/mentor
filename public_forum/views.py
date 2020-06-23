from django.shortcuts import render
from .models import question

from .forms import question_form

# Create your views here.

def public_forum_view(request):
	questions = question.objects.all()
	context = {
		'questions' : questions
	}
	return render(request,'public_forum/public_forum.html',context)

def new_question_view(request):
	return render(request,'public_forum/create_new_question.html')