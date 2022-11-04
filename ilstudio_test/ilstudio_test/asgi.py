import os
from django.urls import re_path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from chat import consumers
import chat.middleware as middleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ilstudio_test.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            middleware.TokenAuthMiddleware(
                URLRouter([
                    re_path(r'ws/chat/(?P<chat_title>\w+)/$', consumers.ChatConsumer.as_asgi())
                ])
            )
        ),
    }
)
