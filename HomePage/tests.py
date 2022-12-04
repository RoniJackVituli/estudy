from datetime import datetime
from django.test import TestCase, tag
from django.urls import resolve, reverse
from accounts.models import User, Student
from HomePage.models import Post
from HomePage.views import (
    indexView,
    aboutView,
    searchView,
    updatePost,
    DownPermissions,
    UpPermissions,
    deletePost,
    updatePost,
)
from django.http import HttpRequest, HttpResponse

# Create your tests here.


# SECURITY WARNING: keep the secret key used in production secret!


@tag("unit-test")
class HomePageUrlsTest(TestCase):
    def setUp(self):
        self.user2 = User.objects.create(username="nameTest")
        self.user = User.objects.create_superuser(
            email="test@test.com",
            username="test_create_super_user",
            first_name="first name",
            last_name="last name",
            password="user password",
        )
        self.post = Post.objects.create(
            title="testTitle", date=datetime.today(), description="TestTest"
        )

    @tag("unit-test")
    def test_showHome(self):
        # Act
        url = reverse("HomePage:home")
        # Assert
        self.assertEqual(resolve(url).func.view_class, indexView)

    @tag("unit-test")
    def test_showAbout(self):
        # Act
        url = reverse("HomePage:about")
        # Assert
        self.assertEqual(resolve(url).func.view_class, aboutView)

    @tag("unit-test")
    def test_showDeletePost(self):
        # Act
        url = reverse("HomePage:delete-post", kwargs={"post_id": self.post.id})
        # Assert
        self.assertEqual(resolve(url).func, deletePost)

    @tag("unit-test")
    def test_showUpdate(self):
        # Act
        url = reverse("HomePage:update-post", kwargs={"post_id": self.post.id})
        # Assert
        self.assertEqual(resolve(url).func, updatePost)

    # SECURITY WARNING: keep the secret key used in production secret!

    @tag("unit-test")
    def test_showSearchUser(self):
        # Act
        url = reverse("HomePage:search-user")
        # Assert
        self.assertEqual(resolve(url).func.view_class, searchView)

    # SECURITY WARNING: keep the secret key used in production secret!

    @tag("unit-test")
    def test_showDownPermissions(self):
        # Act
        url = reverse("HomePage:down-per", kwargs={"user_id": self.user2.id})
        # Assertvvv
        self.assertEqual(resolve(url).func.view_class, DownPermissions)

    @tag("unit-test")
    def test_showUpPermissions(self):
        # Act
        url = reverse("HomePage:up-per", kwargs={"user_id": self.user2.id})
        # Assert
        self.assertEqual(resolve(url).func.view_class, UpPermissions)


tag("unit-test")


class PostTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            "title": "TitleTest",
            "date": datetime.today(),
            "description": "Testdescription",
        }
        self.post = Post.objects.create(**self.credentials)

    def test_title(self):
        self.assertEqual(self.post.title, "TitleTest")

    def test_date(self):
        self.date = datetime.today()
        self.post.date = self.date
        self.assertEqual(self.post.date, self.date)

    def test_description(self):
        self.assertEqual(self.post.description, "Testdescription")


@tag("unit-test")
class SearchTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "studentuser",
            "password": "5t4r3e2w1q",
            "is_student": True,
        }
        self.user = User.objects.create(**self.credentials)
        self.student = Student.objects.create(user=self.user, ID="315369967")
        self.user.save()
        self.student.save()

    @tag("unit-test")
    def test_searchUser(self):
        response = self.client.get(reverse("HomePage:search-user"))
        self.assertEqual(response.status_code, 200)

    @tag("unit-test")
    def test_searchUserExsits(self):
        form_data = {"search": "315369967"}
        response = self.client.post(
            reverse("HomePage:search-user"), data=form_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["exsits"])

    @tag("unit-test")
    def test_searchUserNotExsits(self):
        form_data = {"search": "123456789"}
        response = self.client.post(
            reverse("HomePage:search-user"), data=form_data, follow=True
        )
        self.assertEqual(response.context["error"], "User no found")
