from django.shortcuts import render

from .forms import question_form

# Create your views here.

def public_forum_view(request):
	my_form = question_form(request.POST or None)
	if my_form.is_valid():
		print(my_form.cleaned_data)
	context = {
		'form' : my_form
	}
	return render(request,'public_forum/public_forum.html',context)