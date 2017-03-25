from django.conf.urls import url
from rest_framework.authtoken import views as tviews
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/',views.signup,name='signup'),
    url(r'^signin/',tviews.obtain_auth_token,name='signin'),
    url(r'^allusers/',views.getAllusers,name='appusers'),
    url(r'^notifications/',views.getNotifications,name='notifics'),
    url(r'^(?P<username>[a-zA-Z0-9_]{3,12})/info/',views.userinfo,name='userinfo'),
    url(r'^(?P<username>[a-zA-Z0-9_]{3,12})/friends/',views.userfriends,name='userfriends'),
    url(r'^(?P<username>[a-zA-Z0-9_]{3,12})/addfriend/',views.addfriend,name='addfriend'),
]