from http.client import responses
from django.test import TestCase, tag
from django.urls import reverse,resolve
from accounts.models  import User
from category.models  import Course, YouTubeVideo
from YouTube.views import SearchVideoView
# Create your tests here.

@tag('unit-test')
class YouTubeTest(TestCase):

  def setUp(self):
      self.credentials = {
            "username": "lectureruser",
            "password": "5t4r3e2w1q",
            "is_lecturer": True,
        }

      self.user = User.objects.create_user(**self.credentials)
      self.course = Course.objects.create(name_course="Test",kind_of="5")
  def test_url(self):
    url = reverse("YouTube:youtube")
    self.assertEqual(resolve(url).func.view_class, SearchVideoView)

  def test_get(self):
    response = self.client.get(reverse("YouTube:youtube"))
    self.assertEqual(response.status_code, 200)


  def test_post(self):
    search = "c++"
    response = self.client.post(reverse("YouTube:youtube"),data={'search':search})
    self.assertEqual(response.status_code, 200)

  def test_post_return(self):
    search = "python"
    response = self.client.post(reverse("YouTube:youtube"),data={'search':search})
    self.assertNotEquals(response.context['videos'],None)



  @tag("integration-test")
  def test_create_and_delete(self):
      response = self.client.post("/acoounts/login/", self.credentials, follow=True)
      self.assertTrue(response.context["user"].is_lecturer)
      
      search = "c++"
      response = self.client.post(reverse("YouTube:youtube"), data={'search':search})
      id_video = response.context['videos'][0]['index']
      self.assertNotEquals(response.context['videos'],None)
    
      form_da = {"department":"1", "year":"1", "semester":"1","kind_of":"5"}
      response = self.client.post(reverse("YouTube:save-video", kwargs={'video_index':id_video}), data=form_da)

      youtube = YouTubeVideo.objects.create(id = 3874783, user=self.user, course=self.course, channelId="channelId", IdVideo="test",profile="profile",title="title",thumbnails='thumbnails')

      response = self.client.get(reverse('Category:delete-video',kwargs={'course_id':self.course.id,'video_id':youtube.id}))

      self.assertEqual(response.status_code,302)
      self.assertRedirects(response, reverse("Category:videos",kwargs={'course_id':self.course.id}))






