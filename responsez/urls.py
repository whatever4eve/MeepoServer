from django.conf.urls import url
from rest_framework.authtoken import views as tviews
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/',views.signup,name='signup'),
    url(r'^signin/',tviews.obtain_auth_token,name='signin'),
    url(r'^myprofile/',views.myprofile,name='profile'),
    url(r'^allusers/',views.getAllusers,name='appusers'),
]