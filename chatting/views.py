from django.shortcuts import render


def index(request):
    return render(request, 'ws_index.html')  # render - 전달 받은 이름의 템플릿 HttpResponse 형태로 응답


def room(request, room_id, chat_user_id):
    return render(request, 'ws_room.html', {
        'room_id': room_id,
        'chat_user_id': chat_user_id
    })
