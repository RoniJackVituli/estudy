from django.urls import path
from DetailsAccount import views

app_name = "Details"

urlpatterns = [
    path("detailsStudent/<student_id>", views.DetailsStudentView.as_view(), name="d-s"),
    path(
        "detailsLecturer/<lecturer_id>", views.DetailsLectureView.as_view(), name="d-l"
    ),
    path("Delete/<user_id>", views.deleteUser, name="delete-user"),
    path("changePassword/<user_id>", views.ChangeStudentPass.as_view(), name="ch-pass"),
]
