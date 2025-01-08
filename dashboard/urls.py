from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),     
    path('admin', views.adminDashboard, name='admin-dashboard'),     
    path('student', views.studentDashboard, name='student-dashboard'),     
    path('teacher', views.teacherDashboard, name='teacher-dashboard'),     
]