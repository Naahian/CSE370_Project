from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

def home(request):
    return render(request, "home.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', include("dashboard.urls")),
    path('courses/', include("courses.urls")),
    path('enrollments/', include("enrollments.urls")),
    path('users/', include("users.urls")),   
]
