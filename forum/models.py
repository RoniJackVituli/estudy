import datetime
from django.db import models
from accounts.models import User

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    message = models.TextField(max_length=256, null=True)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField(max_length=256, null=True)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.post)
