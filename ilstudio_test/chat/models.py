from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = models.CharField(
        max_length=255,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]*$',
            message='Имя пользователя содержит недопустимые символы',
            code='invalid_username'
        ),
        ]
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    password = models.CharField(
        max_length=255
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )


    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Chat(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    users = models.ManyToManyField(
        User,
        verbose_name='Пользователи',
        related_name='chats',
        blank=True
    )

class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    chat = models.ForeignKey(
        Chat,
        verbose_name='Чат',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        related_name='messages',
        null=True
    )
