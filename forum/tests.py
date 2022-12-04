from datetime import datetime
from django.test import TestCase, tag
from django.urls import resolve, reverse
from forum.views import forumView
from forum.models import Post
from accounts.models import User

# Create your tests here.


@tag("unit-test")
class ForumPageTestCase(TestCase):
    def test_forumView(self):
        # Act
        url = reverse("Forum:forum-main")
        # Assert
        self.assertEqual(resolve(url).func.view_class, forumView)


@tag("unit-test")
class PostTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "lectureruser",
            "password": "5t4r3e2w1q",
            "is_lecturer": True,
        }

        self.user_lecturer = User.objects.create(**self.credentials)

    def test_postView(self):
        # Act
        form = {"message": "contant!"}
        response = self.client.post(
            reverse("Forum:post-post", kwargs={"user_id": self.user_lecturer.id}),
            data=form,
            follow=True,
        )
        # Assert
        self.assertEqual(response.status_code, 200)


class PostCommentTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "lectureruser",
            "password": "5t4r3e2w1q",
            "is_lecturer": True,
        }
        
        self.user = User.objects.create_user(**self.credentials)
        self.post = Post.objects.create(user=self.user,title="title",message="message",date=datetime.today())
    @tag("unit-test")
    def testCommentView(self):
        form = {"message": "contant!"}
        response = self.client.post(
            reverse("Forum:comment-post", kwargs={"user_id": self.user.id,"post_id":self.post.id}),
            data=form,
            follow=True,
        )
        # Assert
        self.assertEqual(response.status_code, 200)

    @tag("integration-test")
    def test_create_and_delete(self):
        response = self.client.post("/acoounts/login/", self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_lecturer)
        form = {"message": "contant!"}
        response = self.client.post(
            reverse("Forum:comment-post", kwargs={"user_id": self.user.id,"post_id":self.post.id}),
            data=form,
            follow=True,
        )
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("Forum:forum-main"))
        
        response = self.client.post(
            reverse("Forum:delete-po", kwargs={"post_id":self.post.id}),
            data=form,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("Forum:forum-main"))