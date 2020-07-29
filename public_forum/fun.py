from .models import tag_with_question_id,tag
from django.utils import timezone
import random


def get_relevant_question(associated_tags,current_question_id):   # This method will return a random relevant question ids. This is filtered by tags.
    res_ids = []
    ids = list(tag_with_question_id.objects.filter(tag__in=associated_tags).values_list('question_id',flat=True).distinct())
    for i in range(5):
        try:
             rand_id = random.choice(ids)
             ids.remove(rand_id)
             res_ids.append(rand_id)
        except:
             break
    if current_question_id in res_ids:
        res_ids.remove(current_question_id)   # Because the relevant questions should not contain the same question
    return res_ids



def time_convert(posted_time):
    today = timezone.localtime().date()
    posted_time = timezone.localtime(value=posted_time)
    if today == posted_time.date():
        posted_time = posted_time.strftime('Today %I:%M %p') 
    else:
        posted_time = posted_time.strftime('%b %d, %Y')
    return posted_time

def random_tags():
    res = []
    tags = list(tag.objects.all().values_list('tag_name',flat=True))
    for i in range(10):
        rand_tag = random.choice(tags)
        tags.remove(rand_tag)
        res.append(rand_tag)
    print(res)
    return res
