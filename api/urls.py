# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import EventViewSet, CustomUserViewSet

# router = DefaultRouter()
# router.register(r'events', EventViewSet)
# router.register(r'users', CustomUserViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, OrganisationViewSet, VolunteerViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")
router.register(r"organisations", OrganisationViewSet, basename="organisations")
router.register(r"volunteers", VolunteerViewSet, basename="volunteers")

urlpatterns = [
    path("", include(router.urls)),
]
