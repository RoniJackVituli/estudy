import datetime
from django.db import models
from accounts.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from gridfs_storage.storage import GridFSStorage

# Create your models here.

# Define your GrifFSStorage instance

DEPARTMENT_CHOICES = (
    ("1", "הנדסת תוכנה"),
    ("2", "הנדסת בניין"),
    ("3", "הנדסת מכונות"),
    ("4", "הנדסת חשמל"),
    ("5", "הנדסה כימית"),
)

YEAR_CHOICES = (
    ("1", "שנה א"),
    ("2", "שנה ב"),
    ("3", "שנה ג"),
    ("4", "שנה ד"),
)

SEMESTER_CHOICES = (
    ("1", "סמסטר א"),
    ("2", "סמסטר ב"),
    ("3", "סמסטר קיץ"),
)

KIND_CHOICES = (
    ("1", "הרצאות"),
    ("2", "תרגולים"),
    ("3", "עבודות בית"),
    ("3", "מבחנים"),
    ("5", "YouTube"),
    ("6", "Zoom"),
)


class Course(models.Model):
    name_course = models.CharField(
        max_length=30,
    )
    department = models.CharField(
        max_length=30,
        choices=DEPARTMENT_CHOICES,
        default="1",
    )
    year = models.CharField(max_length=30, choices=YEAR_CHOICES, default="1")
    semester = models.CharField(max_length=30, choices=SEMESTER_CHOICES, default="1")
    kind_of = models.CharField(max_length=30, choices=KIND_CHOICES, default="1")

    def __str__(self):
        return str(self.name_course)


class HomeWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    nameFile = models.CharField("Name File", max_length=30)
    file = models.FileField(
        "File",
        upload_to="files",
        null=True,
        storage=GridFSStorage(base_url="https://ik.imagekit.io/zyae7okkm/"),
    )
    ratings = GenericRelation(Rating, related_query_name="homework")

    def __str__(self):
        return str(self.nameFile)


class CommentHomeWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hw = models.ForeignKey(HomeWork, on_delete=models.CASCADE)
    message = models.TextField(max_length=256, null=True)
    date = models.DateField(default=datetime.date.today)



class YouTubeVideo(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    channelId = models.CharField(max_length=100)
    IdVideo = models.CharField(max_length=100)
    profile = models.URLField()
    title = models.CharField(max_length=256)
    thumbnails = models.URLField()
    ratings = GenericRelation(Rating, related_query_name="youtubevideo")

    def __str__(self):
        return str(self.channelId)
