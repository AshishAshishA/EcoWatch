from django.db import models

class WasteSite(models.Model):
    city_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()
    video = models.OneToOneField('Video', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"video:{self.video_file} uploaded_ad{self.uploaded_at}"