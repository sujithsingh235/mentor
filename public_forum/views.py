from django.shortcuts import render, redirect
from .models import questions, answers, comments, like
import datetime
from django.http import HttpResponse
from .forms import answers_form

# from .forms import new_question_form

# Create your views here.


def public_forum_view(request):
    ques = questions.objects.all().order_by('-posted_time')
    if len(ques) != 0:
        exist = True
    else:
        exist = False  # No questions to be displayed
    context = {
        'questions': ques,
        'exist': exist
    }
    return render(request, 'public_forum/public_forum.html', context)


def new_question_view(request):
    if request.method == "GET":
        user = request.session.get('username', 'null')
        if user == 'null':
            return redirect('user_login')
        return render(request, 'public_forum/create_new_question.html')
    question = questions()
    question.question = request.POST.get('question')
    question.description = request.POST.get('desc')
    question.user = request.session.get('username', 'null')
    question.posted_time = datetime.datetime.now()
    question.save()
    return redirect('/public/forum/')


def question_brief_view(request, id):
    question = questions.objects.get(id=id)
    answer = answers.objects.filter(question_id=id).order_by('-posted_time')
    list_of_answers = []
    current_user = request.session.get('username', 'null')
    if len(answer) != 0:
        exist = True
        for ans in answer:		# This will count the number of comments
            count = comments.objects.filter(answer_id=ans.id).count()
            new_tuple = (ans, count)
            list_of_answers.append(new_tuple)
    else:
        exist = False
    context = {
        'question': question,
        'answers': list_of_answers,
        'exist': exist,
        'current_user': current_user
    }
    return render(request, 'public_forum/question_brief.html', context)


def write_answer_view(request, id):
    if request.method == 'GET':
        if request.session.get('username', 'null') == 'null':
            return redirect('user_login')
        question = questions.objects.get(id=id)
        context = {
            'question': question,
            'placeholder': "Enter your answer..."
        }
        return render(request, "public_forum/write_answer.html", context)
    else:
        question_id = id
        user = request.session.get('username', 'null')
        posted_time = datetime.datetime.now()
        ans = request.POST.get('ans')
        answer = answers(question_id=id, answer=ans,
                         user=user, posted_time=posted_time)
        answer.save()
        return redirect("/public/forum/" + str(id))


def comments_view(request, id):
    if request.method == 'POST':
        user = request.session.get('username', 'null')
        posted_time = datetime.datetime.now()
        comment = request.POST.get('comment')
        answer_id = id
        new_comment = comments(
            user=user, posted_time=posted_time, comment=comment, answer_id=id)
        new_comment.save()
    elif request.method == 'POST':
        comment = comments.objects.filter(
            answer_id=id).order_by('-posted_time')
        if len(comment) != 0:
            exist = True
        else:
            exist = False
        context = {
            'comments': comment,
            'exist': exist
        }
        return render(request, "public_forum/comments.html", context)


def edit_answer_view(request, id, question_id):
    if request.method == "GET":
        current_user = request.session.get('username', 'null')
        ans = answers.objects.get(id=id)
        if current_user == 'null':
            return redirect('user_login')
        elif current_user != ans.user:
            return redirect('/')
        text = ans.answer
        context = {
            'text': text
        }
        return render(request, "public_forum/write_answer.html", context)
    elif request.method == 'POST':
        ans = answers.objects.get(id=id)
        ans.answer = request.POST.get('ans')
        ans.posted_time = datetime.datetime.now()
        ans.save()
        return redirect('/public/forum/'+str(question_id))


def delete_answer_view(request):
    answer_id = request.GET.get('answer_id')
    question_id = request.GET.get('question_id')
    answer = answers.objects.get(id=answer_id)
    comment = comments.objects.filter(answer_id=answer_id)
    user = answer.user
    current_user = request.session.get('username', 'null')
    if current_user == 'null':
        return redirect('user_login')
    elif current_user != user:
        return redirect('/')
    else:
        answer.delete()
        comment.delete()
        return redirect('/public/forum/'+str(question_id))


def like_view(request):
    user = request.POST.get('user')
    answer_id = request.POST.get('answer_id')
    question_id = request.POST.get('question_id')
    print(question_id)
    new_like = like(user=user, answer_id=answer_id, like_status="liked")
    new_like.save()
    return redirect('/public/forum/'+str(question_id))
