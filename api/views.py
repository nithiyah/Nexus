from rest_framework import viewsets
from events.models import Event
from accounts.models import CustomUser
from .serializers import EventSerializer, CustomUserSerializer

# ViewSet for Event model
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# ViewSet for CustomUser model
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
