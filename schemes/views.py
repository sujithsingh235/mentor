from django.shortcuts import render
from .models import scheme
from django.http import Http404,HttpResponse
# Create your views here.


def government_schemes_view(request):
    schemes_head = scheme.objects.all().values_list('id','head')
    scheme_tup = []
    if len(schemes_head)!=0:
        exist = True
    else:
        exist = False
    for i in schemes_head:  # abbrevation extraction process
        lst = list(i)
        ind = lst[1].find('(')
        end = lst[1].find(')',ind)
        if ind != -1 and end != -1:
            abb = lst[1][ind : end+1]
            lst[1] = lst[1][:ind]
        else:
            abb = None
        scheme_tup.append((lst[0],lst[1],abb))
    print(scheme_tup)
    auth_uname = request.session.get('username',None)
    auth_uid = request.session.get('id',None)
    auth_role = request.session.get('role',None)
    context = {
        'schemes' : scheme_tup,
        'exist' : exist,
        'auth_uname' : auth_uname,
        'auth_uid' : auth_uid,
        'auth_role' : auth_role
    }
    return render(request,'schemes/schemes.html',context)



def scheme_explain_view(request,id):
    try:
        schemes = scheme.objects.get(id=id)
    except:
        raise Http404('The scheme is not found in the database')
    if schemes.more_info_link == "":
        link_exists = False
    else:
        link_exists = True
    extra_schemes = scheme.objects.exclude(id=id)
    if len(extra_schemes) > 4:
        extra_schemes = extra_schemes[:4]
    auth_uname = request.session.get('username',None)
    auth_uid = request.session.get('id',None)
    auth_role = request.session.get('role',None)
    context = {
        'scheme' : schemes,
        'link_exists' : link_exists,
        'extra_schemes' : extra_schemes,
        'auth_uname' : auth_uname,
        'auth_uid' : auth_uid,
        'auth_role' : auth_role
    }
    return render(request,'schemes/scheme_explain.html',context)