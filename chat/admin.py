from django.contrib import admin

from .models import Room, Chat, ChatUser

class RoomAdmin(admin.ModelAdmin):
    list_display = ["room_name", "dt"]

class ChatAdmin(admin.ModelAdmin):
    list_display = ["name", "dt", "comment", "ip", "room"]

class ChatUserAdmin(admin.ModelAdmin):

    list_display=["id","name","room","language",]


admin.site.register(Room, RoomAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatUser, ChatUserAdmin)
