from django.test import TestCase, tag
from django.urls import resolve, reverse
from DetailsAccount.views import (
    DetailsLectureView,
    DetailsStudentView,
    deleteUser,
    ChangeStudentPass,
)
from accounts.models import User

# Create your tests here.


class DetailsUrlsTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "studentuser",
            "password": "5t4r3e2w1q",
            "is_student": True,
        }

        self.user_student = User.objects.create(**self.credentials)

        self.credentials = {
            "username": "lectureruser",
            "password": "5t4r3e2w1q",
            "is_lecturer": True,
        }
        self.user_lecturer = User.objects.create(**self.credentials)

    @tag("unit-test")
    def test_showdetailsStudent(self):
        # Act
        url = reverse("Details:d-s", kwargs={"student_id": self.user_student.id})
        # Assert
        self.assertEqual(resolve(url).func.view_class, DetailsStudentView)

    @tag("unit-test")
    def test_showdetailsLecturer(self):
        # Act
        url = reverse("Details:d-l", kwargs={"lecturer_id": self.user_lecturer.id})
        # Assert
        self.assertEqual(resolve(url).func.view_class, DetailsLectureView)

    @tag("unit-test")
    def test_showdeleteUser(self):
        # Act
        url = reverse("Details:delete-user", kwargs={"user_id": self.user_lecturer.id})
        # Assert
        self.assertEqual(resolve(url).func, deleteUser)

    @tag("unit-test")
    def test_changePassword(self):
        # Act
        url = reverse("Details:ch-pass", kwargs={"user_id": self.user_lecturer.id})
        # Assert
        self.assertEqual(resolve(url).func.view_class, ChangeStudentPass)
