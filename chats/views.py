import json
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from chats.models import ChatMessage, ChatRoom
from django.core import serializers
from django.http import HttpRequest, HttpResponse, JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


channel_layer = get_channel_layer()

# Create your views here.
class ChatInfo(DetailView):
    model = ChatRoom

    def get(self, request, *args, **kwargs):
        room_id = kwargs['room_id']
        room = get_object_or_404(ChatRoom, room_id=room_id)
        messages = ChatMessage.objects.filter(room=room)
        messages_data = serializers.serialize('json', messages, use_natural_foreign_keys=True)

        data = {
            'room_name': room.room_name,  
            'room_id': str(room.room_id),
            'room_desc': room.description,
            'room_creator': room.creator.username, 
            'room_date_created': room.date_created,
            'messages': messages_data
        }
        return JsonResponse(data)


class ChatView(ListView):
    model = ChatRoom
    template_name = 'userchats.html'
    context_object_name = 'chats'

    def get_queryset(self):
        user_chats = self.model.objects.all().filter(members=self.request.user)
        return user_chats

class AddUserToGroupView(View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        username = data.get('username')
        room_id = kwargs.get('room_id')

        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)

        try:
            # Retrieve chat room and user
            room = ChatRoom.objects.get(room_id=room_id)
            user = get_user_model().objects.get(username=username)

            # Check if request user is the creator of the room
            if room.creator != request.user:
                return JsonResponse({'error': 'You are not authorized to add members to this room'}, status=403)

            # Check if the user is already a member
            if user in room.members.all():
                return JsonResponse({'message': 'User is already a chat group member'}, status=409)

            # Add user to the chat room
            room.members.add(user)

            async_to_sync(channel_layer.group_send)(
                f'chat_{room.room_id}',
                {'type': 'add_user', 'message':f'{username} added to chatroom'}
            )


            # Return updated member list
            members = list(room.members.values('username'))
            return JsonResponse({'message': 'User added successfully', 'members': members}, status=200)

        except ChatRoom.DoesNotExist:
            return JsonResponse({'error': 'Chat room does not exist'}, status=404)
        except get_user_model().DoesNotExist:
            return JsonResponse({'error': 'Username not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)



class CreateChatRoom(View):

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        try:
            data = json.loads(request.body)
            room_name = data.get('room_name')
            room_desc = data.get('room_desc')

            # Validate required fields
            if not room_name or not room_desc:
                return JsonResponse({'error': 'Room name and description are required.'}, status=400)

            # Create the chat room
            chat_room = ChatRoom.objects.create(
                room_name=room_name,
                description=room_desc,
                creator=request.user
            )
            chat_room.members.add(request.user)

            return JsonResponse({
                'message': 'Chat room created successfully.',
                'room_id': chat_room.room_id  
            }, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)
