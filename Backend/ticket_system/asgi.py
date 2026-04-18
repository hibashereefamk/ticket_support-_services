import os
import django
from django.core.asgi import get_asgi_application

# 1. Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_system.settings')

# 2. Initialize Django (This MUST happen before importing routing)
django.setup()

# 3. Now import the rest
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from tickets.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(), # Handles normal web requests
    "websocket": AuthMiddlewareStack( # Handles WebSocket requests
        URLRouter(
            websocket_urlpatterns
        )
    ),
})