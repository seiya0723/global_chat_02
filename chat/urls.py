from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [  
    path('', views.entrance, name="entrance"),
    path('index/', views.index, name="index"),
    path('chat_room/<int:pk>/', views.chat_room, name="chat_room"),

    path('index_exit/', views.index_exit, name="index_exit"),
    path('chat_room_exit/', views.chat_room_exit, name="chat_room_exit"),

    path('refresh/<int:pk>/', views.refresh, name="refresh"),
]
