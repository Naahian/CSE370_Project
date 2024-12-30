from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User, Group
# from courses.models import Course
# from enrollment.models import Enrollment  


# @login_required(login_url="/user/login")
def dashboard(request:HttpRequest):
    usertype = getUsertype(request.user)
    if(usertype == "admin"):
        return adminDashboard(request, usertype)
    if(usertype == "student"):
        return studentDashboard(request, usertype)
    if(usertype == "teacher"):
        return teacherDashboard(request, usertype)


# @login_required(login_url="/user/login")
def adminDashboard(request:HttpRequest, usertype="admin"):
    context = {
        "user_type": usertype,
        # "courses": len(Course.objects.all()),
        # "enrollments": len(Enrollment.objects.all()),        
        "teacher":0,
        "student":0,
    }
    for user in User.objects.all():
        type = getUsertype(user)
        if(type == "teacher"): context["teacher"] +=1
        elif(type == "student"): context["student"] +=1

    return render(request, "admin_dashboard.html")


@login_required(login_url="/user/login")
def studentDashboard(request, usertype):
    context = {
        "user_type": usertype,
        # "enrollments": len(Enrollment.objects.all()),        
    }

    return render(request, "student_dashboard.html", context)


@login_required(login_url="/user/login")
def teacherDashboard(request, usertype):
    context = {
        "user_type": usertype,
        # "courses": len(Course.objects.all()),
        # "enrollments": len(Enrollment.objects.all()),        
    }

    return render(request, "teacher_dashboard.html", context)


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
