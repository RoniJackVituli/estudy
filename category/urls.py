from django.urls import path
from category import views

app_name = "Category"

urlpatterns = [
    path("<user_id>", views.CategoryView.as_view(), name="cat"),
    path(
        "course/<course_id>/<user_id>", views.HomeWorksView.as_view(), name="homework"
    ),
    path(
        "upload-file/<course_id>/<user_id>", views.UploadFileView.as_view(), name="u-f"
    ),
    path("upload/", views.CreateCourseView.as_view(), name="create-course"),
    path("del/<course_id>", views.deleteCourse, name="delete-course"),
    path("delfile/<course_id>/<hw_id>", views.deleteFile, name="delete-file"),
    path("delVideo/<course_id>/<video_id>", views.deleteVideo, name="delete-video"),
    path("videos/<course_id>/cc", views.VideoView.as_view(), name="videos"),
    path("forumFile/<hw_id>", views.ForumFileView.as_view(), name="forum-file"),
    path("delComment/<int:comment_id>/<hw_id>", views.DeleteComment, name="delete-co"),
]
