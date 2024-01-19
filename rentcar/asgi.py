import os

from django.core.asgi import get_asgi_application

from django.urls import path
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.route import websocket_urlpatterns


django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": ((URLRouter(websocket_urlpatterns))),
    }
)
