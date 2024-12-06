from django.contrib import admin

from chats.models import ChatMessage, ChatRoom

# Register your models here.


admin.site.register(ChatRoom)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'room', 'sender', 'date_sent']
    list_filter = ['date_sent', 'room']
    search_fields = ['room']
    





