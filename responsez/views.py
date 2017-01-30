from django.shortcuts import render
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

