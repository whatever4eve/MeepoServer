from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from json import dumps
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
    except IntegrityError:
    	a['status'] = "userexists"
    	a['user'] = username
    except:
    	a['status'] = "wrong"

    return HttpResponse(dumps(a))
    
    