from django.shortcuts import render,redirect
from datetime import datetime
from django.http import JsonResponse
from .models import mentee_request_model
from user_signup.models import mentor_model
from public_forum.fun import time_convert

# Create your views here.
def request_view(request,mentor_id):
    
    mentee_id = request.session.get('id',None)
    if mentee_id is None:
        return redirect('user_login')
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
            new_request = mentee_request_model.objects.create(
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
                request_posted_time = datetime.now()
            )
            res = {
                "status" : "ok",
                "url": "my_request"
            }
            return JsonResponse(res)
    context = {
        'mentor_id' : mentor_id
    }
    return render(request,'request/request.html',context)



def my_request_view(request):
    role = request.session.get('role',None)
    if role is None or role.lower() == 'others' or role.lower() == 'mentor':
        return redirect('user_signup')
    id = request.session.get('id')
    my_request = mentee_request_model.objects.filter(mentee_id=id).order_by('-request_posted_time')
    for req in my_request:
        req.request_posted_time = time_convert(req.request_posted_time)

    context={
        "requests" : my_request
    }
    return render(request,'request/my_request.html',context)


def request_brief_view(request,id):
    return render(request,'request/request_brief.html')