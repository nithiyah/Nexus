from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatRoom, Message
from events.models import Event
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def chat_home(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'chat/chat_home.html', {'chat_rooms': chat_rooms})


def chat_room(request, event_id):
    """Render the chat room with message history."""
    event = get_object_or_404(Event, id=event_id)
    chatroom, created = ChatRoom.objects.get_or_create(event=event)
    messages = chatroom.messages.order_by("timestamp")  # Load old messages

    return render(request, "chat/chat_room.html", {
        "event": event,
        "chatroom": chatroom,
        "messages": messages,
    })



@login_required
def delete_chat_room(request, event_id):
    """Allow organisations to delete a chat room after the event is over."""
    event = get_object_or_404(Event, id=event_id, organisation=request.user)
    chatroom = event.chatroom
    if chatroom:
        chatroom.delete()
        messages.success(request, "Chat room deleted successfully.")
    return redirect("events:organisation_events")
