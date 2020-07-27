from django.shortcuts import render

import urllib
import json
# Create your views here.
def news_view(request):
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=766ca5c12a384a9cbf929e25a5186097"
    data = urllib.request.urlopen(url).read()
    data = json.loads(data)
    article = data['articles'][0]
    title = article['title']
    desc  = article['description']
    link = article['url']
    print(title)
    print(desc)
    print(link)
    context = {
        'title' : title,
        'desc' : desc,
        'link' : link
    }
    return render(request,'news/news.html',context)