from rest_framework import serializers
from events.models import Event
from accounts.models import CustomUser
from announcements.models import Announcement, AnnouncementComment, AnnouncementLike


# Serializer for the CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type']
#  Serializer for Organization Users
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "user_type"]
    
#  Serializer for Volunteer Users
class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "user_type"]

#  Serializer for Events (with nested organization)
class EventSerializer(serializers.ModelSerializer):
    organisation = OrganizationSerializer(read_only=True)  
    #  Display full organization info
    organisation_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(user_type="organisation"), write_only=True
    )

    class Meta:
        model = Event
        fields = [
            "id", "organisation", "organisation_id", "name", "description", "date",
            "location", "volunteers_needed", "roles_responsibilities", "category"
        ]
        read_only_fields = ["id", "organisation"]

    def create(self, validated_data):
        organisation = validated_data.pop("organisation_id")
        event = Event.objects.create(organisation=organisation, **validated_data)
        return event

from rest_framework import serializers

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"

class AnnouncementCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementComment
        fields = "__all__"

class AnnouncementLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementLike
        fields = "__all__"
from rest_framework import serializers
from chat.models import ChatRoom, Message

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # Show sender's username instead of ID

    class Meta:
        model = Message
        fields = ["id", "chatroom", "sender", "content", "file", "timestamp"]
