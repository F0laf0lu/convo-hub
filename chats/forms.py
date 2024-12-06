from django import forms

from chats.models import ChatRoom


class AddUserToGroupForm(forms.Form):
    username = forms.CharField()


class CreateChatRoom(forms.Form):
    
    class Meta:
        model = ChatRoom
        fields = "__all__"