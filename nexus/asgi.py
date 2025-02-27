"""
ASGI config for nexus project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # Ensure chat.routing is imported to ensure that WebSockets are included

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus.settings')
django.setup() # this is required in order to use get_asgi_application() and will prevent the apps arent loaded yet error

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # Ensure this is correctly referenced
        )
    ),
})


