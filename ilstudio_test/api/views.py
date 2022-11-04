from functools import partial
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from chat.models import Chat, Message
from .serializers import (
    LoginSerializer, RegistrationSerializer, ChatSerializer,
    MessageSerializer, UserSerializer
)


User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    activation_code = ''
    # try:
    #     user, created = User.objects.get_or_create(
    #         username=request.data['username'],
    #         email=request.data['email'],
    #         first_name=request.data['first_name'],
    #         last_name=request.data['last_name'],
    #     )
    #     if not created:
    #         raise ValidationError(
    #         'Пользователь с такими данными уже существует.'
    #         )
    #     activation_code = account_activation_token.make_token(user)
    #     user.code = activation_code
    #     user.set_password(request.data['password'])
    #     user.save()
    # except IntegrityError:
    #     raise ValidationError(
    #         'Некорректные username или email.'
    #     )
    # message = f'http://localhost:3000/activate/?activation_code={activation_code}'
    # with open('1.txt', 'w') as f:
    #     f.write(message)

    # send_mail(
    #     'Код подтверждения', message,
    #     settings.EMAIL_HOST_USER,
    #     [request.data.get('email')],
    #     fail_silently=False
    # )
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_chats(request):
    queryset = Chat.objects.all()
    serializer = ChatSerializer(
        queryset,
        partial=True,
        many=True
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_chat_history(request):
    chat, created = Chat.objects.get_or_create(
        title=request.data.get('chat_title')
    ) 
    queryset = Message.objects.filter(
        chat=chat
    ).order_by('-created_at')[::-1]
    serializer = MessageSerializer(
        queryset,
        partial=True,
        many=True
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_or_create_chat(request):
    print(request.data)
    serializer = ChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    chat, created = Chat.objects.get_or_create(
        title = serializer.validated_data['title'],
    )
    if request.user not in chat.users.all():
        chat.users.add(request.user)
        chat.save()
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_message(request):
    if request.user.is_authenticated:
        chat = get_object_or_404(
            Chat, title=request.data['chat']
        )
        message = Message.objects.create(
            chat=chat, author=request.user,
            text=request.data['text']
        )
    serializer = MessageSerializer(
            message,
            partial=True,
            many=False
        )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response(status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    return Response(
        {'token': token.key},
        status=status.HTTP_200_OK
    )
