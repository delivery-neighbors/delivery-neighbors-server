import os

import django
from django.core.asgi import get_asgi_application

import chatting

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application

from chatting import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
django.setup()

django_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": AuthMiddlewareStack(
            URLRouter(
                chatting.routing.websocket_urlpatterns
            )
        )
    }
)

