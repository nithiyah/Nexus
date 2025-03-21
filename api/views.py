from rest_framework import viewsets, permissions, mixins
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from accounts.models import CustomUser
from events.models import Event
from announcements.models import Announcement, AnnouncementComment, AnnouncementLike
from chat.models import ChatRoom, Message

from .serializers import *
from .permissions import IsOrganisation


@extend_schema_view(
    list=extend_schema(summary="List users (filter by type)", tags=["Users"]),
    retrieve=extend_schema(summary="Retrieve user by ID", tags=["Users"]),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user_type = self.request.query_params.get("type")
        return self.queryset.filter(user_type=user_type) if user_type else self.queryset


@extend_schema_view(
    list=extend_schema(summary="List events", tags=["Events"]),
    retrieve=extend_schema(summary="Retrieve event", tags=["Events"]),
    create=extend_schema(summary="Create event", tags=["Events"]),
    update=extend_schema(summary="Update event", tags=["Events"]),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="Delete event", tags=["Events"]),
)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["date", "location", "category"]
    search_fields = ["name", "description"]
    ordering_fields = ["date", "name"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOrganisation()]

    def perform_create(self, serializer):
        serializer.save(organisation=self.request.user)



@extend_schema_view(
    list=extend_schema(summary="List announcements", tags=["Announcements"]),
    retrieve=extend_schema(summary="Retrieve announcement", tags=["Announcements"]),
    create=extend_schema(summary="Create announcement", tags=["Announcements"]),
    update=extend_schema(summary="Update announcement", tags=["Announcements"]),
    destroy=extend_schema(summary="Delete announcement", tags=["Announcements"]),
    partial_update=extend_schema(exclude=True), 
)
class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsOrganisation()]
        return [permissions.AllowAny()]


@extend_schema_view(
    create=extend_schema(summary="Post comment", tags=["Announcements"]),
)
class AnnouncementCommentViewSet(viewsets.ModelViewSet):
    queryset = AnnouncementComment.objects.all()
    serializer_class = AnnouncementCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



@extend_schema_view(
    create=extend_schema(summary="Like announcement", tags=["Announcements"]),
)
class AnnouncementLikeViewSet(viewsets.ModelViewSet):
    queryset = AnnouncementLike.objects.all()
    serializer_class = AnnouncementLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
    
@extend_schema_view(
    list=extend_schema(summary="List chatrooms", tags=["Chat"]),
    retrieve=extend_schema(summary="Retrieve chatroom", tags=["Chat"]),
)
class ChatRoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    list=extend_schema(summary="List messages", tags=["Chat"]),
    retrieve=extend_schema(summary="Retrieve message", tags=["Chat"]),
    create=extend_schema(summary="Send message", tags=["Chat"]),
    destroy=extend_schema(summary="Delete message", tags=["Chat"]),
)
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("timestamp")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']  #  excludes PUT and PATCH

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
