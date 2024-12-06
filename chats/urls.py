from django.urls import path
from .views import ChatView, ChatInfo, AddUserToGroupView, CreateChatRoom


urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
    path('<uuid:room_id>/add_user', AddUserToGroupView.as_view(), name='add_user'),
    path('<uuid:room_id>', ChatInfo.as_view(), name='chat-detail'),
    path('create', CreateChatRoom.as_view(), name='create-chatroom')
]
