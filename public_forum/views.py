from django.shortcuts import render, redirect
from .models import *
import datetime
from django.http import HttpResponse,Http404,JsonResponse
from .forms import answers_form
import json

from user_signup.decorators import *

# from .forms import new_question_form

# Create your views here.

tags = []

def public_forum_view(request,page):
    start = (page-1) * 10
    stop = (page * 10) - 1
    no_of_questions = questions.objects.all().count()
    no_of_pages = int(no_of_questions/11) + 1
    if page > no_of_pages:
        raise Http404("This page is not found in the database")
    try:
        if no_of_pages == page:
            ques = questions.objects.all().order_by('-posted_time')[start:]
        else:
            ques = questions.objects.all().order_by('-posted_time')[start:stop]
    except:
        raise Http404("The page is not found in the database")
    questions_with_tags = []
    if len(ques) != 0:
        exist = True
        for que in ques:
            associated_tags = tag_with_question_id.objects.filter(question_id=que.id).values_list("tag",flat=True)
            print(que.id,associated_tags)
            new_tup = (que,associated_tags)
            questions_with_tags.append(new_tup)
    else:
        exist = False  # No questions to be displayed
    context = {
        'questions_with_tags': questions_with_tags,
        'exist': exist,
        'no_of_pages' : no_of_pages,
        'current_page' : page
    }
    return render(request, 'public_forum/public_forum.html', context)


def new_question_view(request):
    if request.method == "GET":
        user = request.session.get('username', 'null')
        if user == 'null':
            return redirect('user_login')
        global tags 
        tags = list(tag.objects.all().values_list('tag_name',flat=True))
        print(tags)     
        return render(request, 'public_forum/create_new_question.html')     
    question = questions()
    data = json.loads(request.body)
    user = request.session.get('username','null')
    if user == 'null':
        res = {
            "msg" : "login",
            "url" : "user_login"
        }
        return JsonResponse(res)
    question.user = user
    question.posted_time = datetime.datetime.now()
    question.question = data.get('title')
    question.description = data.get('desc')
    question.report = 0
    question.save()
    added_tags = data.get('tags')
    for this_tag in added_tags:
        new_ques_tag = tag_with_question_id(question_id=question.id,tag=this_tag)
        new_ques_tag.save()
        if this_tag not in tags:
            new_tag = tag(tag_name=this_tag)
            new_tag.save()
    tags.clear()
    res = {
        "msg" : "success",
        "url" : "/public/forum/page-1"
    }
    return JsonResponse(res)


def question_brief_view(request, id):
    try:
        question = questions.objects.get(id=id)
    except:
        raise Http404("This question is not found in the database")
    answer = answers.objects.filter(question_id=id).order_by('-like')
    list_of_answers = []
    current_user = request.session.get('username', 'null')
    added_to_fav = favourite.objects.filter(user=current_user,question_id=id).exists() # checks whether the user already added this question to fav or not
    reported_questions = report.objects.filter(user=current_user,QorA="question").values_list("QorA_id",flat=True)
    reported_answers = report.objects.filter(user=current_user,QorA="answer").values_list("QorA_id",flat=True)
    associated_tags = tag_with_question_id.objects.filter(question_id=id).values_list("tag",flat=True)
    print(associated_tags)
    no_of_answers = len(answer)
    if no_of_answers != 0:    
        for ans in answer:		# This will count the number of comments and likes
            comments_count = comments.objects.filter(answer_id=ans.id).count()
            # This will return a list of dictionaries. So we have to convert it as a list of likes_users.
            dict_liked_users = list(like.objects.filter(answer_id=ans.id).values('user'))
            liked_users = []
            for user in dict_liked_users:
                liked_users.append(user['user'])
            likes_count = like.objects.filter(answer_id=ans.id).count()
            new_tuple = (ans, comments_count, likes_count, liked_users)
            list_of_answers.append(new_tuple)
    context = {
        'question': question,
        'tags' : associated_tags,
        'answers': list_of_answers,
        'no_of_answers': no_of_answers,
        'current_user': current_user,
        'fav' : added_to_fav,
        'reported_questions' : reported_questions,
        'reported_answers' : reported_answers
    }
    return render(request, 'public_forum/question_brief.html', context)


@login_required
def write_answer_view(request, id):
    if request.method == 'GET':
        try:
            question = questions.objects.get(id=id)
        except:
            raise Http404("The question is not found in the database")
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
        answer = answers(question_id=id, answer=ans,user=user, posted_time=posted_time, like=0,report=0)
        answer.save()
        return redirect("/public/forum/" + str(id))


@login_required
def comments_view(request, id):
    if request.method == 'POST':
        user = request.session.get('username', 'null')
        if user == 'null':
            return redirect('user_login')
        posted_time = datetime.datetime.now()
        comment = request.POST.get('comment')
        answer_id = id
        new_comment = comments(user=user, posted_time=posted_time, comment=comment, answer_id=id)
        new_comment.save()
    
    comment = comments.objects.filter(answer_id=id).order_by('-posted_time')
    if len(comment) != 0:
        exist = True
    else:
        exist = False
    context = {
        'comments': comment,
        'exist': exist
    }
    return render(request, "public_forum/comments.html", context)


@login_required
def edit_answer_view(request, id, question_id):
    if request.method == "GET":
        current_user = request.session.get('username', 'null')
        try:
            ans = answers.objects.get(id=id)
        except:
            raise Http404("The answer is not found in the database")
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
        try:
            ans = answers.objects.get(id=id)
        except:
            raise Http404("The answer is not found in the database")
        ans.answer = request.POST.get('ans')
        ans.posted_time = datetime.datetime.now()
        ans.save()
        return redirect('/public/forum/'+str(question_id))


def delete_answer_view(request):
    answer_id = request.GET.get('answer_id')
    question_id = request.GET.get('question_id')
    try:
        answer = answers.objects.get(id=answer_id)
    except:
        raise Http404("The answer is not found in the database")
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


def add_like_view(request):
    user = request.session.get('username','null')
    if user == 'null':
        return redirect('user_login')
    answer_id = request.POST.get('answer_id')
    new_like = like(user=user, answer_id=answer_id)
    new_like.save()
    try:
        ans_obj = answers.objects.get(id=answer_id)
    except:
        raise Http404("The answer is not found in the database")
    like_count = ans_obj.like + 1
    print(like_count)
    ans_obj.like = like_count
    ans_obj.save()
    return HttpResponse('success')


def remove_like_view(request):
    user = request.session.get('username','null')
    if user == 'null':
        return redirect('user_login')
    answer_id = request.POST.get('answer_id')
    try:
        l = like.objects.get(user=user,answer_id=answer_id)
    except:
        raise Http404("The like object is not found in the database")
    l.delete()
    try:
        ans_obj = answers.objects.get(id=answer_id)
    except:
        raise Http404("The answer object is not found in the database")
    like_count = ans_obj.like - 1
    print(like_count)
    ans_obj.like = like_count
    ans_obj.save()
    return HttpResponse('success')

    


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
        for an in ans:  # This for loop will group the question with answer.
            for que in ques:
                if an.question_id == que.id:
                    new_tup = (que.id, que.question, an.answer)
                    lst.append(new_tup)
        context = {
            'list': lst
        }
        return render(request, 'public_forum/my_answers.html', context)


def fav_view(request):
    user = request.session.get('username', 'null')
    if user == 'null':
        return redirect('user_login')
    else:
        question_id = request.POST.get('question_id')
        fav = favourite(user=user, question_id=question_id)
        fav.save()
        return HttpResponse('success')


def fav_remove_view(request):
    user = request.session.get('username','null')
    if user == 'null':
        return redirect('user_login')
    else:
        question_id = request.POST.get('question_id')
        try:
            fav = favourite.objects.get(user=user, question_id=question_id)
        except:
            raise Http404("The favourite object is not found in the database")
        fav.delete()
        return HttpResponse('success')

@login_required
def my_favourite_view(request):
    user = request.session.get('username','null')
    question_ids = favourite.objects.filter(user=user).values('question_id')
    print(question_ids)
    ques = questions.objects.filter(id__in = question_ids).order_by('-id')
    if len(question_ids)<=0:
        exist = False
    else:
        exist = True
    context = {
        "questions" : ques,
        "exist" : exist
    }
    return render(request,"public_forum/my_fav.html",context)


def report_view(request):
    user = request.session.get('username','null')
    if user == 'null':
        return redirect('user_login')
    id = request.POST.get('id')
    operation = request.POST.get('operation')
    QorA = request.POST.get('QorA')
    if QorA == 'question':
        try:
            obj = questions.objects.get(id=id)
        except:
            raise Http404("The question object is not found in the database")
    else:
        try:
            obj = answers.objects.get(id=id)
        except:
            raise Http404("The answer object is not found in the database")
    if operation == 'add_report':
        if report.objects.filter(user=user,QorA=QorA,QorA_id=id).exists():
            return HttpResponse("report already exist")
        new_report = report(user=user,QorA=QorA,QorA_id=id)
        new_report.save()
        count = obj.report + 1
        if count>=50:
            obj.delete()
            return redirect('/public/forum/')
        obj.report = count
        obj.save()
        return HttpResponse('success')
    elif operation == 'remove_report':
        if not report.objects.filter(user=user,QorA=QorA,QorA_id=id).exists():
            return HttpResponse("report not found")
        try:
            del_report = report.objects.get(user=user,QorA=QorA,QorA_id=id)
        except:
            raise Http404("The report object is not found in the database")
        del_report.delete()
        count = obj.report
        obj.report = count - 1
        obj.save()
        return HttpResponse('success')



def get_tags_view(request):
    value = request.GET.get('value','null')
    print(value)
    global tags
    res = []
    if value != "":
        i = 0
        for tag in tags:
            if tag.startswith(value):
                res.append(tag)
                i += 1
            if i>5:
                break
        res.sort()
    print(res)
    data = {
        "status" : 'ok',
        "tags" : res
    }
    return JsonResponse(data)


