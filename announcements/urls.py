from django.urls import path
from . import views

app_name = "announcements"

urlpatterns = [
    # path("", views.announcement_list, name="announcement_list"),
    # path("create/", views.create_announcement, name="create_announcement"),
    # path("<int:announcement_id>/", views.announcement_detail, name="announcement_detail"),
    # path("<int:announcement_id>/comment/", views.add_comment, name="add_comment"),
    # path("<int:announcement_id>/like/", views.like_announcement, name="like_announcement"),

    # path("all/", views.all_announcements, name="all_announcements"),
    # path("", views.all_announcements, name="announcement_list"),
    # path("volunteer/", views.volunteer_announcements, name="volunteer_announcements"),
    # path("create/", views.create_announcement, name="create_announcement"),
    # path("<int:announcement_id>/", views.announcement_detail, name="announcement_detail"),
    # path("<int:announcement_id>/comment/", views.add_comment, name="add_comment"),
    # path("<int:announcement_id>/like/", views.like_announcement, name="like_announcement"),


    path("", views.announcement_list, name="announcement_list"),  # the main route
    # path("all/", views.all_announcements, name="all_announcements"),
    # path("volunteer/", views.volunteer_announcements, name="volunteer_announcements"),
    path("create/", views.create_announcement, name="create_announcement"),
    path("<int:announcement_id>/", views.announcement_detail, name="announcement_detail"),
    path("<int:announcement_id>/comment/", views.add_comment, name="add_comment"),
    path("<int:announcement_id>/like/", views.like_announcement, name="like_announcement"),
]
