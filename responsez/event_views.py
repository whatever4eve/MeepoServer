from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from json import dumps

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from datetime import datetime

from .models import BaseEvent,AttendStatus

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def getFeed(request):
	events=request.user.baseevent_set.all().order_by('-date_time')
	data = []
	for event in events:
		data.append(event.info_for_feed())

	return HttpResponse(dumps(data))


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_normal_event(request):
	admin = request.user
	invites = request.user.userprofile.friends.all()
	title = request.POST['title']
	location = request.POST['location']
	year = int(request.POST['year'])
	month = int(request.POST['month'])
	day = int(request.POST['day'])
	hour = int(request.POST['hour'])
	mins = int(request.POST['min'])
	date_time = datetime(year,month,day,hour,mins)
	event = BaseEvent.objects.create(title=title,admin=admin,location=location,date_time=date_time)
	event.save()
	for invite in invites:
		new_invite = AttendStatus.objects.create(baseevent=event,userprofile=invite,status=0)
		new_invite.save()
	return HttpResponse("1")

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def going_users(request,event_id):
	event = get_object_or_404(BaseEvent,event_id=int(event_id))
	users = event.users_by_status(1)
	return HttpResponse(dumps([user.basic_info(request.user) for user in users]))


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def maybe_users(request,event_id):
	event = get_object_or_404(BaseEvent,event_id=int(event_id))
	users = event.users_by_status(2)
	return HttpResponse(dumps([user.basic_info(request.user) for user in users]))


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def invited_users(request,event_id):
	event = get_object_or_404(BaseEvent,event_id=int(event_id))
	users = event.users_by_status(0)
	return HttpResponse(dumps([user.basic_info(request.user) for user in users]))


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def set_going(request,event_id):
	event = get_object_or_404(BaseEvent,event_id=int(event_id))
	status = AttendStatus.objects.get(baseevent=event,userprofile=request.user.userprofile)
	status.status = 1
	status.save()
	return HttpResponse(dumps(event.info_for_feed()))

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def set_maybe(request,event_id):
	event = get_object_or_404(BaseEvent,event_id=int(event_id))
	status = AttendStatus.objects.get(baseevent=event,userprofile=request.user.userprofile)
	status.status = 2
	status.save()
	return HttpResponse(dumps(event.info_for_feed()))

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def not_going(request,event_id):
	event = get_object_or_404(BaseEvent,event_id=int(event_id))
	status = AttendStatus.objects.get(baseevent=event,userprofile=request.user.userprofile)
	status.status = 3
	status.save()
	return HttpResponse(dumps(event.info_for_feed()))