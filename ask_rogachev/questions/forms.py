from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import *
from django.core import validators
from .models import *

class AnswerForm(forms.Form):
	text = forms.CharField(widget = forms.Textarea(attrs = {
		'class': 'form-control input-lg', 
		'placeholder': 'Enter your answer here',
		'rows': 5,
		}))

	def save(self, question_id, user_id = 228):
		data = self.cleaned_data
		answer = Answer(text = data['text'], question_id = question_id, author_id = user_id)
		print (answer.text)
		print (answer.question.title)
		answer.save()

class TagField(forms.Field):
	def getTags(self, tags):
		if tags in validators.EMPTY_VALUES:
			return []

		tags = [item.strip() for item in tags.split(',') if item.strip()]
		return tags

	def clean(self, tags):
		tags = self.getTags(tags)
		self.validate(tags)
		self.run_validators(tags)
		return tags


class AskForm(forms.Form):
	title = forms.CharField(widget = forms.TextInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Enter the title here'
		}))
	text = forms.CharField(widget = forms.Textarea(attrs = {
		'class': 'form-control input-lg', 
		'placeholder': 'Enter your question here',
		'rows': 20,
		}))
	tags = TagField(widget = forms.TextInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Enter tags separated by comma'
		}))

	def save(self, user_id):
		data = self.cleaned_data
		profileID = User.objects.get(id = user_id).profile.id
		question = Question(title = data['title'], text = data['text'], author_id = profileID)
		question.save()
		tags = data['tags']
		for t in tags:
			tag = Tag.objects.get_or_create(text = t)[0]
			question.tag_set.add(tag)
		question.save()

		return question


class SettingsForm(forms.Form):

	username = forms.CharField(widget = forms.TextInput(attrs = {
		'class': 'form-control input-lg',
		}))

	email = forms.EmailField(widget = forms.EmailInput(attrs = {
		'class': 'form-control input-lg',
		}))

	avatar = forms.ImageField(required = False, widget = forms.FileInput(attrs = {
		'class': 'form-control input-lg',
		}))

	def clean_username(self):
		username = self.cleaned_data['username']
		if self.fields['username'].has_changed(initial = self.initial['username'], \
			data = username):
			if User.objects.filter(username = username).exists():
				raise forms.ValidationError('Login already exists!')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if self.fields['email'].has_changed(initial = self.initial['email'], \
			data = email):
			if User.objects.filter(email = email).exists():
				raise forms.ValidationError('Email already exists!')
		return email

	def save(self, user):
		data = self.cleaned_data
		user.username = data['username']
		user.email = data['email']
		if data['avatar'] is not None:
			user.avatar = data['avatar']
		user.save()


class LoginForm(forms.Form):
	username = forms.CharField(widget = forms.TextInput(attrs = {
		'class' : 'form-control',
		'placeholder' : 'Login'
		}))

	password = forms.CharField(widget = forms.PasswordInput(attrs = {
		'class' : 'form-control',
		'placeholder' : 'Password'
		}))

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		self.user = authenticate(username = username, password = password)

		if self.user is None:
			raise forms.ValidationError('Incorrect login or password')


class SignUpForm(forms.Form):

	username = forms.CharField(widget = forms.TextInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Login'
		}))

	email = forms.EmailField(widget = forms.EmailInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'E-mail'
		}))

	password = forms.CharField(widget = forms.PasswordInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Password'
		}))

	repeat_password = forms.CharField(widget = forms.PasswordInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Repeat password'
		}))

	avatar = forms.ImageField(required = False, widget = forms.FileInput(attrs = {
		'class': 'form-control input-lg'
		}))
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username = username):
			raise forms.ValidationError('Login is already exists!')
		return username

	def clean_repeat_password(self):
		data = self.cleaned_data
		if data['password'] != data['repeat_password']:
			raise forms.ValidationError('Different passwords!')
		return data['repeat_password']

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email = email):
			raise forms.ValidationError('Email is already exists!')
		return email

	def save(self):
		data = self.cleaned_data
		username = data['username']
		email = data['email']
		password = data['password']
		user = User.objects.create_user(username = username, email = email, password = password)
		if self.cleaned_data['avatar'] is not None:
			profile = Profile(user = user, avatar = self.cleaned_data['avatar'])
			profile.save()
		else:
			profile = Profile(user = user)
			profile.save()