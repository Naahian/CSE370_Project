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

def detail(request:HttpRequest):
    return render(request, "course_detail.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', include("dashboard.urls")),
    path('courses/', include("courses.urls")),
    path('enrollments/', include("enrollments.urls")),
    path('users/', include("users.urls")),   
    path('detail/', detail, name="detail"),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)