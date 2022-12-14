# Generated by Django 3.2.15 on 2022-08-23 06:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_rename_name_room_room_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='投稿者名')),
                ('language', models.CharField(max_length=10, verbose_name='言語指定')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.room', verbose_name='ルーム名')),
            ],
        ),
    ]
