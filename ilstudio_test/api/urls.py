from django.urls import path


from .views import (
    get_all_chats, get_or_create_chat,
    get_chat_history, create_message, login
)


app_name = 'api'

urlpatterns = [
    path('', get_all_chats, name='get_all_chats'),
    path('get_chat/', get_or_create_chat, name='chat'),
    path('get_chat_history/', get_chat_history, name='chat_history'),
    path('create_message/', create_message, name='create_message'),
    path('login/', login, name='login'),
]
