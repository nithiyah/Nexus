# import os
# import django

# # ✅ Explicitly load Django settings before importing anything else
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus.settings')
# django.setup()

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import chat.routing  # ✅ Import chat WebSocket routes

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(chat.routing.websocket_urlpatterns)
#     ),
# })



# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import chat.routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nexus.settings")

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(chat.routing.websocket_urlpatterns)  # Ensure this exists
#     ),
# })

# import os
# import django  #  Ensure Django initializes before loading ASGI application
# from django.core.asgi import get_asgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nexus.settings")
# django.setup()  # Manually initialize Django before anything else

# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import chat.routing 
#   # Now import chat.routing after Django is set up

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(chat.routing.websocket_urlpatterns)
#     ),
# })

import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nexus.settings")
django.setup()  # Ensure Django is initialized first

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)  # Correct WebSocket routing
    ),
})
