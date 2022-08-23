from django.db import models
from django.utils import timezone

import uuid


class Room(models.Model):
    dt = models.DateField(verbose_name="投稿日時",default=timezone.now)
    room_name = models.CharField(verbose_name="ルーム名",max_length=100)

class Chat(models.Model):
    dt = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)

    #ChatUserと1対多を組むと、ChatUserが消えた時、Chatの表示にも影響するため、ここには投稿当時のデータを記録する
    room = models.ForeignKey(Room,verbose_name="ルーム名",on_delete=models.CASCADE)
    name = models.CharField(verbose_name="投稿者名",max_length=100)

    #ipアドレスは投稿されるたびに記録する
    ip = models.GenericIPAddressField(verbose_name="IPアドレス")

    comment = models.TextField(verbose_name="原文コメント")
    ja_comment = models.TextField(verbose_name="日本語コメント")
    en_comment = models.TextField(verbose_name="英語コメント")
    zh_comment = models.TextField(verbose_name="中国語コメント")
    ko_comment = models.TextField(verbose_name="韓国語コメント")
    de_comment = models.TextField(verbose_name="ドイツ語コメント")
    fr_comment = models.TextField(verbose_name="フランス語コメント")


class ChatUser(models.Model):

    id          = models.UUIDField( default=uuid.uuid4, primary_key=True, editable=False )

    #Cookieに記録されていた名前とルームをChatUserに記録。Cookieには上記idのみを記録する
    name        = models.CharField(verbose_name="投稿者名",max_length=100)
    room        = models.ForeignKey(Room,verbose_name="ルーム名",on_delete=models.CASCADE,null=True,blank=True)

    language    = models.CharField(verbose_name="言語指定",max_length=10)

