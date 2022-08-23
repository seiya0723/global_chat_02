from django import forms
from .models import Chat, Room, ChatUser

"""
class RoomEnterForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["name", "room"]



class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["room_name"]

"""


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["comment","ip", "room", "name", "ja_comment", "en_comment", "zh_comment", "ko_comment", "de_comment", "fr_comment"]

class ChatBeforeForm(forms.ModelForm):
    class Meta:
        model = Chat
        #TODO:roomとnameとipがない
        fields = ["comment","ip", "room", "name",]




class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["room_name"]

class RoomEnterForm(forms.ModelForm):
    class Meta:
        model = ChatUser
        fields = ["room"]

class ChatUserForm(forms.ModelForm):
    class Meta:
        model = ChatUser
        fields = ["name","room","language"]




#ロングポーリング用のフォームクラス
class ChatFirstForm(forms.Form):

    #Topicのidに基づく
    first = forms.IntegerField()
