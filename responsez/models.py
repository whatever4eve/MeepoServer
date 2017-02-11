from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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
