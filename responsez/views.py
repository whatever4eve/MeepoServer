from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def signup(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']

    user = User.objects.create_user(username,email,password)
    user.save()
    return HttpResponse(username+' '+password+' ',email)