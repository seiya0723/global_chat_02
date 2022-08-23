import pkgutil
from django.shortcuts import render, redirect

from django.views import View

from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Chat, Room, ChatUser
from .forms import RoomEnterForm, ChatForm, ChatBeforeForm, RoomForm, ChatFirstForm, ChatUserForm

import urllib
import time

from googletrans import Translator


class EntranceView(View):

    def get(self, request, *args, **kwargs):

        #TODO:ここでCookieが存在する場合はChatUserを検索
        if "id" in request.COOKIES:

            #Cookieに記録されているChatUserのidを取得
            chat_user_id = urllib.parse.unquote(request.COOKIES["id"])
            chat_user    = ChatUser.objects.filter(id=chat_user_id).first()

            #roomの指定がある場合はroomへリダイレクト
            if chat_user.room:
                return redirect("chat:chat_room", chat_user.room.id)
            else:
                #部屋一覧のページへリダイレクト
                return redirect("chat:index")


        return render(request, "chat/entrance.html")

    def post(self, request, *args, **kwargs):

        form        = ChatUserForm(request.POST)

        if not form.is_valid():
            return redirect("chat:entrance")

        chat_user    = form.save()

        response    = redirect("chat:index")

        #TIPS:UUIDは文字列に直して格納する
        response.set_cookie("id", urllib.parse.quote(str(chat_user.id)))

        return response

entrance    = EntranceView.as_view()


class IndexView(View):
    def get(self, request, *args, **kwargs):
        #チャットのルーム選択。(ルーム一覧をcontextに入れる)
        context = {}
        context["rooms"] = Room.objects.order_by("-dt")

        return render(request, "chat/index.html", context)

    def post(self, request, *args, **kwargs):
        #ルームの新規作成
        room_form   = RoomForm(request.POST)



        #ChatUserの存在確認
        if "id" not in request.COOKIES:
            return redirect("chat:entrance")

        #Cookieに記録されているChatUserのidを取得
        chat_user_id = urllib.parse.unquote(request.COOKIES["id"])
        chat_user    = ChatUser.objects.filter(id=chat_user_id).first()

        if not chat_user:
            return redirect("chat:entrance")



        if room_form.is_valid():
            #ルーム新規作成
            room            = room_form.save()
            copied          = request.POST.copy()
            copied["room"]  = room.id

            form            = RoomEnterForm(copied, instance=chat_user)
        else:
            #既存ルームに入室

            form            = RoomEnterForm(request.POST, instance=chat_user)


        if not form.is_valid():
            print("RoomEnterFormのバリデーションエラー")
            return redirect("chat:index")

        #ChatUserにroomを記録
        chat_user    = form.save()

        #リダイレクトする
        return redirect("chat:chat_room", chat_user.room.id)

index = IndexView.as_view()



class ChatRoomView(View):
    def get(self, request, pk, *args, **kwargs):
      
        context = {}
        context["room"] = Room.objects.filter(id=pk).first()
        context["chats"] = Chat.objects.filter(room=pk).order_by("dt")

        if "id" not in request.COOKIES:
            return redirect("chat:entrance")
        
        return render(request, "chat/chat_room.html", context)

    
    def post(self, request, pk, *args, **kwargs):
        
        data = {"error": True}

        #ChatUserの存在確認
        if "id" not in request.COOKIES:
            return redirect("chat:entrance")

        #Cookieに記録されているChatUserのidを取得
        chat_user_id = urllib.parse.unquote(request.COOKIES["id"])
        chat_user    = ChatUser.objects.filter(id=chat_user_id).first()

        if not chat_user:
            return redirect("chat:entrance")


        #(リバース)プロキシサーバー有りと想定してIPアドレスのリストを取得
        ip_list = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_list:
            ip  = ip_list.split(',')[0]#そのうちの最初のIPアドレス(クライアントのグローバルIPアドレス)
        else:
            ip  = request.META.get('REMOTE_ADDR')#このサーバーに直接アクセスしてきたIPアドレスを取得

        copied          = request.POST.copy()
        copied["ip"]    = ip
        copied["room"]  = pk
        copied["name"]  = chat_user.name

        form = ChatBeforeForm(copied)

        if not form.is_valid():
            print(form.errors)
            print("form.is_valid()失敗1")
            return JsonResponse(data)

        cleaned = form.clean()
        comment = cleaned["comment"]
         
        # copied = request.POST.copy()
        translator = Translator()
        copied["ja_comment"] = translator.translate(comment, dest="ja").text
        copied["en_comment"] = translator.translate(comment, dest="en").text
        copied["zh_comment"] = translator.translate(comment, dest="zh-CN").text
        copied["ko_comment"] = translator.translate(comment, dest="ko").text
        copied["de_comment"] = translator.translate(comment, dest="de").text
        copied["fr_comment"] = translator.translate(comment, dest="fr").text

        form = ChatForm(copied)
        if not form.is_valid():
            print(form.errors)
            print("form.is_valid()失敗2")
            return JsonResponse(data)

        form.save()

        context = {}
        context["chats"] = Chat.objects.filter(room=pk).order_by("dt")

        data["error"] = False
        #render_to_stringはレンダリング結果を文字列にして返す
        data["content"] = render_to_string("chat/content.html", context, request)

        return JsonResponse(data)

chat_room = ChatRoomView.as_view()


class IndexExitView(View):
    def post(self, request, *args, **kwargs):

        if "id" not in request.COOKIES:
            return redirect("chat:entrance")

        #Cookieに記録されているChatUserのidを取得
        chat_user_id = urllib.parse.unquote(request.COOKIES["id"])
        chat_user    = ChatUser.objects.filter(id=chat_user_id).first()

        if not chat_user:
            return redirect("chat:entrance")

        #ChatUserを削除する
        chat_user.delete()

        response    = redirect("chat:entrance")
        response.delete_cookie("id")

        return response

index_exit  = IndexExitView.as_view()



class ChatRoomExitView(View):
    def post(self, request, *args, **kwargs):

        if "id" not in request.COOKIES:
            return redirect("chat:entrance")

        #Cookieに記録されているChatUserのidを取得
        chat_user_id = urllib.parse.unquote(request.COOKIES["id"])
        chat_user    = ChatUser.objects.filter(id=chat_user_id).first()

        if not chat_user:
            return redirect("chat:entrance")



        #roomを削除する
        chat_user.room  = None
        chat_user.save()

        return redirect("chat:index")

chat_room_exit  = ChatRoomExitView.as_view()




class RefreshView(View):
    def get(self, request, pk, *args, **kwargs):
        data = {"error": True}

        context = {}


        # 送信されたIDを抜き取り、最新データのチェックで扱えるようにする。
        form = ChatFirstForm(request.GET)

        first = None
        if form.is_valid():
            cleaned = form.clean()
            first = cleaned["first"]
        else:
            print(form.errors)
        

        for i in range(30):

            time.sleep(1)
            chat = Chat.objects.order_by("-dt").first()

            #以降はtopicが存在することを前提とするため、存在しない場合は次のループへ(エラー回避)
            if not chat:
                continue 

            #トピックが存在し、なおかつ送られたファーストデータは空。
            if not first:
                break

            #トピックのidと送られたファーストデータが異なる
            if chat.id != first:
                break

        #order_by("-dt")で新しい物が上、order_by("dt")で新しい物が下 
        context["chats"] = Chat.objects.filter(room=pk).order_by("dt")

        data["error"] = False
        data["content"] = render_to_string("chat/content.html", context, request)

        return JsonResponse(data)

refresh = RefreshView.as_view()
