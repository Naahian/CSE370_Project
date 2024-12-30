from django.db import models
from django.contrib.auth.models import User

# class Dashboard(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE) 
#     title = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
  
#     def serializeJSON(self):
#         return  {
#             "user": self.user.username,  
#             "title": self.title,
#             "created_at": self.created_at.isoformat(),
#             "updated_at": self.updated_at.isoformat(),
#             "widgets": [widget.id for widget in self.widgets.all()]  
#         }

#     def __str__(self):
#         return self.title
    
#     class Meta:
#         ordering = ['-updated_at']  # Order dashboards by last updated

