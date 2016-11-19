from django.core.management.base import BaseCommand, CommandError
from questions.models import *
from django.db import transaction
import random
import datetime


random.seed()


class Command(BaseCommand):
	def fillTags(self):
		n = 10
		with transaction.atomic():
			for i in range(1, n + 1):
				t = Tag(text = 'tag' + str(i))
				try:
					t.save()
					self.stdout.write('Tag ' + str(i) + ' saved')
				except:
					self.stdout.write('Error in tag ' + str(i))

	def fillLikes(self):
		n = 250
		with transaction.atomic():
			for i in range(1, n + 1):
				l = Like(likes = i % 10 + 1)
				try:
					l.save()
					self.stdout.write('Like ' + str(i) +' saved')
				except:
					self.stdout.write('Like ' + str(i) +' error')


	def fillQuestions(self):
		n = 100
		with transaction.atomic():
			for i in range(1, n + 1):
				q = Question(
					text = 'Question #' + str(i),
					like = Like.objects.get(id = 514 + i),
					author = Profile.objects.get(avatar = '140.jpg'),
					creationDate = datetime.datetime.now()
					)
				try:
					q.save()
					self.stdout.write('Question ' + str(i) +' saved')
				except:
					self.stdout.write('Question ' + str(i) +' error')


	def fillAnswers(self):
		n = 200
		with transaction.atomic():
			for i in range(1, n + 1):
				a = Answer(
					text = 'Answer #' + str(i),
					like = Like.objects.get(id = 514 + i),
					question = Question.objects.get(id = 7 + i % 100)
					)
				try:
					a.save()
					self.stdout.write('Answer ' + str(i) +' saved')
				except:
					self.stdout.write('Answer ' + str(i) +' error')


	def handle(self, *args, **options):
		#self.fillTags()
		#self.fillLikes()
		self.fillQuestions()
		self.fillAnswers()