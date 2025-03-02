# from rest_framework import viewsets, filters
# from django_filters.rest_framework import DjangoFilterBackend
# from events.models import Event
# from accounts.models import CustomUser
# from .serializers import EventSerializer, CustomUserSerializer

# # ViewSet for Event model
# class EventViewSet(viewsets.ModelViewSet):
#     queryset = Event.objects.all().order_by("date")
#     serializer_class = EventSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ["date", "location", "category"]  #  Filter by these fields
#     search_fields = ["name", "description"]  #  Enable search on event names
#     ordering_fields = ["date", "name"]  #  Allow ordering by name and date

# # ViewSet for CustomUser model
# class CustomUserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from events.models import Event
from accounts.models import CustomUser
from .serializers import EventSerializer, CustomUserSerializer

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

#Section: Organizations API
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
