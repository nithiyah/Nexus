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

# Create your views here.


# def chat_home(request):
#     chat_rooms = ChatRoom.objects.all()
#     return render(request, 'chat/chat_home.html', {'chat_rooms': chat_rooms})

def chat_home(request):
    # Get events created by the logged-in organization
    if request.user.is_authenticated and request.user.user_type == "organisation":
        events = Event.objects.filter(organisation=request.user)
    else:
        events = []  # Empty list if user is not an organization

    return render(request, "chat/chat_home.html", {"events": events})

# Retrieves the correct chat room.
# Fetches all messages in order.



# Creates a chat room when the event is created (not just when accessed).
# Prevents unauthorized users from joining chats (volunteers must be registered).
# Ensures messages load correctly.
@login_required
def chat_room(request, event_id):
    """Render the chat room with message history."""
    event = get_object_or_404(Event, id=event_id)

    # Ensure a chat room is created for each event
    chatroom, created = ChatRoom.objects.get_or_create(event=event)

    # Check if the user is allowed in the chat
    if request.user.user_type == 'volunteer':
        is_registered = VolunteerEvent.objects.filter(event=event, volunteer=request.user, status='Registered').exists()
        if not is_registered:
            return render(request, "chat/chat_room.html", {"error": "You are not registered for this event."})

    # Load past messages
    messages = chatroom.messages.order_by("timestamp")

    return render(request, "chat/chat_room.html", {
        "event": event,
        "chatroom": chatroom,
        "messages": messages,
    })

# def chat_room(request, event_id):
#     """Render the chat room with message history."""
#     event = get_object_or_404(Event, id=event_id)
#     chatroom, created = ChatRoom.objects.get_or_create(event=event)
#     messages = chatroom.messages.order_by("timestamp")  # Load old messages

#     return render(request, "chat/chat_room.html", {
#         "event": event,
#         "chatroom": chatroom,
#         "messages": messages,
#     })



@login_required
def delete_chat_room(request, event_id):
    """Allow organisations to delete a chat room after the event is over."""
    event = get_object_or_404(Event, id=event_id, organisation=request.user)
    chatroom = event.chatroom
    if chatroom:
        chatroom.delete()
        messages.success(request, "Chat room deleted successfully.")
    return redirect("events:organisation_events")


# send message view 
@csrf_exempt
def send_message(request, event_id):
    if request.method == "POST":
        chatroom = get_object_or_404(ChatRoom, event__id=event_id)  # ✅ Ensure consistency in field name
        data = json.loads(request.body)
        content = data.get("content", "").strip()

        if content:
            message = Message.objects.create(
                chatroom=chatroom,  # ✅ Match the field name from the Message model
                sender=request.user,
                content=content
            )

            return JsonResponse({
                "success": True,
                "sender": message.sender.username,
                "content": message.content,
                "timestamp": message.timestamp.strftime("%H:%M")
            })

    return JsonResponse({"success": False})



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
