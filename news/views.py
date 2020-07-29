from django.shortcuts import render,redirect
from .models import news_model
from public_forum.fun import time_convert
import urllib
import json

# Create your views here.
def news_home_view(request):
    type = request.GET.get('type','null')
    type_list = ['business','general','science','technology','entertainment']
    if type not in type_list:
        type = 'business'
    news = news_model.objects.filter(type=type)
    for n in news:
        n.published_at = time_convert(n.published_at)
    topics = [('business','info'),('general','warning'),('science','success'),('technology','danger'),('entertainment','primary')]
    context = {
        'news' : news,
        'topics' : topics,
        'type' : type 
    }
    return render(request,'news/news_home.html',context)

def request_news_view(request):
    news_model.objects.all().delete()
    for query in ['business','general','science','technology','entertainment']:
        q = "q=" + query
        url = "https://newsapi.org/v2/everything?"+q+"&language=en&sortBY=publishedAt&apiKey=766ca5c12a384a9cbf929e25a5186097&pageSize=20"
        data = urllib.request.urlopen(url).read()
        data = json.loads(data)
        status = data['status']
        print('status',status)
        print('total results',data['totalResults'])
        if status == 'ok':
            results = data['totalResults']
            if results > 20:
                results = 20
            articles = data['articles']
            for i in range(results):
                    print('inside loop')
                    title = articles[i]["title"]
                    author = articles[i]['author']
                    if author is None:
                        author = 'N/A'
                    url = articles[i]["url"]
                    url_to_image = articles[i]["urlToImage"]
                    if url_to_image is None:
                        url_to_image = '#'
                    published_at = articles[i]['publishedAt']
                    content = articles[i]['content']
                    if content is None:
                        content = " "
                    if len(content)>196:
                        content = content[:197] + "..."
                    else:
                        content = content + "..."
                    type = query
                    obj = news_model(
                    title = title,
                    author = author,
                    url = url,
                    url_to_image = url_to_image,
                    content = content,
                    published_at = published_at,
                    type = type
                    )
                    obj.save()
                    print('obj saved')
    print('done')
    return redirect('/news?type=business')