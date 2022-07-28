from django.shortcuts import render

from chat.models import ChatUser

print("views.py")


def index(request):
    return render(request, 'chat/index.html')  # render - 전달 받은 이름의 템플릿 HttpResponse 형태로 응답


def room(request, room_name, user_id):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user_id': user_id
    })
