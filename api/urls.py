from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
