# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import ChatRoom, Message
# from django.utils.timezone import now

# from events.models import Event, VolunteerEvent
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from events.models import Event, VolunteerEvent
# from chat.models import ChatRoom, Message

# @login_required
# def chat_home(request):
#     """Shows all chat rooms the logged-in user has access to, including participant count."""
    
#     if request.user.user_type == 'volunteer':
#         registered_events = VolunteerEvent.objects.filter(volunteer=request.user).values_list('event_id', flat=True)
#         chat_rooms = ChatRoom.objects.filter(event__id__in=registered_events)

#     elif request.user.user_type == 'organisation':
#         chat_rooms = ChatRoom.objects.filter(event__organisation=request.user)

#     else:
#         chat_rooms = ChatRoom.objects.none()

#     for room in chat_rooms:
#         room.participant_count = VolunteerEvent.objects.filter(event=room.event).count()

#     return render(request, "chat/chat_home.html", {"chat_rooms": chat_rooms})


# @login_required
# def chat_room(request, event_id):
#     """Allow only registered volunteers and event organizers to access the chat room."""
    
#     event = get_object_or_404(Event, id=event_id)
#     chatroom, created = ChatRoom.objects.get_or_create(event=event)

#     # Check if user is the organisation OR a registered volunteer
#     is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user).exists()
    
#     if request.user == event.organisation or is_registered:
#         messages = chatroom.messages.order_by("timestamp")  # Load previous messages
#         return render(request, "chat/chat_room.html", {
#             "event": event,
#             "chatroom": chatroom,
#             "messages": messages,
#         })
    
#     # 🚨 If unauthorized, show an error message and redirect
#     messages.error(request, "You are not authorized to join this chat room.")
#     return redirect("chat:chat_home") 


# @csrf_exempt
# @login_required
# def send_message(request, event_id):
#     """Allows registered volunteers and event organizers to send messages."""

#     chatroom = get_object_or_404(ChatRoom, event__id=event_id)
#     event = chatroom.event

#     # Check if user is the organiser or a registered volunteer
#     is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user).exists()

#     if request.user == event.organisation or is_registered:
#         if request.method == "POST":
#             try:
#                 data = json.loads(request.body)
#                 content = data.get("content", "").strip()

#                 if content:
#                     message = Message.objects.create(
#                         chatroom=chatroom,
#                         sender=request.user,
#                         content=content
#                     )

#                     return JsonResponse({
#                         "success": True,
#                         "sender": message.sender.username,
#                         "content": message.content,
#                         "timestamp": message.timestamp.strftime("%H:%M")
#                     })
#             except json.JSONDecodeError:
#                 return JsonResponse({"success": False, "error": "Invalid JSON data"})

#     return JsonResponse({"success": False, "error": "Unauthorized"})


# @login_required
# def get_online_users(request, event_id):
#     """Returns the number of online users in a chat room."""
    
#     room_group_name = f"chat_{event_id}"  # Ensure this matches ChatConsumer
#     channel_layer = get_channel_layer()

#     try:
#         online_users = async_to_sync(channel_layer.group_channels)(room_group_name)
#     except Exception:
#         online_users = []

#     return JsonResponse({"count": len(online_users)})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatRoom, Message
from django.utils.timezone import now
from events.models import Event, VolunteerEvent
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from chat.models import ChatRoom, Message

@login_required
def chat_home(request):
    """Shows all chat rooms the logged-in user has access to, including participant count."""
    
    if request.user.user_type == 'volunteer':
        # Get all events where the user is registered
        registered_events = VolunteerEvent.objects.filter(volunteer=request.user).values_list('event_id', flat=True)
        chat_rooms = ChatRoom.objects.filter(event__id__in=registered_events)

    elif request.user.user_type == 'organisation':
        # Show all chat rooms for events created by this organisation
        chat_rooms = ChatRoom.objects.filter(event__organisation=request.user)

    else:
        chat_rooms = ChatRoom.objects.none()  # Empty queryset for unknown user types

    # Attach participant count to each chat room
    for room in chat_rooms:
        room.participant_count = VolunteerEvent.objects.filter(event=room.event).count()

    return render(request, "chat/chat_home.html", {"chat_rooms": chat_rooms})


# Retrieves the correct chat room.
# Fetches all messages in order.


# Event organizers can access their event chat rooms.
# Registered volunteers can access chat rooms of events they registered for.
# Creates a chat room when the event is created (not just when accessed).
# Prevents unauthorized users from joining chats (volunteers must be registered).
# Ensures messages load correctly.

from django.http import HttpResponseForbidden

# @login_required
# def chat_room(request, event_id):
#     """Allow only registered volunteers and event organizers to access the chat room."""
    
#     event = get_object_or_404(Event, id=event_id)
#     chatroom, created = ChatRoom.objects.get_or_create(event=event)

#     # Check if user is the organiser OR a registered volunteer
#     is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user).exists()
    
#     if request.user == event.organisation or is_registered:
#         messages = chatroom.messages.order_by("timestamp")  # Load previous messages
#         return render(request, "chat/chat_room.html", {
#             "event": event,
#             "chatroom": chatroom,
#             "messages": messages,
#         })
    
#     return HttpResponseForbidden("You are not authorized to join this chat room.")

@login_required
def chat_room(request, event_id):
    """Allow only registered volunteers and event organizer to access the chat room."""
    
    event = get_object_or_404(Event, id=event_id)
    chatroom, created = ChatRoom.objects.get_or_create(event=event)

    # Check if user is the organisation or a registered volunteer
    is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user).exists()
    
    if request.user == event.organisation or is_registered:
        messages = chatroom.messages.order_by("timestamp")  # Load previous messages
        return render(request, "chat/chat_room.html", {
            "event": event,
            "chatroom": chatroom,
            "messages": messages,
        })
    # else:
    #     return redirect("events:volunteer_events")  # Redirect if not authorized
    return HttpResponseForbidden("You are not authorized to join this chat room.")
    

# # send message view 
# @csrf_exempt
# def send_message(request, event_id):
#     """Only allow registered volunteers or event organisers to send messages."""

#     chatroom = get_object_or_404(ChatRoom, event__id=event_id)
#     event = chatroom.event

#     # Check if user is the organiser or a registered volunteer
#     is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user).exists()

#     if request.user == event.organisation or is_registered:
#         if request.method == "POST":
#             data = json.loads(request.body)
#             content = data.get("content", "").strip()

#             if content:
#                 message = Message.objects.create(
#                     chatroom=chatroom,
#                     sender=request.user,
#                     content=content
#                 )

#                 return JsonResponse({
#                     "success": True,
#                     "sender": message.sender.username,
#                     "content": message.content,
#                     "timestamp": message.timestamp.strftime("%H:%M")
#                 })

#     return JsonResponse({"success": False, "error": "Unauthorized"})

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# @csrf_exempt
# def send_message(request, event_id):
#     """Only allow registered volunteers or event organisers to send messages."""
#     # chatroom = get_object_or_404(ChatRoom, event__id=event_id)
#     chatroom = get_object_or_404(ChatRoom, event=event)

#     event = chatroom.event

#     is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user).exists()

#     if request.user == event.organisation or is_registered:
#         if request.method == "POST":
#             data = json.loads(request.body)
#             content = data.get("content", "").strip()

#             if content:
#                 message = Message.objects.create(
#                     chatroom=chatroom,
#                     sender=request.user,
#                     content=content
#                 )

#                 # ✅ Broadcast message to WebSocket group
#                 channel_layer = get_channel_layer()
#                 async_to_sync(channel_layer.group_send)(
#                     f"chat_{event_id}",
#                     {
#                         "type": "chat_message",
#                         "message": message.content,
#                         "sender": message.sender.username,
#                         "timestamp": message.timestamp.strftime("%H:%M")
#                     }
#                 )

#                 return JsonResponse({
#                     "success": True,
#                     "sender": message.sender.username,
#                     "content": message.content,
#                     "timestamp": message.timestamp.strftime("%H:%M")
#                 })

#     return JsonResponse({"success": False, "error": "Unauthorized"})
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# @csrf_exempt
# def send_message(request, event_id):
#     """Sends messages and updates WebSocket in real-time."""

#     chatroom = get_object_or_404(ChatRoom, event__id=event_id)
#     event = chatroom.event

#     is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user).exists()

#     if request.user == event.organisation or is_registered:
#         if request.method == "POST":
#             data = json.loads(request.body)
#             content = data.get("content", "").strip()

#             if content:
#                 message = Message.objects.create(
#                     chatroom=chatroom,
#                     sender=request.user,
#                     content=content
#                 )

#                 # Send WebSocket update to get real time updates
#                 channel_layer = get_channel_layer()
#                 async_to_sync(channel_layer.group_send)(
#                     f"chat_{event_id}",
#                     {
#                         "type": "chat_message",
#                         "message": message.content,
#                         "sender": message.sender.username,
#                         "timestamp": message.timestamp.strftime("%H:%M"),
#                     },
#                 )

#                 return JsonResponse({
#                     "success": True,
#                     "sender": message.sender.username,
#                     "content": message.content,
#                     "timestamp": message.timestamp.strftime("%H:%M"),
#                 })

#     return JsonResponse({"success": False, "error": "Unauthorized"})
from django.core.files.storage import default_storage

@csrf_exempt
def send_message(request, event_id):
    """Handles text and file messages."""
    chatroom = get_object_or_404(ChatRoom, event__id=event_id)
    event = chatroom.event

    is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user).exists()

    if request.user == event.organisation or is_registered:
        if request.method == "POST":
            content = request.POST.get("content", "").strip()
            file = request.FILES.get("file")

            message = Message.objects.create(
                chatroom=chatroom,
                sender=request.user,
                content=content if content else None,  # Handle text messages
                file=file if file else None,  # Handle file uploads
            )

            # Send WebSocket update for real-time updates
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{event_id}",
                {
                    "type": "chat_message",
                    "message": message.content if message.content else "",  # Include text message
                    "file_url": message.file.url if message.file else "",  # Include file URL
                    "sender": message.sender.username,
                    "timestamp": message.timestamp.strftime("%H:%M"),
                },
            )

            return JsonResponse({
                "success": True,
                "sender": message.sender.username,
                "content": message.content if message.content else "",
                "file_url": message.file.url if message.file else "",
                "timestamp": message.timestamp.strftime("%H:%M"),
            })

    return JsonResponse({"success": False, "error": "Unauthorized"})

from chat.models import ChatRoom

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organisation = request.user
            event.save()

            # Create a chat room when an event is created
            ChatRoom.objects.create(event=event)

            return redirect('events:organisation_dashboard')
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})


from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required

@login_required
def get_online_users(request, event_id):
    """Returns the number of online users in a chat room."""
    room_group_name = f"chat_{event_id}"
    channel_layer = get_channel_layer()

    # Get the list of connected WebSocket channels for the room
    try:
        online_users = async_to_sync(channel_layer.group_channels)(room_group_name)
    except Exception:
        online_users = []

    return JsonResponse({"count": len(online_users)})