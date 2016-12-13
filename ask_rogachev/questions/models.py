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


class TopQuestionsManager(models.Manager):
	def get_queryset(self):
		return super(TopQuestionsManager, self).get_queryset().order_by('-like__likes')[0:6]


class Question(models.Model):
	text = models.TextField()
	title = models.CharField(max_length = 50)
	author = models.ForeignKey(Profile, on_delete = models.CASCADE)
	creationDate = models.DateTimeField(auto_now_add = True)

	objects = models.Manager()
	byLikes = TopQuestionsManager()
	byDate = NewQuestionsManager()

	def __str__(self):
		return self.title

class Like(models.Model):
	question = models.OneToOneField(
		Question,
		on_delete = models.CASCADE,
		)

	likes = models.IntegerField(default = 0)
	user = models.ManyToManyField(User)

	def __str__(self):
		return self.likes



class Tag(models.Model):
	text = models.CharField(max_length = 10)
	question = models.ManyToManyField(Question)
	objects = models.Manager()

	def __str__(self):
		return self.text


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	text = models.CharField(max_length = 200)
	like = models.PositiveIntegerField(default = 0)
	author = models.ForeignKey(Profile)
	creationDate = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.title
