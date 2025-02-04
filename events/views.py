from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import Event  # Import the Event model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def create_event(request):
    if request.user.user_type != 'organisation':
        return redirect('home')  # Redirect non-organisations away

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organisation = request.user  # Assign logged-in organisation
            event.save()
            form.save_m2m()  # Save many-to-many relationship for categories
            messages.success(request, 'New event successfully created!')
            return redirect('organisation_dashboard')
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def organisation_dashboard(request):
    if request.user.user_type == "organisation":  # Ensure only organizations access this page
        events = Event.objects.filter(organisation=request.user)  # Get events for the logged-in organization
        return render(request, 'accounts/organisation_dashboard.html', {'events': events})
    else:
        return redirect('home')  # Redirect unauthorized users


# Edit Event View
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organisation=request.user)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('organisation_dashboard')
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
        return redirect('organisation_dashboard')

    return render(request, 'events/delete_event.html', {'event': event})


@login_required
def volunteer_dashboard(request):
    events = Event.objects.all()  # Volunteers can see all events
    return render(request, 'events/volunteer_dashboard.html', {'events': events})