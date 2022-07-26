import os
import chatting

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from chatting import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

django_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            # URLRouter url 패턴을 통해 어떤 consumer 라우팅할 지 정함
            URLRouter(
                chatting.routing.urlpatterns
            )
        )
    ),
})

