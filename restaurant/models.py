from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Restaurant(models.Model):
	"""docstring for Restaurant"""
	name = models.CharField(max_length=120)
	description = models.TextField()
	opening_time = models.TimeField()
	closing_time = models.TimeField()
	logo = models.ImageField()
	owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return "/restaurants/detail/%s/"%(self.id)


class Item(models.Model):
	"""docstring for Restaurant"""
	name = models.CharField(max_length=120)
	description = models.TextField()
	price = models.IntegerField()
	restaurant = models.ForeignKey(Restaurant, default=1, on_delete=models.CASCADE)

	def __str__(self):
		return self.name


class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)