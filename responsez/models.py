from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import date
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	city = models.CharField(max_length=30)
	birthdate = models.DateField()
	bio = models.CharField(max_length=250)
	friends = models.ManyToManyField("self",symmetrical=True)
	def __str__(self):
		return self.user.username
    #takes a user,return a dict
	def basic_info(self, asker=None):
		data = {}
		data['username'] = self.user.username
		data['fullname'] = self.user.first_name + ' ' + self.user.last_name
		if asker:
			data['isfriend'] = self.user.userprofile in asker.userprofile.friends.all() or self.user.username == asker.username
		else:
			data['isfriend'] = False
		return data
	#takes a user, return a dict
	def advanced_info(self,asker=None):
		data = self.basic_info(asker)
		data['age'] = self.age()
		data['bio'] = self.bio
		data['city'] = self.city
		return data

	def age(self):
		birthdate = self.birthdate
		today = date.today()
		return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


msgType = (
    (0, 'addFriend'),
    (1, 'message'),
    (2, 'eventInvite')
	)

class Notification(models.Model):
	typeNof = models.IntegerField(choices=msgType)
	toUser = models.ForeignKey(User, on_delete=models.CASCADE)
	userCaused = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
