
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

@login_required
def organisation_dashboard(request):
    if request.user.user_type == 'organisation':
        events = Event.objects.filter(organisation=request.user)
        return render(request, 'events/organisation_dashboard.html', {'events': events})
    return redirect('home')


# @login_required
# def volunteer_dashboard(request):
#     if request.user.user_type == 'volunteer':
#         # To display all the events
#         events = Event.objects.all()
#         return render(request, 'events/volunteer_dashboard.html', {'events': events})
#     return redirect('home')

# @login_required
# def volunteer_dashboard(request):
#     if request.user.user_type == 'volunteer':
#         # Retrieve all events
#         events = Event.objects.all()

#         # Filtering logic
#         category = request.GET.get('category')
#         location = request.GET.get('location')
#         date = request.GET.get('date')

#         if category:
#             events = events.filter(category=category)
#         if location:
#             events = events.filter(location__icontains=location)
#         if date:
#             events = events.filter(date=date)

#         return render(request, 'events/volunteer_dashboard.html', {'events': events})
#     return redirect('home')

@login_required
def volunteer_dashboard(request):
    if request.user.user_type == 'volunteer':
        # Retrieve all events
        events = Event.objects.all()

        # Get distinct categories for the dropdown
        categories = Event.objects.values_list('category', flat=True).distinct()

        # Filtering logic
        category = request.GET.get('category')
        location = request.GET.get('location')
        date = request.GET.get('date')

        if category:
            events = events.filter(category=category)
        if location:
            events = events.filter(location__icontains=location)
        if date:
            events = events.filter(date=date)

        return render(request, 'events/volunteer_dashboard.html', {
            'events': events,
            'categories': categories  # Pass categories to template
        })
    return redirect('home')


# Edit Event View
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organisation=request.user)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:organisation_dashboard')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {'form': form, 'event': event})

# Delete Event View
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organisation=request.user)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('events:organisation_dashboard')

    return render(request, 'events/delete_event.html', {'event': event})


# Create Event View
@login_required
def create_event(request):
    if request.user.user_type != 'organisation':
        return redirect('home')  # Only organizations can create events

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organisation = request.user
            event.save()
            return redirect('events:organisation_dashboard')
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})
