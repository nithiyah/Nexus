from rest_framework import serializers
from accounts.models import CustomUser
from events.models import Event
from announcements.models import Announcement, AnnouncementComment, AnnouncementLike
from chat.models import ChatRoom, Message


# === USER SERIALIZER ===
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type']


# === EVENT SERIALIZER ===
class EventSerializer(serializers.ModelSerializer):
    organisation = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "organisation", "name", "description", "date",
            "location", "volunteers_needed", "roles_responsibilities", "category"
        ]

# === ANNOUNCEMENT SERIALIZERS ===
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'organisation', 'title', 'content', 'created_at']


class AnnouncementCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AnnouncementComment
        fields = ['id', 'announcement', 'user', 'comment', 'created_at']

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class AnnouncementLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AnnouncementLike
        fields = '__all__'


# === CHAT SERIALIZERS ===
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'event']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'sender', 'content', 'file', 'timestamp']

    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)
