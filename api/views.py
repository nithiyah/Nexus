from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from events.models import Event
from accounts.models import CustomUser
from .serializers import EventSerializer, CustomUserSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, permissions
from announcements.models import Announcement, AnnouncementComment, AnnouncementLike
from chat.models import ChatRoom, Message
from .serializers import (
    AnnouncementSerializer, AnnouncementCommentSerializer, AnnouncementLikeSerializer,
    ChatRoomSerializer, MessageSerializer
)



class IsOrganisation(BasePermission):
    """Custom permission to allow only organizations to create/delete events."""

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True  # Allow read-only access for everyone
        return request.user.is_authenticated and request.user.user_type == "organisation"
    

#Section: Events API
@extend_schema_view(
    list=extend_schema(summary="Retrieve all events", tags=["Events"]),
    retrieve=extend_schema(summary="Retrieve a specific event", tags=["Events"]),
    create=extend_schema(summary="Create a new event", tags=["Events"]),
    update=extend_schema(summary="Update an event", tags=["Events"]),
    partial_update=extend_schema(summary="Partially update an event", tags=["Events"]),
    destroy=extend_schema(summary="Delete an event", tags=["Events"]),


)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("date")
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["date", "location", "category"]
    search_fields = ["name", "description"]
    ordering_fields = ["date", "name"]

    def get_permissions(self):
        """Allow public access to list & retrieve, but restrict create/update/delete."""
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsOrganisation()]

    def update(self, request, *args, **kwargs):
        """Ensure only the organisation that created the event can update it"""
        event = self.get_object()
        if request.user != event.organisation:
            return Response({"error": "You do not have permission to update this event."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Ensure only the organisation that created the event can delete it"""
        event = self.get_object()
        if request.user != event.organisation:
            return Response({"error": "You do not have permission to delete this event."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Ensure only organizations can create events"""
        if request.user.user_type != "organisation":
            return Response({"error": "Only organisations can create events."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)


#Section: Organisations API
@extend_schema_view(
    list=extend_schema(summary="Retrieve all organisations", tags=["Organisations"]),
    retrieve=extend_schema(summary="Retrieve a specific organisation", tags=["Organisations"]),
    create=extend_schema(summary="Create a new organisation", tags=["Organisations"]),
    update=extend_schema(summary="Update an organisation", tags=["Organisations"]),
    partial_update=extend_schema(summary="Partially update an organisation", tags=["Organisations"]),
    destroy=extend_schema(summary="Delete an organisation", tags=["Organisations"]),
)
class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(user_type="organisation")
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """Allow public access to list organisations, but restrict create/update/delete"""
        if self.action == "list":
            return [AllowAny()]  # Allow anyone to list organisations
        if self.action == "create":
            return [IsAuthenticated(), IsAdminUser()]  # Only admins can create organisations
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Ensure only admins can create organisations"""
        if not request.user.is_staff:
            return Response({"error": "Only admins can create organisations."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

# Section: Volunteers API
@extend_schema_view(
    list=extend_schema(summary="Retrieve all volunteers", tags=["Volunteers"]),
    retrieve=extend_schema(summary="Retrieve a specific volunteer", tags=["Volunteers"]),
    create=extend_schema(summary="Create a new volunteer", tags=["Volunteers"]),
    update=extend_schema(summary="Update a volunteer", tags=["Volunteers"]),
    partial_update=extend_schema(summary="Partially update a volunteer", tags=["Volunteers"]),
    destroy=extend_schema(summary="Delete a volunteer", tags=["Volunteers"]),
)
class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(user_type="volunteer")
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        # Allow public access to list volunteers, but restrict create/update/delete
        if self.action == "list":
            return [AllowAny()]  # Allow anyone to list volunteers
        if self.action == "create":
            return [IsAuthenticated(), IsAdminUser()]  # Only admins can create volunteers
        return [IsAuthenticated()]


    def destroy(self, request, *args, **kwargs):
        # Prevent volunteers from deleting themselves
        user = self.get_object()
        if request.user == user:
            return Response({"error": "You cannot delete your own account."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    


# ANNOUNCEMENTS API GROUP
@extend_schema_view(
    list=extend_schema(summary="Retrieve all announcements", tags=["Announcements"]),
    retrieve=extend_schema(summary="Retrieve a specific announcement", tags=["Announcements"]),
    create=extend_schema(summary="Create an announcement", tags=["Announcements"]),
    update=extend_schema(summary="Update an announcement", tags=["Announcements"]),
    partial_update=extend_schema(summary="Partially update an announcement", tags=["Announcements"]),
    destroy=extend_schema(summary="Delete an announcement", tags=["Announcements"]),
)
class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by("-created_at")
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    list=extend_schema(summary="Retrieve all announcement comments", tags=["Announcements"]),
    create=extend_schema(summary="Add a comment to an announcement", tags=["Announcements"]),
)
class AnnouncementCommentViewSet(viewsets.ModelViewSet):
    queryset = AnnouncementComment.objects.all()
    serializer_class = AnnouncementCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    list=extend_schema(summary="Retrieve all announcement likes", tags=["Announcements"]),
    create=extend_schema(summary="Like an announcement", tags=["Announcements"]),
)
class AnnouncementLikeViewSet(viewsets.ModelViewSet):
    queryset = AnnouncementLike.objects.all()
    serializer_class = AnnouncementLikeSerializer
    permission_classes = [permissions.IsAuthenticated]


#CHAT API GROUP
@extend_schema_view(
    list=extend_schema(summary="Retrieve all chat rooms", tags=["Chat"]),
    retrieve=extend_schema(summary="Retrieve a specific chat room", tags=["Chat"]),
)
class ChatRoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    list=extend_schema(summary="Retrieve all messages in a chat room", tags=["Chat"]),
    create=extend_schema(summary="Send a message in a chat room", tags=["Chat"]),
)
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("timestamp")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
