import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from events.models import Event, VolunteerEvent
from .models import ChatRoom, Message

@login_required
def chat_home(request):
    """Shows all chat rooms the logged-in user has access to, including participant count."""
    
    if request.user.user_type == 'volunteer':
        registered_events = VolunteerEvent.objects.filter(volunteer=request.user).values_list('event_id', flat=True)
        chat_rooms = ChatRoom.objects.filter(event__id__in=registered_events)

    elif request.user.user_type == 'organisation':
        chat_rooms = ChatRoom.objects.filter(event__organisation=request.user)

    else:
        chat_rooms = ChatRoom.objects.none()

    for room in chat_rooms:
        room.participant_count = VolunteerEvent.objects.filter(event=room.event).count()

    return render(request, "chat/chat_home.html", {"chat_rooms": chat_rooms})


@login_required
def chat_room(request, event_id):
    """Allow only registered volunteers and event organizers to access the chat room."""
    
    event = get_object_or_404(Event, id=event_id)
    chatroom, created = ChatRoom.objects.get_or_create(event=event)

    # Check if user is the organisation OR a registered volunteer
    is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user).exists()
    
    if request.user == event.organisation or is_registered:
        messages = chatroom.messages.order_by("timestamp")  # Load previous messages
        return render(request, "chat/chat_room.html", {
            "event": event,
            "chatroom": chatroom,
            "messages": messages,
        })
    
    # 🚨 If unauthorized, show an error message and redirect
    messages.error(request, "You are not authorized to join this chat room.")
    return redirect("chat:chat_home") 


@csrf_exempt
@login_required
def send_message(request, event_id):
    """Allows registered volunteers and event organizers to send messages."""

    chatroom = get_object_or_404(ChatRoom, event__id=event_id)
    event = chatroom.event

    # Check if user is the organiser or a registered volunteer
    is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user).exists()

    if request.user == event.organisation or is_registered:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                content = data.get("content", "").strip()

                if content:
                    message = Message.objects.create(
                        chatroom=chatroom,
                        sender=request.user,
                        content=content
                    )

                    return JsonResponse({
                        "success": True,
                        "sender": message.sender.username,
                        "content": message.content,
                        "timestamp": message.timestamp.strftime("%H:%M")
                    })
            except json.JSONDecodeError:
                return JsonResponse({"success": False, "error": "Invalid JSON data"})

    return JsonResponse({"success": False, "error": "Unauthorized"})


@login_required
def get_online_users(request, event_id):
    """Returns the number of online users in a chat room."""
    
    room_group_name = f"chat_{event_id}"  # Ensure this matches ChatConsumer
    channel_layer = get_channel_layer()

    try:
        online_users = async_to_sync(channel_layer.group_channels)(room_group_name)
    except Exception:
        online_users = []

    return JsonResponse({"count": len(online_users)})