from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView

from chat.models import Room
from chatting.models import Message
from chatting.serializers import MessageListSerializer


def index(request):
    return render(request, 'ws_index.html')  # render - 전달 받은 이름의 템플릿 HttpResponse 형태로 응답


def room(request, room_id, user_id):
    return render(request, 'ws_room.html', {
        'room_id': room_id,
        'user_id': user_id
    })


class MessageGetAPIView(ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer

    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        messages = Message.objects.filter(room=room)

        for message in messages:
            avatar = message.chat_user.user.avatar
            message = message.__dict__
            message['user_avatar'] = f"https://deliveryneighborsbucket.s3.ap-northeast-2.amazonaws.com/{avatar}"

        serializer = MessageListSerializer(instance=messages, many=True)

        return JsonResponse({"status": status.HTTP_200_OK, "rooms": serializer.data})
