from dataclasses import field
import re

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from chat.models import Chat, Message


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name'
        )
        model = User


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254
    )
    username = serializers.CharField(
        max_length=150
    )
    password = serializers.CharField(
        max_length=150
    )
    first_name = serializers.CharField(
        max_length=150
    )
    last_name = serializers.CharField(
        max_length=150
    )

    class Meta:
        fields = (
            'email', 'username', 'password', 
            'first_name', 'last_name'
        )

    def validate_username(self, data):
        if re.match(r'^[\\w.@+-]+\\z', data):
            raise serializers.ValidationError(
                'Недопустимые символы в username.'
            )
        if data == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=255
    )
    # email = serializers.EmailField(
    #     max_length=255
    # )
    password = serializers.CharField(
        max_length=150,
        trim_whitespace=False,
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    class Meta:
        fields = ('token', 'username', 'password')


class ChatSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255,
        trim_whitespace=False,
    )

    class Meta:
        model = Chat
        fields = '__all__'


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    author = serializers.CharField()
    chat = ChatSerializer()
    created_at = serializers.DateTimeField(read_only=True, format="%m-%d-%Y %H:%M:%S")

    class Meta:
        model = Message
        fields = '__all__'
