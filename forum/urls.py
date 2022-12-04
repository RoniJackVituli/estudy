from django.urls import path
from forum import views

app_name = "Forum"

urlpatterns = [
    path("", views.forumView.as_view(), name="forum-main"),
    path("<user_id>", views.forumView.as_view(), name="post-post"),
    path("<user_id>/<post_id>", views.PostComments, name="comment-post"),
    path("delete/<int:post_id>/", views.DeletePost, name="delete-po"),
    path("delComment/<int:comment_id>/", views.DeleteComment, name="delete-co"),
]
