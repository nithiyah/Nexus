
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import FeedbackFormForm
from django.utils.timezone import now, localtime
from .models import Event, VolunteerEvent, FeedbackForm, FeedbackResponse
from .forms import FeedbackResponseForm  
from chat.models import ChatRoom
from django.db.models import Sum
from .models import VolunteerParticipation 
import datetime


###################### EVENT VIEW ######################
# volunteer_dashboard
# organisation_dashboard
# complete_event
# volunteer_events
# edit_event
# delete_event
# create_event

# register_for_event
# cancel_registration
# volunteer_events
# organisation_events
# remove_volunteer
# create_feedback_form
# publish_feedback
# complete_feedback
# submit_feedback
# view_feedback
# complete_feedback
# feedback_hub
# volunteer_list
# feedback_event_poge

###################### EVENT VIEW ######################

@login_required
def volunteer_dashboard(request):
    if request.user.user_type == 'volunteer':
        events = Event.objects.all().distinct()

        # Registered eventid
        registered_event_ids = set(
            VolunteerEvent.objects.filter(volunteer=request.user, status='registered')
            .values_list('event_id', flat=True)
        )

        # Get the total hours volunteered
        total_hours = VolunteerParticipation.objects.filter(volunteer=request.user).aggregate(
            total_hours=Sum('hours_contributed')
        )['total_hours'] or 0

        # total events participated - volunteer
        total_events = VolunteerParticipation.objects.filter(volunteer=request.user).count()

        # The filtering logic
        selected_categories = request.GET.getlist('category')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if selected_categories:
            events = events.filter(category__in=selected_categories)
        
        if start_date:
            events = events.filter(date__gte=start_date)
        
        if end_date:
            events = events.filter(date__lte=end_date)

        # To make sure its distinct filter
        events = events.distinct()

        # To get unique categories for filtering dropdown
        category_choices = dict(Event.CATEGORY_CHOICES)
        categories = list(category_choices.keys())

        # Number of volunteer and open spots in each event
        for event in events:
            event.volunteer_count = VolunteerEvent.objects.filter(event=event, status='registered').count()
            event.open_spots = max(event.volunteers_needed - event.volunteer_count, 0)

        return render(request, 'events/volunteer_dashboard.html', {
            'events': events,
            'categories': categories,
            'category_labels': category_choices,
            'selected_categories': selected_categories,
            'registered_event_ids': registered_event_ids,
            'total_hours': round(total_hours, 2),
            'total_events': total_events,
        })
    return redirect('home')


# @login_required
# def organisation_dashboard(request):
#     if request.user.user_type == 'organisation': 
#         events = Event.objects.filter(organisation=request.user)
#         return render(request, 'events/organisation_dashboard.html', {'events': events})
#     return redirect('home')

@login_required
def organisation_dashboard(request):
    if request.user.user_type == 'organisation': 
        events = Event.objects.filter(organisation=request.user)
        
        # Get filter parameters from request
        status = request.GET.get('status')
        category = request.GET.get('category')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Apply filtering logic
        if status == 'ongoing':
            events = events.filter(date__gte=now())
        elif status == 'completed':
            events = events.filter(date__lt=now())

        if category:
            events = events.filter(category=category)

        if start_date:
            events = events.filter(date__gte=start_date)
        
        if end_date:
            events = events.filter(date__lte=end_date)

        # Get distinct categories for filtering
        category_choices = dict(Event.CATEGORY_CHOICES)

        return render(request, 'events/organisation_dashboard.html', {
            'events': events,
            'category_labels': category_choices,
            'current_time': now(),
        })
    return redirect('home')


# def complete_event( event_id):
#     event = get_object_or_404(Event, id=event_id)

#     # Ensure event duration is calculated correctly
#     duration_hours = event.get_duration_hours()
#     print(f"DEBUG: Calculated event duration: {duration_hours} hours for event {event.name}")


#     # Log hours for all volunteers who participated
#     participants = VolunteerParticipation.objects.filter(event=event)
#     if not participants.exists():
#         print(f"DEBUG: No volunteers found for event {event.name}")

#     for participant in participants:
#         participant.hours_contributed = duration_hours
#         participant.save()
#         print(f"DEBUG: Logged {duration_hours} hours for {participant.volunteer.username}")

#     print(f"DEBUG: Total volunteers updated: {participants.count()}")
    
#     return redirect('events:organisation_events')

@login_required
def complete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Calculate event duration
    duration_hours = event.get_duration_hours()
    print(f"DEBUG: Calculated event duration: {duration_hours} hours for event {event.name}")

    # Ensure all registered volunteers have their hours logged
    registered_volunteers = VolunteerEvent.objects.filter(event=event, status='Registered')

    for registration in registered_volunteers:
        vp, created = VolunteerParticipation.objects.get_or_create(
            volunteer=registration.volunteer,
            event=event
        )
        vp.hours_contributed = duration_hours
        vp.save()
        print(f"DEBUG: Updated {registration.volunteer.username} with {vp.hours_contributed} hours")

    print(f"DEBUG: Total volunteers updated: {registered_volunteers.count()}")

    messages.success(request, f"Event {event.name} marked as completed, and hours logged.")
    return redirect('events:organisation_events')

@login_required
def volunteer_events(request):
    # Get all the events that volunteer particpate in
    registered_events = VolunteerEvent.objects.filter(volunteer=request.user)
    
    feedback_forms = {
        event.event.id: event.event.feedback_form if hasattr(event.event, "feedback_form") else None
        for event in registered_events
    }


    return render(request, 'events/volunteer_events.html', {
        'registered_events': registered_events,
        # pass the mapping to the template
        'feedback_forms': feedback_forms,  
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
            
            return redirect('events:organisation_events')
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
        
        return redirect('events:organisation_events')

    return render(request, 'events/delete_event.html', {'event': event})


# Create Event View
@login_required
def create_event(request):
    if request.user.user_type != 'organisation':
        return redirect('home')  
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organisation = request.user
            event.save()

            # Create a chat room when an event is created
            ChatRoom.objects.create(event=event)
            
            return redirect('events:organisation_events')
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})


# @login_required
# def register_for_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)

#     # Count currently registered volunteers
#     registered_count = VolunteerEvent.objects.filter(event=event, status='registered').count()

#     # Check if the user is already registered or waitlisted
#     existing_registration = VolunteerEvent.objects.filter(event=event, volunteer=request.user).first()
    
#     if existing_registration:
#         if existing_registration.status == 'waiting_list':
#             messages.info(request, 'You are already on the waiting list for this event.')
#         else:
#             messages.info(request, 'You have already registered for this event.')
#     else:
#         if registered_count < event.volunteers_needed:
#             # Register the volunteer as "registered"
#             registration, created = VolunteerEvent.objects.get_or_create(event=event, volunteer=request.user, status='registered')

#             # Ensure the volunteer participation record is also created
#             # VolunteerParticipation.objects.get_or_create(volunteer=request.user, event=event)
           
#             # Create a VolunteerEvent record
#             registration, created = VolunteerEvent.objects.get_or_create(event=event, volunteer=request.user, status='registered')

#             # Ensure the volunteer participation record is also created
#             participation, created = VolunteerParticipation.objects.get_or_create(volunteer=request.user, event=event)

#             if created:
#                 print(f"DEBUG: Participation record created for {request.user.username} in event {event.name}")
#             else:
#                 print(f"DEBUG: Participation record already exists for {request.user.username} in event {event.name}")

#             messages.success(request, 'You have successfully registered for the event.')
#         else:
#             # Event is full, add to waiting list
#             new_entry = VolunteerEvent.objects.create(event=event, volunteer=request.user, status='waiting_list')
#             messages.info(request, 'The event is full. You have been added to the waiting list.')

#     return redirect('events:volunteer_dashboard')


@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Prevent volunteers from registering for past events
    if event.date < now():
        messages.error(request, "You cannot register for past events.")
        return redirect("events:volunteer_dashboard")

    # Count currently registered volunteers
    registered_count = VolunteerEvent.objects.filter(event=event, status="registered").count()

    # Check if the user is already registered or waitlisted
    existing_registration = VolunteerEvent.objects.filter(event=event, volunteer=request.user).first()

    if existing_registration:
        if existing_registration.status == "waiting_list":
            messages.info(request, "You are already on the waiting list for this event.")
        else:
            messages.info(request, "You have already registered for this event.")
    else:
        if registered_count < event.volunteers_needed:
            # Register the volunteer as "registered"
            registration, created = VolunteerEvent.objects.get_or_create(event=event, volunteer=request.user, status="registered")

            # Ensure the volunteer participation record is also created
            VolunteerParticipation.objects.get_or_create(volunteer=request.user, event=event)

            messages.success(request, "You have successfully registered for the event.")
        # else:
            # Event is full, add to waiting list
            # VolunteerEvent.objects.create(event=event, volunteer=request.user, status="waiting_list")
            # messages.info(request, "The event is full. You have been added to the waiting list.")

    return redirect("events:volunteer_dashboard")



# @login_required
# def cancel_registration(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
    
#     # Find the volunteer's registration (registered or waitlisted)
#     # registration = VolunteerEvent.objects.filter(event=event, volunteer=request.user).first()
#     registration = VolunteerEvent.objects.filter(event=event, volunteer=request.user).first()

#     # Remove the volunteer participation record as well
#     VolunteerParticipation.objects.filter(event=event, volunteer=request.user).delete()

#     if registration:
#         registration.delete()
#         messages.success(request, 'You have successfully canceled your registration.')

#         # Move the first waitlisted volunteer to "registered" if a spot opens
#         waitlisted_volunteers = VolunteerEvent.objects.filter(event=event, status='waiting_list').order_by('id')
#         if waitlisted_volunteers.exists():
#             next_volunteer = waitlisted_volunteers.first()
#             next_volunteer.status = 'registered'
#             next_volunteer.save()
#             messages.info(request, f"{next_volunteer.volunteer.username} has been moved from the waitlist to registered.")

#     return redirect('events:volunteer_events')
# @login_required
# def cancel_registration(request, event_id):
#     event = get_object_or_404(Event, id=event_id)

#     # Prevent volunteers from cancelling if the event is completed
#     if event.date < now():
#         messages.error(request, "You cannot cancel registration for a completed event.")
#         return redirect("events:volunteer_events")

#     # Find the volunteer's registration
#     registration = VolunteerEvent.objects.filter(event=event, volunteer=request.user).first()

#     if registration:
#         registration.delete()
#         messages.success(request, "You have successfully canceled your registration.")

#         # Move the first waitlisted volunteer to "registered" if a spot opens
#         waitlisted_volunteers = VolunteerEvent.objects.filter(event=event, status="waiting_list").order_by("id")
#         if waitlisted_volunteers.exists():
#             next_volunteer = waitlisted_volunteers.first()
#             next_volunteer.status = "registered"
#             next_volunteer.save()
#             messages.info(request, f"{next_volunteer.volunteer.username} has been moved from the waitlist to registered.")

#     return redirect("events:volunteer_events")
@login_required
def cancel_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Prevent volunteers from cancelling if the event is completed
    if event.date < now():
        messages.error(request, "You cannot cancel registration for a completed event.")
        return redirect("events:volunteer_events")

    # Find the volunteer's registration
    registration = VolunteerEvent.objects.filter(event=event, volunteer=request.user).first()

    if registration:
        registration.delete()
        messages.success(request, "You have successfully canceled your registration.")

        # Move the first waitlisted volunteer to "registered" if a spot opens
        # waitlisted_volunteers = VolunteerEvent.objects.filter(event=event, status="waiting_list").order_by("id")
        # if waitlisted_volunteers.exists():
        #     next_volunteer = waitlisted_volunteers.first()
        #     next_volunteer.status = "registered"
        #     next_volunteer.save()
        #     messages.info(request, f"{next_volunteer.volunteer.username} has been moved from the waitlist to registered.")

    return redirect("events:volunteer_events")


@login_required
def volunteer_events(request):
    # Get all events the volunteer has registered for
    registered_events = VolunteerEvent.objects.filter(volunteer=request.user)

    for registration in registered_events:
        # Check if event has a feedback form
        feedback_form = getattr(registration.event, "feedback_form", None)
        if feedback_form:
            feedback_exists = FeedbackResponse.objects.filter(
                feedback_form=feedback_form, 
                volunteer=request.user
            ).exists()
            registration.has_submitted_feedback = feedback_exists
        else:
            # feedback form doesnt exist
            registration.has_submitted_feedback = None  

    return render(request, 'events/volunteer_events.html', {
        'registered_events': registered_events,
    })



from django.utils.timezone import now, localtime, is_naive, make_aware


# Converts event.date to timezone-aware before passing it to the template.
# Ensures localtime() does not throw an error.

from django.utils.timezone import now, localtime, is_naive, make_aware

@login_required
def organisation_events(request):
    events = Event.objects.filter(organisation=request.user)
    
    # Convert all the event dates to timezone-aware before it is rendered
    for event in events:
        if is_naive(event.date):  
            # If it is naive, make it timezone-aware
            event.date = make_aware(event.date)

        event.volunteers = VolunteerEvent.objects.filter(event=event)

    # Ensure the current time is timezone-aware
    # now() will return a timezone-aware datetime
    current_time = now()  

    return render(request, 'events/organisation_events.html', {
        'events': events,
        'current_time': current_time,
    })




# remove_volunter: allows organisation to remove volunteer from event
@login_required
def remove_volunteer(request, registration_id):
    registration = get_object_or_404(VolunteerEvent, id=registration_id)

    # Ensure only the event creator can remove volunteers
    if registration.event.organisation == request.user:
        registration.delete()
        messages.success(request, f"{registration.volunteer.full_name} has been removed from the event.")
    else:
        messages.error(request, "You are not authorised to remove volunteers from this event.")

    # return redirect('events:organisation_events')
    return redirect("events:organisation_dashboard")


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

            return redirect("events:organisation_dashboard")
    else:
        form = FeedbackFormForm(instance=feedback_form)

    return render(request, "events/create_feedback_form.html", {"form": form, "event": event})

# organisation to publish feedback form view
@login_required
def publish_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id, organisation=request.user)

    # Fetch the feedback form or return 404 if it doesn't exist
    # feedback_form = get_object_or_404(FeedbackForm, event=event)
    feedback_form = FeedbackForm.objects.filter(event=event).first()



    if not feedback_form:
        messages.error(request, "No feedback form exists for this event.")
        return redirect("events:feedback_event_page", event_id=event.id)  # Redirect back to event page

    # To publish the feedback form
    feedback_form.published = True  
    feedback_form.save()
    messages.success(request, "Feedback form has been published.")

    return redirect("events:organisation_dashboard")


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
            return redirect('events:volunteer_events')  
    else:
        form = FeedbackForm()

    return render(request, 'events/submit_feedback.html', {'form': form, 'event': event})


import json
from django.http import JsonResponse

@login_required
def view_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    feedback_entries = FeedbackResponse.objects.filter(feedback_form__event=event)

    # To get the Average Ratings
    ratings = {
        "rating_1": 0, "rating_2": 0, "rating_3": 0, "rating_4": 0, "rating_5": 0
    }
    total_responses = feedback_entries.count()

    if total_responses > 0:
        for feedback in feedback_entries:
            ratings["rating_1"] += feedback.rating_1
            ratings["rating_2"] += feedback.rating_2
            ratings["rating_3"] += feedback.rating_3
            ratings["rating_4"] += feedback.rating_4
            ratings["rating_5"] += feedback.rating_5

        # Calculate averages of the ratings
        for key in ratings:
            ratings[key] = round(ratings[key] / total_responses, 2)

    return render(request, 'events/view_feedback.html', {
        'event': event,
        'feedback_entries': feedback_entries,

        # To convert avergae ratings to JSON safe format
        'average_ratings': json.dumps(list(ratings.values())), 
    })



@login_required
def complete_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # To get the feedback form
    feedback_form = event.feedback_form  

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



@login_required
def feedback_hub(request):
    """Render the Feedback Hub page where organizations manage feedback."""
    events = Event.objects.filter(organisation=request.user)  # Get all events for this organization
    return render(request, "events/feedback_hub.html", {"events": events})


@login_required
def volunteer_list(request, event_id):
    # volunteer_list: show all volunteers registered for specific event
    event = get_object_or_404(Event, id=event_id, organisation=request.user)
    # Get the list of volunteers for an event
    volunteers = VolunteerEvent.objects.filter(event=event)  

    return render(request, "events/volunteer_list.html", {
        "event": event,
        "volunteers": volunteers,
    })



@login_required
def feedback_event_page(request, event_id):
    # Render the Feedback Page for a specific event 
    event = get_object_or_404(Event, id=event_id, organisation=request.user)

    return render(request, "events/feedback_event.html", {"event": event})


@login_required
def event_detail(request, event_id):
    # View an event's details
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event_detail.html", {"event": event})
