from django.contrib import admin
from .models import Room, Message, Topic, UserProfile, WebsocketSessions

# from .models import User
# # Register your models here.

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(WebsocketSessions)

admin.site.register(UserProfile)
