from django.urls import path
from . import views

urlpatterns = [
    path('', views.getEnrollments, name='all-enrollments'),
    path('enroll', views.createEnrollment, name='enroll-course'),
]
