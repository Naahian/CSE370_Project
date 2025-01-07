from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_view, name='success'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('courses/', views.get_courses, name='courses'),
    path('courses/create/', views.create_course, name='create_course'),  # Create course
    path('courses/<int:course_id>/update/', views.update_course, name='update_course'),  # Update course
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),  # Delete course
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)