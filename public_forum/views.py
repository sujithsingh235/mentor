from django.shortcuts import render, redirect
from .models import questions, answers, comments, like,favourite
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
    answer = answers.objects.filter(question_id=id).order_by('-like')
    list_of_answers = []
    current_user = request.session.get('username', 'null')
    if len(answer) != 0:
        exist = True
        for ans in answer:		# This will count the number of comments and likes
            comments_count = comments.objects.filter(answer_id=ans.id).count()
            # This will return a list of dictionaries. So we have to convert it as a list of likes_users.
            dict_liked_users = list(like.objects.filter(
                answer_id=ans.id).values('user'))
            liked_users = []
            for user in dict_liked_users:
                liked_users.append(user['user'])
            likes_count = like.objects.filter(answer_id=ans.id).count()
            new_tuple = (ans, comments_count, likes_count, liked_users)
            list_of_answers.append(new_tuple)
    else:
        exist = False
    context = {
        'question': question,
        'answers': list_of_answers,
        'exist': exist,
        'current_user': current_user,
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
                         user=user, posted_time=posted_time, like=0)
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
    current_user = request.session.get('username', 'null')
    if current_user == 'null':
        return redirect('user_login')
    user = request.POST.get('user')
    answer_id = request.POST.get('answer_id')
    question_id = request.POST.get('question_id')
    status = request.POST.get('status')
    if status == 'like':
        new_like = like(user=user, answer_id=answer_id)
        new_like.save()
        ans_obj = answers.objects.get(id=answer_id)
        like_count = ans_obj.like + 1
        print(like_count)
        ans_obj.like = like_count
        ans_obj.save()
    elif status == "rlike":   # rlike means removing the like
        l = like.objects.get(user=user, answer_id=answer_id)
        l.delete()
        ans_obj = answers.objects.get(id=answer_id)
        like_count = ans_obj.like - 1
        print(like_count)
        ans_obj.like = like_count
        ans_obj.save()
    return redirect('/public/forum/'+str(question_id))


def my_questions_view(request):
    user = request.session.get('username', 'null')
    if user == 'null':
        return redirect('user_login')
    else:
        ques = questions.objects.filter(user=user)
        if len(ques) != 0:
            exist = True
        else:
            exist = False  # No questions to be displayed
        context = {
            'questions': ques,
            'exist': exist
        }
        return render(request, 'public_forum/my_questions.html', context)


def my_answers_view(request):
    user = request.session.get('username', 'null')
    if user == 'null':
        return redirect('user_login')
    else:
        ans = answers.objects.filter(user=user)
        lst = []
        for i in ans:
            lst.append(i.question_id)
        ques = questions.objects.filter(id__in=lst)
        lst.clear()
        print(ans)
        print(ques)
        for an in ans:  # This for loop will group the question with answer.
           for que in ques:
               if an.question_id == que.id:
                   new_tup = (que.id,que.question,an.answer)
                   lst.append(new_tup)
        print(lst)
        context = {
            'list' : lst
          }
        return render(request,'public_forum/my_answers.html',context)

def fav_view(request):
    question_id = request.GET.get('question_id',0)
    user = request.session.get('username','null')
    fav = favourite(user=user,question_id=question_id)
    fav.save()
    return HttpResponse('success')
