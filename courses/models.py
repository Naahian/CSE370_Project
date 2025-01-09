from django.db import models
from django.contrib.auth.models import User


def get_default_user():
    return User.objects.first()   

class Course(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user, db_index=True)
    detail = models.TextField()
    duration = models.CharField(max_length=50)
    video_url = models.URLField(max_length=300,null=False, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    


    def __str__(self):
        return self.title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_by": {
                "id": self.created_by.id,
                "username": self.created_by.username,
            },
            "detail": self.detail,
            "duration": self.duration,
            "video_url": self.video_url,
            "thumbnail": self.thumbnail.url if self.thumbnail else None,
        }
    

