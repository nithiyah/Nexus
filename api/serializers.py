from rest_framework import serializers
from events.models import Event
from accounts.models import CustomUser
from announcements.models import Announcement, AnnouncementComment, AnnouncementLike
from chat.models import Message

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
from announcements.models import Announcement, AnnouncementComment, AnnouncementLike
from accounts.models import CustomUser

# Announcements Serializer
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["id", "organisation", "title", "content", "created_at"]



# Announcement Comment Serializer
class AnnouncementCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AnnouncementComment
        fields = ["id", "announcement", "user", "comment", "created_at"]

    def create(self, validated_data):
        """Ensure request.user is linked to the comment."""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
            return AnnouncementComment.objects.create(**validated_data)
        raise serializers.ValidationError("User is required to post a comment.")




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
        
# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "chatroom", "sender", "content", "file", "timestamp"]

    def create(self, validated_data):
        """Ensure the sender is set from the request user."""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["sender"] = request.user
            return Message.objects.create(**validated_data)
        raise serializers.ValidationError("Sender is required to send a message.")
