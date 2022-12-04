from django.test import TestCase, tag
from category.models import Course, HomeWork
from category.models import User
from django.urls import resolve, reverse
from category.form import CreatCourseForm, CourseForm
from category.apps import CategoryConfig
from category.views import (
    CategoryView,
    HomeWorksView,
    UploadFileView,
    CreateCourseView,
    ForumFileView,
    deleteCourse,
    deleteFile,
)

# Create your tests here.

######################################################################
@tag("unit-test")
class CourseTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name_course="testCourse")

    def test_department(self):
        self.assertEqual(self.course.department, "1")

    def test_semester(self):
        self.assertEqual(self.course.semester, "1")

    def test_year(self):
        self.assertEqual(self.course.year, "1")

    def test_kind_of(self):
        self.assertEqual(self.course.kind_of, "1")

    def test_name_course(self):
        self.assertEqual(self.course.name_course, "testCourse")


@tag("unit-test")
class HomeWorkTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="nameTest")
        self.course = Course.objects.create(name_course="testCourse")
        self.hw = HomeWork.objects.create(
            course=self.course, user=self.user, nameFile="hwTest"
        )

    def test_user(self):
        self.assertEqual(self.hw.user.username, "nameTest")

    def test_course(self):
        self.assertEqual(self.hw.course.name_course, "testCourse")

    def test_hw(self):
        self.assertEqual(self.hw.nameFile, "hwTest")

    def test_update(self):
        self.assertEqual(self.hw.nameFile, "hwTest")
        # Update
        self.hw.nameFile = "newNameFile"
        self.assertEqual(self.hw.nameFile, "newNameFile")

    def test_homework_Notexsits(self):
        self.assertFalse(HomeWork.objects.filter(pk=1111).exists(), False)

    def test_homework_exsits(self):
        self.assertTrue(HomeWork.objects.filter(pk=self.hw.id).exists, True)


######################################################################


@tag("unit-test")
class ProfileAppsTestCase(TestCase):
    def test_apps_name(self):
        # Assert
        self.assertEqual(CategoryConfig.name, "category")


######################################################################


@tag("unit-test")
class CategoryUrlsTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "studentuser",
            "password": "5t4r3e2w1q",
            "is_student": True,
        }
        self.user = User.objects.create_user(**self.credentials)
        self.course = Course.objects.create(name_course="testCourse")
        self.hw = HomeWork.objects.create(
            user=self.user, course=self.course, nameFile="hwTest"
        )

    def test_showCategory(self):
        # Act
        url = reverse("Category:cat", kwargs={"user_id": self.user.id})
        # Assert
        self.assertEqual(resolve(url).func.view_class, CategoryView)

    def test_showHomeWork(self):
        # Act
        url = reverse(
            "Category:homework",
            kwargs={"course_id": self.course.id, "user_id": self.user.id},
        )
        # Assert
        self.assertEqual(resolve(url).func.view_class, HomeWorksView)

    def test_showUploadFileView(self):
        # Act
        url = reverse(
            "Category:u-f",
            kwargs={"course_id": self.course.id, "user_id": self.user.id},
        )
        # Assert
        self.assertEqual(resolve(url).func.view_class, UploadFileView)

    def test_showdeleteFile(self):
        # Act
        url = reverse(
            "Category:delete-file",
            kwargs={"course_id": self.course.id, "hw_id": self.hw.id},
        )
        # Assert
        self.assertEqual(resolve(url).func, deleteFile)


class CreateCourseTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "LecturerUser",
            "password": "5t4r3e2w1q",
            "is_lecturer": True,
        }
        self.user = User.objects.create_user(**self.credentials)

    @tag("unit-test")
    def test_create(self):
        response = self.client.get(reverse("Category:create-course"))
        self.assertEqual(response.status_code, 200)

    @tag("unit-test")
    def test_create_form(self):
        response = self.client.get(reverse("Category:create-course"))
        self.assertEqual(type(response.context["folder"]), CreatCourseForm)

    @tag("unit-test")
    def test_create_course(self):
        response = self.client.get(reverse("Category:create-course"))
        self.assertEqual(type(response.context["form"]), CourseForm)

    @tag("unit-test")
    def test_post_course(self):
        # "department", "year", "semester", "name_course", "kind_of")
        form_data = {
            "department": "1",
            "year": "1",
            "semester": "1",
            "name_course": "test",
            "kind_of": "1",
        }
        response = self.client.post(reverse("Category:create-course"), data=form_data)
        self.assertEqual(response.status_code, 302)


######################################################


class HomeWorksTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "TestUser",
            "password": "5t4r3e2w1q",
            "is_student": True,
        }
        self.user = User.objects.create_user(**self.credentials)
        self.course = Course.objects.create(name_course="testCourse")

    @tag("unit-test")
    def test_select_option_one(self):
        form_data = {"selecting": "1"}
        response = self.client.get(
            reverse(
                "Category:homework",
                kwargs={"course_id": self.course.id, "user_id": self.user.id},
            ),
            data=form_data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["1"], "1")

    @tag("unit-test")
    def test_select_option_two(self):
        form_data = {"selecting": "2"}
        response = self.client.get(
            reverse(
                "Category:homework",
                kwargs={"course_id": self.course.id, "user_id": self.user.id},
            ),
            data=form_data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["2"], "2")


######################################################
class ForumTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "studentuser",
            "password": "5t4r3e2w1q",
            "is_student": True,
        }
        self.user = User.objects.create_user(**self.credentials)
        self.course = Course.objects.create(name_course="testCourse")
        self.hw = HomeWork.objects.create(
            user=self.user, course=self.course, nameFile="hwTest"
        )

    @tag("unit-test")
    def test_showforum(self):
        # Act
        url = reverse("Category:forum-file", kwargs={"hw_id": self.hw.id})
        # Assert
        self.assertEqual(resolve(url).func.view_class, ForumFileView)

    @tag("unit-test")
    def test_post_forum(self):
        response = self.client.post(
            reverse("Category:forum-file", kwargs={"hw_id": self.hw.id}),
            data={"hw_id": self.hw.id},
        )
        self.assertEqual(response.status_code, 302)
