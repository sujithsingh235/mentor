from .models import tag_with_question_id
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