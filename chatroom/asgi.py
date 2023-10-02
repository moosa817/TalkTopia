"""
ASGI config for chatroom project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatroom.settings')

django_asgi_app = get_asgi_application()
app = django_asgi_app

import base.routing

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            base.routing.websocket_urlpatterns
        )
    )
})

