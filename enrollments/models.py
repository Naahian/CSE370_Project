from django.db import models
from django.contrib.auth.models import User
 
from courses.models import Course

# Create your models here.
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    completed = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    def serializeJSON(self):
        return {
            "id":self.id,
            "user":{
                "id":self.user.id,
                "username":self.user.username,
            },
            "course": {
                "id":self.course.id,
                "title":self.course.title,
                "created_by":self.course.created_by.username,
            },
            "completed":self.completed
        }
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
