from django.conf.urls import url
from rest_framework.authtoken import views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/',views.signup,name='signup'),
    url(r'^signin/',views.obtain_auth_token,name='signin'),
]