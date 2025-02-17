
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import FeedbackFormForm
from django.utils.timezone import now
from .models import Event, VolunteerEvent, FeedbackForm, FeedbackResponse
from .forms import FeedbackResponseForm  # Import the form



@login_required
def organisation_dashboard(request):
    if request.user.user_type == 'organisation': 
        events = Event.objects.filter(organisation=request.user)
        return render(request, 'events/organisation_dashboard.html', {'events': events})
    return redirect('home')

@login_required
def volunteer_dashboard(request):
    if request.user.user_type == 'volunteer':
        events = Event.objects.all()

        # Get events the volunteer has registered for
        registered_event_ids = set(
            VolunteerEvent.objects.filter(volunteer=request.user, status='registered')
            .values_list('event_id', flat=True)
        )

        # Filtering logic
        selected_categories = request.GET.getlist('category')
        location = request.GET.get('location', '').strip()
        date = request.GET.get('date', '').strip()

        if selected_categories:
            events = events.filter(category__in=selected_categories)
        if location:
            events = events.filter(location__icontains=location)
        if date:
            events = events.filter(date=date)

        # Ensure unique categories for filtering dropdown
        category_choices = dict(Event.CATEGORY_CHOICES)
        categories = list(category_choices.keys())

        # # Attach `volunteer_count` to each event
        # for event in events:
        #     event.volunteer_count = VolunteerEvent.objects.filter(event=event, status='registered').count()
        # Attach `volunteer_count` and `open_spots` to each event
        for event in events:
            event.volunteer_count = VolunteerEvent.objects.filter(event=event, status='registered').count()
            event.open_spots = max(event.volunteers_needed - event.volunteer_count, 0)

        return render(request, 'events/volunteer_dashboard.html', {
            'events': events,
            'categories': categories,
            'category_labels': category_choices,
            'selected_categories': selected_categories,
            'registered_event_ids': registered_event_ids, 
        })
    return redirect('home')


@login_required
def volunteer_events(request):
    # Get all events the volunteer has participated in
    registered_events = VolunteerEvent.objects.filter(volunteer=request.user)
    
    feedback_forms = {
        event.event.id: event.event.feedback_form if hasattr(event.event, "feedback_form") else None
        for event in registered_events
    }


    return render(request, 'events/volunteer_events.html', {
        'registered_events': registered_events,
        'feedback_forms': feedback_forms,  # Pass the mapping to the template
    })


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


@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Count currently registered volunteers
    registered_count = VolunteerEvent.objects.filter(event=event, status='registered').count()

    # Check if the user is already registered or waitlisted
    existing_registration = VolunteerEvent.objects.filter(event=event, volunteer=request.user).first()
    
    if existing_registration:
        if existing_registration.status == 'waiting_list':
            messages.info(request, 'You are already on the waiting list for this event.')
        else:
            messages.info(request, 'You have already registered for this event.')
    else:
        if registered_count < event.volunteers_needed:
            # Register the volunteer as "registered"
            VolunteerEvent.objects.create(event=event, volunteer=request.user, status='registered')
            messages.success(request, 'You have successfully registered for the event.')
        else:
            # Event is full, add to waiting list
            new_entry = VolunteerEvent.objects.create(event=event, volunteer=request.user, status='waiting_list')
            new_entry.save()
            messages.info(request, 'The event is full. You have been added to the waiting list.')

    return redirect('events:volunteer_dashboard')


@login_required
def cancel_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Find the volunteer's registration (registered or waitlisted)
    registration = VolunteerEvent.objects.filter(event=event, volunteer=request.user).first()
    
    if registration:
        registration.delete()
        messages.success(request, 'You have successfully canceled your registration.')

        # Move the first waitlisted volunteer to "registered" if a spot opens
        waitlisted_volunteers = VolunteerEvent.objects.filter(event=event, status='waiting_list').order_by('id')
        if waitlisted_volunteers.exists():
            next_volunteer = waitlisted_volunteers.first()
            next_volunteer.status = 'registered'
            next_volunteer.save()
            messages.info(request, f"{next_volunteer.volunteer.username} has been moved from the waitlist to registered.")

    return redirect('events:volunteer_events')

@login_required
def volunteer_events(request):
    # Get events where the volunteer is registered or on the waiting list
    registered_events = VolunteerEvent.objects.filter(volunteer=request.user, status='registered')
    waitlisted_events = VolunteerEvent.objects.filter(volunteer=request.user, status='waiting_list')
    # Fetch feedback forms linked to the events this volunteer attended
    # feedback_forms = {
    #     event.event.id: FeedbackResponse.objects.filter(
    #         feedback_form__event=event.event, volunteer=request.user
    #     ).first()
    #     for event in registered_events
    # }
    feedback_forms = {
        event.event.id: event.event.feedback_form if hasattr(event.event, "feedback_form") else None
        for event in registered_events
    }


    return render(request, 'events/volunteer_events.html', {
        'registered_events': registered_events,
        'waitlisted_events': waitlisted_events,
        'feedback_forms': feedback_forms,  # Pass feedback data to the template

    })

@login_required
def organisation_events(request):
    events = Event.objects.filter(organisation=request.user)

    # Preprocess event volunteers
    for event in events:
        event.volunteers = VolunteerEvent.objects.filter(event=event)

    return render(request, 'events/organisation_events.html', {
        'events': events,
        'today': now()  # Pass the current date to the template for the feedback form

    })


#Under organisation events page
@login_required
def remove_volunteer(request, registration_id):
    """Allows an organisation to remove a volunteer from an event."""
    registration = get_object_or_404(VolunteerEvent, id=registration_id)

    # Ensure only the event creator can remove volunteers
    if registration.event.organisation == request.user:
        registration.delete()
        messages.success(request, f"{registration.volunteer.full_name} has been removed from the event.")
    else:
        messages.error(request, "You are not authorized to remove volunteers from this event.")

    return redirect('events:organisation_events')


# organisation to create and edit feedback form
@login_required
def create_feedback_form(request, event_id):
    event = get_object_or_404(Event, id=event_id, organisation=request.user)

    feedback_form, created = FeedbackForm.objects.get_or_create(event=event, created_by=request.user)
    
    if request.method == "POST":
        form = FeedbackFormForm(request.POST, instance=feedback_form)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback form updated successfully!")
            return redirect("events:organisation_events")
    else:
        form = FeedbackFormForm(instance=feedback_form)

    return render(request, "events/create_feedback_form.html", {"form": form, "event": event})

# organisation to publish feedback form view
@login_required
def publish_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id, organisation=request.user)

    # Fetch the feedback form or return 404 if it doesn't exist
    feedback_form = get_object_or_404(FeedbackForm, event=event)

    feedback_form.published = True  # Publish the feedback form
    feedback_form.save()
    messages.success(request, "Feedback form has been published.")

    return redirect("events:organisation_events")

# @login_required
# def publish_feedback(request, event_id):
#     event = get_object_or_404(Event, id=event_id, organisation=request.user)

#     feedback_form = event.feedback_form  # Fetch the related FeedbackForm
#     if feedback_form:
#         feedback_form.published = True
#         feedback_form.save()
#         messages.success(request, "Feedback form has been published.")
#     else:
#         messages.error(request, "No feedback form found for this event.")

#     return redirect("events:organisation_events")

# @login_required
# def publish_feedback_form(request, event_id):
#     feedback_form = get_object_or_404(FeedbackForm, event_id=event_id, created_by=request.user)
#     feedback_form.published = True
#     feedback_form.save()
#     messages.success(request, "Feedback form published to volunteers!")
#     return redirect("events:organisation_events")


# volunteers to complete the feedback form
@login_required
def complete_feedback(request, event_id):
    feedback_form = get_object_or_404(FeedbackForm, event_id=event_id, published=True)
    
    if request.method == "POST":
        form = FeedbackResponseForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.feedback_form = feedback_form
            feedback.volunteer = request.user
            feedback.save()
            messages.success(request, "Feedback submitted successfully!")
            return redirect("events:volunteer_events")
    else:
        form = FeedbackResponse()

    return render(request, "events/complete_feedback.html", {"form": form, "feedback_form": feedback_form})

# volunteers to submit feedback form
@login_required
def submit_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.event = event
            feedback.volunteer = request.user
            feedback.save()
            messages.success(request, "Feedback submitted successfully!")
            return redirect('events:volunteer_events')  # Redirect to Volunteer My Events page
    else:
        form = FeedbackForm()

    return render(request, 'events/submit_feedback.html', {'form': form, 'event': event})

# organisations to view submitted volunteer feedback forms
@login_required
def view_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    #Fitlers the responses based on the correct event
    feedback_entries = FeedbackResponse.objects.filter(feedback_form__event=event)  

    return render(request, 'events/view_feedback.html', {
        'event': event,
        'feedback_entries': feedback_entries,
    })


@login_required
def complete_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    feedback_form = event.feedback_form  # Get the feedback form

    if not feedback_form or not feedback_form.published:
        messages.error(request, "Feedback form is not available for this event.")
        return redirect("events:volunteer_events")

    if request.method == "POST":
        form = FeedbackResponseForm(request.POST)
        if form.is_valid():
            feedback_response = form.save(commit=False)
            feedback_response.feedback_form = feedback_form
            feedback_response.volunteer = request.user
            feedback_response.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect("events:volunteer_events")
    else:
        form = FeedbackResponseForm()

    return render(request, "events/complete_feedback_form.html", {
        "form": form,
        "event": event,
        "feedback_form": feedback_form,
    })