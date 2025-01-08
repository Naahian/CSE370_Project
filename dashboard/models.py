from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    ACTION_CHOICES = [
        ("USER_CREATED", "User Created"),
        ("USER_CREATED", "User Deleted"),
        ("COURSE_CREATED", "Course Created"),
        ("COURSE_DELETED", "Course Deleted"),
        ("ENROLLED", "Enrolled"),
        ("COMPLETED", "Enrollment Completed"),
    ]
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True) 
    
    def serializeJSON(self):
        return  {
            "user": self.user.username,  
            "action": self.action,
            "timestamp": self.timestamp.isoformat(),  
        }

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"



