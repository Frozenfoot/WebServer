from django.core.management.base import BaseCommand, CommandError
from questions.models import *
from django.db import transaction
import random
import datetime


random.seed()


class Command(BaseCommand):

	def getRandomId(self, idList):
		index = random.randint(0, idList.count() - 1)
		randomId = idList[index]
		return randomId

	def fillTags(self):
		n = 100
		for i in range(1, n + 1):
			t = Tag(text = 'tag_' + str(i))
			try:
				with transaction.atomic():
					t.save()
				self.stdout.write('Tag ' + str(i) + ' saved')
			except:
				self.stdout.write('Error in tag ' + str(i))


	def fillProfiles(self):
		n = 100

		for i in range (1, n + 1):
			username = 'user_' + str(i)
			password = '123456Aa'
			try:
				user = User.objects.create_user(password = password, username = username)
				p = Profile(
					avatar = '/' + str(i) + '.jpg',
					user = user
					)
				with transaction.atomic():
					p.save()
				self.stdout.write('Profile ' + str(i) + ' saved')
			except:
				self.stdout.write('Error in profile ' + str(i))



	def fillQuestions(self):
		n = 1000

		authorIDs = Profile.objects.all().values_list('id', flat = True)
		tagIDs = Tag.objects.all().values_list('id', flat = True)

		for i in range(1, n + 1):
			number = str(i)
			title = 'Question title ' + number
			text = ('Question text ' + number + ' ') * 10
			likes = random.randint(0, 20)
			creationDate = datetime.datetime.now()
			authorID = self.getRandomId(authorIDs)

			
			q = Question(
				title = title,
				text = text,
				like = likes,
				creationDate = creationDate,
				author_id = authorID
				)
			with transaction.atomic():
				q.save()
			for j in range(random.randint(1, 3)):
				tagID = self.getRandomId(tagIDs)
				q.tag_set.add(tagID)
			with transaction.atomic():
				q.save()

			self.stdout.write('Question ' + str(i) + 'saved')


	def fillAnswers(self):
		questions = Question.objects.all()
		numberOfQuestions = questions.count()
		authorIDs = Profile.objects.all().values_list('id', flat = True)

		i = 0
		for q in questions:
			n = 100
			k = random.randint(0, 5)
			i += 1
			for j in range(k):
				j += 1
				number = str(j)
				text = ('Answer text ' + number + ' ') * 5
				likes = random.randint(0, 6)

				authorID = self.getRandomId(authorIDs)

				a = Answer(
					text = text,
					like = likes,
					author_id = authorID,
					question_id = q.id,
					)
				with transaction.atomic():
					a.save()
				self.stdout.write('Answer ' + str(i) + ' saved')


	def handle(self, *args, **options):
		self.fillTags()
		#self.fillProfiles()
		self.fillQuestions()
		self.fillAnswers()