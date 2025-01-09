from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings

from django.conf.urls.static import static
from django.urls import path, include

def home(request:HttpRequest):
    context = {}
    if(request.user.is_authenticated):
        context = {
            "username":request.user.username,
        }
        print(context)
    return render(request, "home.html", context= context)

def allCourse(request:HttpRequest):
    return render(request, "all_courses.html")










urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', include("dashboard.urls")),
    path('courses/', include("courses.urls")),
    path('enrollments/', include("enrollments.urls")),
    path('users/', include("users.urls")),   
    path('profiles/', include("profiles.urls")),   
    path('all_courses/', allCourse, name='allCourse'),    
    path('profiles/', include("profiles.urls")),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)