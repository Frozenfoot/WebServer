from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import *
from django.core import validators
from .models import *


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