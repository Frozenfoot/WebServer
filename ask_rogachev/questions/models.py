from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	avatar = models.ImageField(
		upload_to = 'avatars/%Y/%m/%d/%H/',
		max_length = 100, 
		default = '140.jpg'
		)

	user = models.OneToOneField(
		User,
		on_delete = models.CASCADE,
		null = True
		)

	def __str__(self):
		return self.user.username


class NewQuestionsManager(models.Manager):
	def get_queryset(self):
		return super(NewQuestionsManager, self).get_queryset().order_by('-creationDate')[0:6]


class QuestionManager(models.Manager):
	def hot(self):
		return self.annotate(likes = models.Count('questionlike')).order_by('-likes')[0:6]


class TopAnswersManager(models.Manager):
	def hot(self):
		return self.annotate(likes = models.Count('answerlike')).order_by('-likes')


class Question(models.Model):
	text = models.TextField()
	title = models.CharField(max_length = 50)
	author = models.ForeignKey(Profile)
	creationDate = models.DateTimeField(auto_now_add = True)

	def likes(self):

		likes = 0
		for item in self.questionlike_set.all():
			if item.like:
				likes += 1

			else:
				likes -= 1

		return likes

	objects = QuestionManager()
	#byLikes = TopQuestionsManager()
	byDate = NewQuestionsManager()

	def __str__(self):
		return self.title


class QuestionLike(models.Model):
	profile = models.ForeignKey(Profile)
	question = models.ForeignKey(Question)
	like = models.BooleanField(default = True)

	class Meta:
		unique_together = (('profile', 'question'))


class Tag(models.Model):
	text = models.CharField(max_length = 10)
	question = models.ManyToManyField(Question)
	objects = models.Manager()

	def __str__(self):
		return self.text


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	text = models.CharField(max_length = 200)
	author = models.ForeignKey(Profile)
	creationDate = models.DateTimeField(auto_now_add = True)
	top = TopAnswersManager()
	objects = models.Manager()
	correct = models.BooleanField(default = False)

	def likes(self):

		likes = 0
		for item in self.answerlike_set.all():
			if item.like:
				likes += 1

			else:
				likes -= 1

		return likes

	def __str__(self):
		return self.title


class AnswerLike(models.Model):
	profile = models.ForeignKey(Profile)
	answer = models.ForeignKey(Answer)
	like = models.BooleanField(default = True)

	class Meta:
		unique_together = (('profile', 'answer'))
