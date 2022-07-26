from django.shortcuts import render

print("views.py")


def index(request):
    return render(request, 'chat/index.html')  # render - 전달 받은 이름의 템플릿 HttpResponse 형태로 응답


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
