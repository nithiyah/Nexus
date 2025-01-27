from django.shortcuts import render, redirect
from .forms import EventForm
from django.contrib.auth.decorators import login_required

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
            return redirect('organisation_dashboard')
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {'form': form})
