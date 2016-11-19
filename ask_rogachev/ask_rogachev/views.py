from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from questions import models

def newQuestions(request):    
    return render_to_response('index.html', {'objects' :
        listing(request, models.Question.byDate.all())})

def hot(request):
    return render_to_response('hot.html', {'objects' :
        listing(request, models.Question.byLikes.all())})

def settings(request):
    return render_to_response('settings.html')

def login(request):
    return render_to_response('login.html')

def signup(request):
    return render_to_response('register.html')

def ask(request):
    return render_to_response('ask.html')

def question(request, questionId):
    question = get_object_or_404(models.Question, id = questionId)
    return render_to_response('question.html', {'question' : question, 
        'objects' : listing(request, question.answer_set.all().order_by('-like__likes'))}) 

def tag(request, tagName):
    tag = get_object_or_404(models.Tag, text = tagName)
    questionList = []
    for item in tag.question.all():
        questionList.append(item)
    return render_to_response('tag.html', {'tagName' : tagName,
        'objects' : listing(request, questionList)})

def listing(request, respondList, elementsOnPage = 3):
    paginator = Paginator(respondList, elementsOnPage)

    page = request.GET.get('page')
    try:
        result = paginator.page(page)

    except PageNotAnInteger:
        result = paginator.page(1)

    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return result