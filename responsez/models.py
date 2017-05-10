from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
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
		data = {
			'username' : self.user.username,
			'fullname' : self.user.first_name + ' ' + self.user.last_name
		}
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
    (1, 'friendship_accomplished'),
    (2, 'eventInvite')
	)

class Notification(models.Model):
	typeNof = models.IntegerField(choices=msgType)
	toUser = models.ForeignKey(User, on_delete=models.CASCADE)
	userCaused = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now())

	def get_info(self):
		return {
		'sender': self.userCaused.basic_info(asker=self.toUser),
		'type' : self.typeNof,
		'time_ago' : self.time_ago(),
		}
	def time_ago(self):
		now = timezone.now()
		date = self.date
		dt = now-date
		if dt.days > 365:
			return date.strftime('%B %d %y')
		if dt.days > 7:
			return date.strftime('%B %d')
		if dt.days > 0:
			return str(dt.days) + ' days ago'
		if dt.seconds > 3600:
			return str(dt.seconds/3600) +' hours ago'
		if dt.seconds > 60:
			return str(dt.seconds/60) + ' minutes ago'
		if dt.seconds < 60:
			return "now"
		return "???"


class BaseEvent(models.Model):
	invites = models.ManyToManyField(UserProfile,through='AttendStatus')
	event_id = models.AutoField(primary_key=True)
	admin = models.ForeignKey(User)
	date_time=models.DateTimeField()
	location=models.CharField(max_length=64)
	title=models.CharField(max_length=150)	
		

	def users_by_status(self,status):
		users = self.attendstatus_set.all()
		statuses = filter(lambda x:x.status == status,users)
		return map(lambda x:x.userprofile,statuses)

	def users_number_by_status(self):
		users = self.attendstatus_set.all()			
		return {
			'invited':len(filter(lambda x:x.status == 0,users)),
			'going':len(filter(lambda x:x.status == 1,users)),
			'maybe':len(filter(lambda x:x.status == 2,users)),
			'not_going':len(filter(lambda x:x.status == 3,users)),}

	def info_for_feed(self):
		info = self.users_number_by_status()
		info['inviter'] = self.admin.userprofile.basic_info()
		info['location'] = self.location
		info['name'] = self.title
		info['hour'] =self.date_time.hour
		info['min'] = self.date_time.minute
		info['date'] = self.date_time.strftime('%B %d')
		info['id'] = str(self.event_id)
		info['information'] = ""
		return info

	

	def __unicode__(self):
		return self.title



atend_status = (
    (0, 'invited'),
    (1, 'going'),
    (2, 'maybe'),
    (3, 'not_going'),
	)

class AttendStatus(models.Model):
	userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
	baseevent = models.ForeignKey(BaseEvent,on_delete=models.CASCADE)
	status = models.IntegerField(choices=atend_status)
	

	def __unicode__(self):
		return self.userprofile.user.username + "==>" + self.baseevent.title	