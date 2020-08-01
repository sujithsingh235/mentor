from django.shortcuts import render,redirect,reverse
from datetime import datetime
from django.http import JsonResponse,HttpResponse
from .models import mentee_request_model,mentor_request_model
from user_signup.models import mentor_model,mentee_model
from public_forum.fun import time_convert
from user_signup.decorators import *

# Create your views here.
def request_view(request,mentor_id):
    
    mentee_id = request.session.get('id',None)
    role = request.session.get('role',None)
    if mentee_id is None:
        return redirect('user_login')
    elif role is None or role !='mentee':
        messages.warning(request,'mentor cannot goto this page')
        return redirect('/')
    if request.method == "POST":
        print('came here')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        hours_per_day = request.POST.get('hours_per_day')
        no_of_days = request.POST.get('no_of_days')
        from_time = request.POST.get('from')
        to_time = request.POST.get('to')
        note = request.POST.get('note')

        if int(hours_per_day) > 4:
            res = {
                "status" : "error",
                "message" : "Hours per day should be less than 4 hours."
            }
            return JsonResponse(res)
        hours = datetime.strptime(hours_per_day,"%H")
        from_hour = datetime.strptime(from_time,"%H:%M")
        to_hour = datetime.strptime(to_time,"%H:%M")

        str_hours = hours.strftime("%X")
        print(str_hours)
        if str_hours[0] == '0':
            str_hours = str_hours[1:]
        if str(to_hour - from_hour) != str_hours:
            res = {
                "status" : "error",
                "message": "Choose correct time"
            }
            return JsonResponse(res)
        else:
            mentor = mentor_model.objects.get(id=mentor_id)
            amount = (int(hours_per_day)*int(no_of_days)*mentor.pay_per_month)
            print(amount)
            new_request = mentee_request_model(
                mentor = mentor,
                mentee_id = mentee_id,
                title = title,
                description = desc,
                hours_per_day = hours_per_day,
                no_of_days = no_of_days,
                from_time = from_time,
                to_time = to_time,
                note = note,
                status = 'pending',
                request_posted_time = datetime.now(),
            )
            new_request.save()
            m = mentor_request_model(
                mentor_id = mentor_id,
                mentee_request = new_request,
                mentee = mentee_model.objects.get(id=mentee_id),
                status = 'new'
            )
            m.save()
            url = "mentee/"+str(mentee_id)+"/my_request"
            res = {
                "status" : "ok",
                "url": url
            }
            return JsonResponse(res)
    context = {
        'mentor_id' : mentor_id,
        'mentee_id' : mentee_id
    }
    return render(request,'request/request.html',context)



def my_request_view(request,mentee_id):
    role = request.session.get('role',None)
    if role is None or role.lower() == 'others' or role.lower() == 'mentor':
        messages.warning(request,"mentees only can access this page")
        return redirect('user_login')
    id = request.session.get('id')
    if mentee_id != id :
        return redirect('/')
    my_request = mentee_request_model.objects.filter(mentee_id=id).order_by('-request_posted_time')
    for req in my_request:
        req.request_posted_time = time_convert(req.request_posted_time)

    context={
        "requests" : my_request
    }
    return render(request,'request/my_request.html',context)


def request_cancel_view(request,mentee_id):
    role = request.session.get('role',None)
    id = request.session.get('id',None)
    print(role)
    print(id)
    if role is None or role!='mentee' or id!=mentee_id:
        return redirect('/')

    request_id = request.POST.get('request_id')
    req = mentee_request_model.objects.get(id=request_id)
    req.status = 'cancelled'
    req.save()

    req = mentor_request_model.objects.get(mentee_request__id=request_id)   
    req.delete()
    print(req)

    return redirect('my_request',mentee_id=mentee_id)


def request_brief_view(request,request_id):
    id = request.session.get('id')
    req = mentor_request_model.objects.get(mentee_request_id=request_id)
    print(req)
    # req.mentee_request.from_time = time_convert(req.mentee_request.from_time)
    # req.mentee_request.from_time = time_convert(req.mentee_request.to_time)
    context = {
        'request' : req
    }
    return render(request,'request/mentee-details.html',context)  # request_brief


@login_required
def mentor_requests_view(request):
    id = request.session.get('id',None)
    role = request.session.get('role',None)
    print(id)
    print(role)
    if id is None or role != "mentor":
        return redirect('/')
    mentor_request = mentor_request_model.objects.filter(mentor_id=id)
    print(mentor_request)
    for req in mentor_request:
        req.mentee_request.request_posted_time = time_convert(req.mentee_request.request_posted_time)
    context = {
        'requests' : mentor_request
    }
    return render(request,'request/mentor-request.html',context)


def mentor_oper_view(request,oper,mentee_id,request_id):
    print(oper)
    print(mentee_id)
    if oper == 'accept':
        req = mentee_request_model.objects.get(id=request_id)
        req.status = 'accepted'
        req.save()
        req = mentor_request_model.objects.get(mentee_request_id=request_id)
        req.status = "accepted"
        req.save()
    elif oper == 'reject':
        req = mentee_request_model.objects.get(id=request_id)
        req.status = 'rejected'
        req.save()
        req = mentor_request_model.objects.get(mentee_request_id=request_id)
        req.status = "rejected"
        req.save()
    return redirect('/request/mentor/mentor_requests',permanent=True)
    
    