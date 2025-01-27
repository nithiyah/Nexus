from rest_framework import serializers
from events.models import Event
from accounts.models import CustomUser

# Serializer for the CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type']

# Serializer for the Event model
class EventSerializer(serializers.ModelSerializer):
    organisation = CustomUserSerializer(read_only=True)  # Nested serialization for the organization
    organisation_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(user_type='organisation'), write_only=True
    )

    class Meta:
        model = Event
        fields = [
            'id', 'organisation', 'organisation_id', 'name', 'description', 'date',
            'location', 'volunteers_needed', 'roles_responsibilities', 'category'
        ]
        read_only_fields = ['id', 'organisation']  # Organisation name should not be editable via API

    def create(self, validated_data):
        # Extract organisation_id and replace it with actual organisation instance
        organisation = validated_data.pop('organisation_id')
        event = Event.objects.create(organisation=organisation, **validated_data)
        return event
