from django.contrib import admin
from .models import UserProfile, Notification,BaseEvent,AttendStatus
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(AttendStatus)
admin.site.register(BaseEvent)