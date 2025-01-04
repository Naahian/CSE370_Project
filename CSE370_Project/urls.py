from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

#just for test, delete when home app is ready
def home(request):
    return render(request, "home.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('dashboard/', include("dashboard.urls")),
]
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

