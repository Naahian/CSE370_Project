from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 

    def __str__(self):
        return self.email
    
def get_default_user():
        return User.objects.first()  

class Course(models.Model):
    title = models.CharField(max_length=255)
    detail = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    duration = models.CharField(max_length=50)
    modules = models.IntegerField()
    video_url = models.URLField(max_length=200, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title

    def serialize(self):
        return{"id": self.id, "title": self.title, "detail": self.detail,}


created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"