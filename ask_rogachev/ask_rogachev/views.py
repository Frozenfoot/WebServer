from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login as authLogin
from questions import models
from questions import forms

def newQuestions(request):    
    return render_to_response('index.html', {'objects' :
        listing(request, models.Question.byDate.all())})

def hot(request):
    return render_to_response('hot.html', {
        'objects': listing(request, models.Question.byLikes.all()),
    })

def settings(request):
    return render_to_response('settings.html')

def login(request):

    user = request.user
    if user.is_authenticated():
        print ('User is_authenticated')
        print (user.username)
        return redirect('new')

    nextPage = request.GET.get('next')
    if nextPage is None:
        nextPage = 'new'

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            authLogin(request, form.user)
            print (form.user.username)
            return redirect(nextPage)
    else:
        form = forms.LoginForm()

    return render(request, 'login.html', {
        'form' : form
        })

def signup(request):
    return render_to_response('register.html')

def ask(request):
    return render_to_response('ask.html')

def question(request, questionId):
    question = get_object_or_404(models.Question, id = questionId)
    return render_to_response('question.html', {'question' : question, 
        'objects' : listing(request, question.answer_set.all().order_by('-like'))}) 

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