from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group

from courses.models import Course
from dashboard.models import Activity
from enrollments.models import Enrollment
# from courses.models import Course
# from enrollment.models import Enrollment  


@login_required(login_url="/users/login")
def dashboard(request:HttpRequest):
    usertype = getUsertype(request.user)
    if(usertype == "admin"):
        return redirect('admin-dashboard')
    if(usertype == "student"):
        return redirect('student-dashboard')
    if(usertype == "teacher"):
        return redirect('teacher-dashboard')


#ADMIN
@login_required(login_url="/users/login")
def adminDashboard(request:HttpRequest, usertype="admin"):
    activities = list(Activity.objects.values().order_by('-timestamp'))
    for activity in activities:
        activity["username"] = User.objects.filter(id=activity['user_id']).first().username

    context = {
        "user_type": usertype,
        "courses": len(Course.objects.all()),
        "enrollments": len(Enrollment.objects.all()),        
        "teachers":Group.objects.get(name="teacher").user_set.count(),
        "students":Group.objects.get(name="student").user_set.count(),
        "activities" : activities
    }
    return render(request, "admin_dashboard.html", context=context)


#STUDENT
@login_required(login_url="/users/login")
def studentDashboard(request, usertype="student"):
    activities = list( Activity.objects.filter(user=request.user).values().order_by('-timestamp'))
    for activity in activities:
        activity["username"] = User.objects.filter(id=activity['user_id']).first().username
    
    context = {
        "user_id": request.user.id,
        "username": request.user.username,
        "user_type": usertype,
        "enrollments": len(Enrollment.objects.all()),  
        "enrollments": len(Enrollment.objects.all()),  
        "activities":activities,
    }
    return render(request, "student_dashboard.html", context)


#TEACHER
@login_required(login_url="/users/login")
def teacherDashboard(request, usertype="teacher"):
    activities = list( Activity.objects.filter(user=request.user).values().order_by('-timestamp'))
    for activity in activities:
        activity["username"] = User.objects.filter(id=activity['user_id']).first().username

    context = {
        "user_id": request.user.id,
        "username": request.user.username,
        "user_type": usertype,
        "courses": len(Course.objects.all()),
        "enrollments": len(Enrollment.objects.all()),  
        "activities":activities,
    }
    return render(request, "teacher_dashboard.html", context)


#others
def isNotStudent(user:User):
    admin = user.groups.filter(name="admin").exists()
    teacher = user.groups.filter(name="teacher").exists()
    return (not admin and not teacher)


def getUsertype(user:User):
     if(user.groups.filter(name="admin").exists()):
        return "admin"
     elif(user.groups.filter(name="student").exists()):
        return "student"
     elif(user.groups.filter(name="teacher").exists()):
        return "teacher"
