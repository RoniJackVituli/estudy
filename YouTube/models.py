from django.db import models

# Create your models here.


class YouTube(models.Model):
    index = models.IntegerField()
    channelId = models.CharField(max_length=100)
    IdVideo = models.CharField(max_length=100)
    profile = models.URLField()
    title = models.CharField(max_length=256)
    thumbnails = models.URLField()

    def __str__(self):
        return "the channelID is " + str(self.channelId)
