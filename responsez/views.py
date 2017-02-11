from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.utils import timezone
from json import dumps
from .models import UserProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view,authentication_classes,permission_classes
# Create your views here.
import random



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def signup(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    a = {"status":""}
    try:
    	user = User.objects.create_user(username,email,password)
    	a['status'] = "success"
        user.first_name = "baruch"
        user.last_name = "varzil"
        user.save()
        profile = UserProfile(user=user,city="jers",birthdate=timezone.now(),bio="anal sex")
        profile.save()
    except IntegrityError:
    	a['status'] = "userexists"
    	a['user'] = username
    #except:
    #	a['status'] = "wrong"

    return HttpResponse(dumps(a))


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def myprofile(request):
    data = {}
    data['username'] = request.user.username
    data['name'] = request.user.first_name + ' ' +request.user.last_name
    return HttpResponse(dumps(data))

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def getAllusers(request):
    data = renderuserlist(request, User.objects.all())
    return HttpResponse(dumps(data))


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def userinfo(request,username):
    user = get_object_or_404(User,username=username)
    data = {}
    data['username'] = user.username
    data['name'] = user.first_name + ' ' + user.last_name
    data['isfriend'] = user.userprofile in request.user.userprofile.friends.all() or user.username == request.user.username
    return HttpResponse(dumps(data))


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def userfriends(request,username):
    user = get_object_or_404(User,username=username)
    data = renderuserlist(request,map(lambda x:x.user,user.userprofile.friends.all()))
    return HttpResponse(dumps(data))



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def addfriend(request,username):
    sender = request.user
    user = get_object_or_404(User,username=username)
    if not user.userprofile in sender.userprofile.friends.all():
        sender.userprofile.friends.add(user.userprofile)
    return HttpResponse("1")


def renderuserlist(request,lst):
    data = []
    friends = request.user.userprofile.friends.all()
    for user in lst:
        dic={}
        dic['username'] = user.username
        dic['fullname'] = user.first_name + ' ' + user.last_name
        dic['isfriend'] = user.userprofile in friends or user.username == request.user.username
        data.append(dic) 
    return data