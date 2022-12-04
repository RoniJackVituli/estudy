from django.urls import path
from YouTube import views

app_name = "YouTube"

urlpatterns = [
    path("", views.SearchVideoView.as_view(), name="youtube"),
    path("save/<int:video_index>", views.SaveVideoView.as_view(), name="save-video"),
    path(
        "upload/<int:video_index>",
        views.CreateCourseView.as_view(),
        name="create-course",
    ),
    path(
        "videos/<str:course_id>/<str:user_id>/<int:video_index>/",
        views.YouTubeVideoView.as_view(),
        name="yotube-video",
    ),
]
