from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	avatar = models.CharField(max_length = 20, null = True)
	user = models.OneToOneField(
		User,
		on_delete = models.CASCADE,
		null = True
	)

	def __str__(self):
		return self.avatar


class Like(models.Model):
	likes = models.IntegerField(default = 0)

	def __str__(self):
		return str(self.likes)


class NewQuestionsManager(models.Manager):
	def get_queryset(self):
		return super(NewQuestionsManager, self).get_queryset().order_by('-creationDate')[0:6]


class TopQuestionsManager(models.Manager):
	def get_queryset(self):
		return super(TopQuestionsManager, self).get_queryset().order_by('-like__likes')[0:6]


class Question(models.Model):
	text = models.CharField(max_length = 200)
	author = models.ForeignKey(Profile, on_delete = models.CASCADE)
	creationDate = models.DateTimeField()
	like = models.ForeignKey(
		Like,
		on_delete = models.CASCADE,
	)
	objects = models.Manager()
	byLikes = TopQuestionsManager()
	byDate = NewQuestionsManager()

	def __str__(self):
		return self.text


class Tag(models.Model):
	text = models.CharField(max_length = 10)
	question = models.ManyToManyField(Question)
	objects = models.Manager()

	def __str__(self):
		return self.text


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	text = models.CharField(max_length = 200)
	like = models.OneToOneField(
		Like,
		on_delete = models.CASCADE,
	)

	def __str__(self):
		return self.text
