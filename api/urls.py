from django.urls import path

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework.decorators import action
from .views import (
    UserViewSet, EventViewSet,
    AnnouncementViewSet, AnnouncementCommentViewSet, AnnouncementLikeViewSet,
    ChatRoomViewSet, MessageViewSet,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# keep your router for all other ViewSets
router = SimpleRouter()
router.register(r'users', UserViewSet, basename="users")
router.register(r'events', EventViewSet, basename="events")
router.register(r'announcements', AnnouncementViewSet, basename="announcements")
router.register(r'chatrooms', ChatRoomViewSet, basename="chatrooms")
router.register(r'messages', MessageViewSet, basename="messages")

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Explicit POST-only paths for comments and likes
    # path("api/announcements/comments/", AnnouncementCommentViewSet.as_view({"post": "create"}), name="announcement-comments-list"),
    # path("api/announcements/likes/", AnnouncementLikeViewSet.as_view({"post": "create"}), name="announcement-likes-list"),
    path("announcements/comments/", AnnouncementCommentViewSet.as_view({"post": "create"}), name="announcement-comments-list"),
    path("announcements/likes/", AnnouncementLikeViewSet.as_view({"post": "create"}), name="announcement-likes-list"),

    # all other router URLs
    path("", include(router.urls)),
]
