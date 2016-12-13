from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login as authLogin
from django.contrib.auth import logout as authLogout
from django.contrib.auth import authenticate
from questions import models
from questions import forms


def logout(request):

    print (request.get_host())
    authLogout(request)
    nextPage = request.GET.get('next')
    if nextPage:
        return redirect(nextPage)
    else:
        return redirect('new')


def newQuestions(request):   

    return render(request, 'index.html', {
        'objects' : listing(request, models.Question.byDate.all())
        })


def hot(request):

    return render(request, 'hot.html', {
        'objects': listing(request, models.Question.byLikes.all()),
    })


def settings(request):
    
    user = request.user

    if not user.is_authenticated():
        return redirect('new')

    data = {'username' : user.username, 'email' : user.email}
    if request.method == 'POST':
        form = forms.SettingsForm(request.POST, request.FILES, initial = data)
        if form.is_valid():
            form.save(user.profile)
    else:
        form = forms.SettingsForm(initial = data)

    return render(request, 'settings.html', {
        'form' : form
        })


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

    user = request.user

    if user.is_authenticated():
        return redirect('new')

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'] )
            authLogin(request, user)
            return redirect('login')
    else:
        form = forms.SignUpForm()

    return render(request, 'register.html', {
            'form': form,
})


def ask(request):

    user = request.user
    if not user.is_authenticated():
        return redirect('login')

    if request.method == 'POST':
        form = forms.AskForm(request.POST)
        if form.is_valid():
            question = form.save(user.id)
            return redirect('question', question.id)
    else:
        form = forms.AskForm()

    return render(request, 'ask.html', {
            'form': form,
    })


def question(request, questionId):

    user = request.user

    question = get_object_or_404(models.Question, pk = questionId)
    answers = question.answer_set.all()

    if request.method == 'POST':
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            form.save(questionId, user.id)
            paginator = Paginator(answers, 3)
            return render(request, 'question.html', {
                'form' : forms.AnswerForm(),
                'question': question,
                'objects' : paginator.page(paginator.num_pages),
                'id': questionId,
            }) 
    else:
        form = forms.AnswerForm()

    return render(request, 'question.html', {
            'form': form,
            'objects' : listing(request, question.answer_set.all().order_by('-like')),
            'question': question,
            'id': questionId,
    }) 


def tag(request, tagName):

    tag = get_object_or_404(models.Tag, text = tagName)
    questionList = []
    for item in tag.question.all():
        questionList.append(item)
    return render(request, 'tag.html', {'tagName' : tagName,
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