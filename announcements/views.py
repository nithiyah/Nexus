from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Announcement, AnnouncementComment, AnnouncementLike
from .forms import AnnouncementForm, AnnouncementCommentForm
from events.models import Event
from django.contrib import messages

@login_required
def announcement_list(request):
    # Show all announcements relevant to the user
    if request.user.user_type == "organisation":
        announcements = Announcement.objects.filter(organisation=request.user)
    else:
        # Volunteers see announcements for events they registered for
        registered_events = request.user.registered_events.values_list('event_id', flat=True)
        announcements = Announcement.objects.filter(event__in=registered_events) | Announcement.objects.filter(event=None)

    return render(request, "announcements/announcement_list.html", {"announcements": announcements})

@login_required
def all_announcements(request):
    # View showing all organization announcements (Twitter-style)
    announcements = Announcement.objects.all().order_by('-created_at')  # Show latest first

    return render(request, "announcements/all_announcements.html", {"announcements": announcements})


@login_required
def volunteer_announcements(request):
    # View showing announcements related to events a volunteer has registered for
    if request.user.user_type == "organisation":
        messages.error(request, "Only volunteers can view event-related announcements.")
        return redirect("announcements:all_announcements")

    registered_events = request.user.registered_events.values_list('event_id', flat=True)
    announcements = Announcement.objects.filter(event__in=registered_events).order_by('-created_at')

    return render(request, "announcements/volunteer_announcements.html", {"announcements": announcements})
@login_required
def create_announcement(request):
    # Allow organisations to create announcements
    if request.user.user_type != "organisation":
        messages.error(request, "Only organisations can post announcements.")
        return redirect("announcements:announcement_list")

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.organisation = request.user
            announcement.save()
            messages.success(request, "Announcement posted successfully!")
            return redirect("announcements:announcement_list")
    else:
        form = AnnouncementForm()

    return render(request, "announcements/create_announcement.html", {"form": form})

@login_required
def announcement_detail(request, announcement_id):
    # View an announcement with comments
    announcement = get_object_or_404(Announcement, id=announcement_id)
    comments = announcement.comments.all()
    comment_form = AnnouncementCommentForm()

    return render(request, "announcements/announcement_detail.html", {
        "announcement": announcement,
        "comments": comments,
        "comment_form": comment_form
    })

@login_required
def add_comment(request, announcement_id):
    # Allow users to add comments to announcements
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    if request.method == "POST":
        form = AnnouncementCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.announcement = announcement
            comment.save()
            messages.success(request, "Comment added!")
    
    return redirect("announcements:announcement_detail", announcement_id=announcement_id)

# @login_required
# def like_announcement(request, announcement_id):
#     # Allow users to like/unlike an announcement
#     announcement = get_object_or_404(Announcement, id=announcement_id)
#     like, created = AnnouncementLike.objects.get_or_create(announcement=announcement, user=request.user)

# # NEED TO CHECK WHERE THIS GOES
#     if not created:
#         like.delete()
#         messages.info(request, "You unliked this announcement.")
#     else:
#         messages.success(request, "You liked this announcement!")

#     return redirect("announcements:announcement_list")
@login_required
def like_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    like, created = AnnouncementLike.objects.get_or_create(announcement=announcement, user=request.user)

    if not created:
        like.delete()
        messages.info(request, "You unliked this announcement.")
    else:
        messages.success(request, "You liked this announcement!")

    # Redirect back to where the user came from
    return redirect(request.META.get("HTTP_REFERER", "announcements:announcement_list"))
