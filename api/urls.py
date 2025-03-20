from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, OrganisationViewSet, VolunteerViewSet
from .views import (
    EventViewSet, OrganisationViewSet, VolunteerViewSet,
    AnnouncementViewSet, AnnouncementCommentViewSet, AnnouncementLikeViewSet,
    ChatRoomViewSet, MessageViewSet
)

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")
router.register(r"organisations", OrganisationViewSet, basename="organisations")
router.register(r"volunteers", VolunteerViewSet, basename="volunteers")


# Announcements API
router.register(r"announcements", AnnouncementViewSet, basename="announcements")
router.register(r"announcements/comments", AnnouncementCommentViewSet, basename="announcement-comments")
router.register(r"announcements/likes", AnnouncementLikeViewSet, basename="announcement-likes")

# Chat API
router.register(r"chatrooms", ChatRoomViewSet, basename="chatrooms")
router.register(r"chatrooms/messages", MessageViewSet, basename="chat-messages")

urlpatterns = [
    path("", include(router.urls)),
]
