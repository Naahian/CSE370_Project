from django.urls import path
from . import views


urlpatterns = [
    # path('', views, name='all-courses'),
    path('', views.get_courses, name='courses'),
    path('courses/create/', views.create_course, name='create_course'),  # Create course
    path('courses/<int:course_id>/update/', views.update_course, name='update_course'),  # Update course
    path('delete/', views.delete_course, name='delete_course'),
]
