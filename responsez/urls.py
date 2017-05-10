from django.conf.urls import url
from rest_framework.authtoken import views as tviews
from . import views,event_views

urlpatterns = [
    url(r'^signup/',views.signup,name='signup'),
    url(r'^signin/',tviews.obtain_auth_token,name='signin'),
    url(r'^allusers/',views.getAllusers,name='appusers'),
    url(r'^notifications/',views.getNotifications,name='notifics'),
    url(r'^feed/',event_views.getFeed,name="feed"),
    url(r'^(?P<username>[a-zA-Z0-9_]{3,12})/info/',views.userinfo,name='userinfo'),
    url(r'^(?P<username>[a-zA-Z0-9_]{3,12})/friends/',views.userfriends,name='userfriends'),
    url(r'^(?P<username>[a-zA-Z0-9_]{3,12})/addfriend/',views.addfriend,name='addfriend'),

    url(r'^events/create_normal_event/',event_views.create_normal_event),
    url(r'^events/(?P<event_id>[0-9]+)/going_users/',event_views.going_users),
    url(r'^events/(?P<event_id>[0-9]+)/maybe_users/',event_views.maybe_users),
    url(r'^events/(?P<event_id>[0-9]+)/invited_users/',event_views.invited_users),
    url(r'^events/(?P<event_id>[0-9]+)/set_going/',event_views.set_going),
    url(r'^events/(?P<event_id>[0-9]+)/maybe_going/',event_views.set_maybe),
    url(r'^events/(?P<event_id>[0-9]+)/set_not_going/',event_views.not_going),
]