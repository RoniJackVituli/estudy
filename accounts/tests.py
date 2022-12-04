from django.test import TestCase, tag
from accounts.models import User, Student, Lecturer
from accounts.views import signUp, signStudentView, signLectureView
from django.urls import resolve, reverse


@tag("unit-test")
class StudentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="Dana", is_student=True, is_lecturer=False, permissions=True
        )
        Student.objects.create(
            user=user,
            first_name="Dana",
            last_name="Abutbul",
            Phone="+97254679521",
            ID="123456789",
        )
        user = User.objects.create(
            username="Yosi", is_student=True, is_lecturer=False, permissions=True
        )
        Student.objects.create(
            user=user,
            first_name="Yosi",
            last_name="Alfsi",
            Phone="+97254679521",
            ID="258963147",
        )
        user = User.objects.create(
            username="Ben", is_student=True, is_lecturer=False, permissions=True
        )
        Student.objects.create(
            user=user,
            first_name="Ben",
            last_name="Vitali",
            Phone="+97254679521",
            ID="159753963",
        )
        user = User.objects.create(
            username="Dor", is_student=True, is_lecturer=False, permissions=True
        )
        Student.objects.create(
            user=user,
            first_name="Dor",
            last_name="Rosluv",
            Phone="+97254679521",
            ID="357412586",
        )

        user = User.objects.create(
            username="Marina", is_student=False, is_lecturer=True, permissions=True
        )
        Lecturer.objects.create(
            user=user,
            first_name="Marina",
            last_name="Abutbul",
            Phone="+97254679521",
            ID="123456789",
        )
        user = User.objects.create(
            username="Karim", is_student=False, is_lecturer=True, permissions=True
        )
        Lecturer.objects.create(
            user=user,
            first_name="Karim",
            last_name="Vitali",
            Phone="+97254679521",
            ID="123456789",
        )
        user = User.objects.create(
            username="Hadas", is_student=False, is_lecturer=True, permissions=True
        )
        Lecturer.objects.create(
            user=user,
            first_name="Hadas",
            last_name="Rosluv",
            Phone="+97254679521",
            ID="123456789",
        )

    def test_student_exsits(self):
        dana = User.objects.get(username="Dana")
        yosi = User.objects.get(username="Yosi")
        ben = User.objects.get(username="Ben")
        self.assertEqual(Student.objects.filter(user=dana).exists(), True)
        self.assertEqual(Student.objects.filter(user=yosi).exists(), True)
        self.assertEqual(Student.objects.filter(user=ben).exists(), True)

    def test_has_permissions(self):
        dana = User.objects.get(username="Dana")
        yosi = User.objects.get(username="Yosi")
        ben = User.objects.get(username="Ben")
        karim = User.objects.get(username="Karim")
        marina = User.objects.get(username="Marina")
        hadas = User.objects.get(username="Hadas")

        self.assertEqual(dana.permissions, True)
        self.assertEqual(yosi.permissions, True)
        self.assertEqual(ben.permissions, True)
        self.assertEqual(karim.permissions, True)
        self.assertEqual(marina.permissions, True)
        self.assertEqual(hadas.permissions, True)

    def test_is_student(self):
        dana = User.objects.get(username="Dana")
        yosi = User.objects.get(username="Yosi")
        ben = User.objects.get(username="Ben")
        self.assertEqual(dana.is_student, True)
        self.assertEqual(yosi.is_student, True)
        self.assertEqual(ben.is_student, True)

        karim = User.objects.get(username="Karim")
        marina = User.objects.get(username="Marina")
        hadas = User.objects.get(username="Hadas")

        self.assertEqual(karim.is_student, False)
        self.assertEqual(marina.is_student, False)
        self.assertEqual(hadas.is_student, False)


@tag("unit-test")
class LecturerTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="Dana", is_student=True, is_lecturer=False, permissions=True
        )
        Student.objects.create(
            user=user,
            first_name="Dana",
            last_name="Abutbul",
            Phone="+97254679521",
            ID="123456789",
        )
        user = User.objects.create(
            username="Yosi", is_student=True, is_lecturer=False, permissions=True
        )
        Student.objects.create(
            user=user,
            first_name="Yosi",
            last_name="Alfsi",
            Phone="+97254679521",
            ID="258963147",
        )
        user = User.objects.create(
            username="Ben", is_student=True, is_lecturer=False, permissions=True
        )
        Student.objects.create(
            user=user,
            first_name="Ben",
            last_name="Vitali",
            Phone="+97254679521",
            ID="159753963",
        )
        user = User.objects.create(
            username="Dor", is_student=True, is_lecturer=False, permissions=True
        )
        Student.objects.create(
            user=user,
            first_name="Dor",
            last_name="Rosluv",
            Phone="+97254679521",
            ID="357412586",
        )

        user = User.objects.create(
            username="Marina", is_student=False, is_lecturer=True, permissions=True
        )
        Lecturer.objects.create(
            user=user,
            first_name="Marina",
            last_name="Abutbul",
            Phone="+97254679521",
            ID="123456789",
        )
        user = User.objects.create(
            username="Karim", is_student=False, is_lecturer=True, permissions=True
        )
        Lecturer.objects.create(
            user=user,
            first_name="Karim",
            last_name="Vitali",
            Phone="+97254679521",
            ID="123456789",
        )
        user = User.objects.create(
            username="Hadas", is_student=False, is_lecturer=True, permissions=True
        )
        Lecturer.objects.create(
            user=user,
            first_name="Hadas",
            last_name="Rosluv",
            Phone="+97254679521",
            ID="123456789",
        )

    def test_lectuere_exsits(self):
        karim = User.objects.get(username="Karim")
        marina = User.objects.get(username="Marina")
        hadas = User.objects.get(username="Hadas")

        self.assertEqual(Lecturer.objects.filter(user=karim).exists(), True)
        self.assertEqual(Lecturer.objects.filter(user=marina).exists(), True)
        self.assertEqual(Lecturer.objects.filter(user=hadas).exists(), True)

    def test_is_lecturer(self):
        dana = User.objects.get(username="Dana")
        yosi = User.objects.get(username="Yosi")
        ben = User.objects.get(username="Ben")
        self.assertEqual(dana.is_lecturer, False)
        self.assertEqual(yosi.is_lecturer, False)
        self.assertEqual(ben.is_lecturer, False)

        karim = User.objects.get(username="Karim")
        marina = User.objects.get(username="Marina")
        hadas = User.objects.get(username="Hadas")

        self.assertEqual(karim.is_lecturer, True)
        self.assertEqual(marina.is_lecturer, True)
        self.assertEqual(hadas.is_lecturer, True)


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "5t4r3e2w1q"}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post("/acoounts/login/", self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context["user"].is_authenticated)

    def test_admin(self):
        response = self.client.post("/acoounts/login/", self.credentials, follow=True)
        self.assertFalse(response.context["user"].is_superuser)

    def test_student_login(self):
        self.credentials = {
            "username": "studentuser",
            "password": "5t4r3e2w1q",
            "is_student": True,
        }
        User.objects.create_user(**self.credentials)

        response = self.client.post("/acoounts/login/", self.credentials, follow=True)

        self.assertTrue(response.context["user"].is_student)

    def test_lecturer_login(self):
        self.credentials = {
            "username": "lectureruser",
            "password": "5t4r3e2w1q",
            "is_lecturer": True,
        }
        User.objects.create_user(**self.credentials)

        response = self.client.post("/acoounts/login/", self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_lecturer)


class LogOutTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "testuser",
            "password": "5t4r3e2w1q",
            "is_lecturer": True,
        }
        User.objects.create_user(**self.credentials)
        self.client.post("/acoounts/login/", self.credentials, follow=True)

    def test_student_logout(self):
        self.credentials = {
            "username": "studentuser",
            "password": "5t4r3e2w1q",
            "is_student": True,
        }
        User.objects.create_user(**self.credentials)
        self.client.post("/acoounts/login/", self.credentials, follow=True)
        response = self.client.post("/acoounts/logout/", self.credentials, follow=True)
        self.assertFalse(response.context["user"].is_authenticated)

    def test_lecturer_logout(self):
        response = self.client.post("/acoounts/logout/", self.credentials, follow=True)
        self.assertFalse(response.context["user"].is_authenticated)


@tag("unit-test")
class URLTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Dana", is_student=True, is_lecturer=False, permissions=True
        )

    def test_signUp_url(self):
        url = reverse("accounts:signup")
        self.assertEqual(resolve(url).func, signUp)

    def test_signupStudent_url(self):
        url = reverse("accounts:si-student")
        self.assertEqual(resolve(url).func.view_class, signStudentView)

    def test_signupLecture_url(self):
        url = reverse("accounts:si-lecture")
        self.assertEqual(resolve(url).func.view_class, signLectureView)


class LoginViewTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "testuser",
            "password": "5t4r3e2w1q",
            "email": "testadmin@estudy.com",
        }
        User.objects.create_superuser(**self.credentials)

    @tag("integration-test")
    def test_login_and_logout_admin(self):
        # Arrange
        login_form_data = {"username": "testuser", "password": "5t4r3e2w1q", "is_superuser":True}

        # Act
        response = self.client.post(reverse("login"), data=login_form_data, follow=True)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("HomePage:home"))
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertTrue(response.context["user"].is_superuser)

        # Act
        response = self.client.post("/acoounts/logout/", follow=True)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)

    @tag("integration-test")
    def test_login_and_logout_user_student(self):
        self.credentials = {
            "username": "student",
            "password": "5t4r3e2w1q",
            "is_student":True,
        }
        User.objects.create_user(**self.credentials)
        # Act
        response = self.client.post("/acoounts/login/", self.credentials, follow=True)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("HomePage:home"))
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertTrue(response.context["user"].is_student)

        # Act
        response = self.client.post("/acoounts/logout/", follow=True)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)


    @tag("integration-test")
    def test_login_and_logout_user_lecturer(self):
        self.credentials = {
            "username": "lecturer",
            "password": "5t4r3e2w1q",
            "is_lecturer":True,
        }
        User.objects.create_user(**self.credentials)
        # Act
        response = self.client.post("/acoounts/login/", self.credentials, follow=True)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("HomePage:home"))
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertTrue(response.context["user"].is_lecturer)

        # Act
        response = self.client.post("/acoounts/logout/", follow=True)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)
