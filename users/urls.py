from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.getAllUsers, name='users'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_view, name='success'),
    path('delete/', views.deleteUser, name='delete-user'),
]
