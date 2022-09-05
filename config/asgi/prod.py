import os
import chatting

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application

from chatting import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

django_application = get_default_application()

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
            URLRouter(
                chatting.routing.websocket_urlpatterns
            )
        )
    }
)

