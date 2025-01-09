from django.shortcuts import  redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from courses.models import Course
from dashboard.models import Activity
from .models import Enrollment

@login_required(login_url="/user/login")
def getEnrollments(request):
    id = request.GET.get("id")
    user_id = request.GET.get("user_id")
    if(id):
        enrollment = Enrollment.objects.filter(id=id).first()
        return JsonResponse(enrollment.serializeJSON())
    if(user_id):
        enrollments = Enrollment.objects.filter(user__id=user_id)
        enrolls = [enrollment.serializeJSON() for enrollment in enrollments]
        return JsonResponse({"enrollment":enrolls})
        
    enrolls = [enrollment.serializeJSON() for enrollment in Enrollment.objects.all()]
    return JsonResponse({"enrollment":enrolls})
 

@login_required
def createEnrollment(request):
    user_id = request.POST.get('user_id')
    course_id = request.POST.get('course_id')
    if(user_id):
        user = User.objects.filter(id=user_id).first()
    else:
        user = request.user
    if(course_id):course = Course.objects.filter(id=course_id).first()
 

    if Enrollment.objects.filter(user=user, course=course).exists():
        messages.error(request, "You are already enrolled in this course.")
    else:
        # Create the enrollment
        enrollment = Enrollment.objects.create(user=user, course=course)
        enrollment.save
        Activity.objects.create(user=user, action="ENROLLED", details=f"Enrolled course {course.title}")
        messages.success(request, f"You have successfully enrolled in {course.title}!")
        
    return redirect('dashboard')


@login_required(login_url="/user/login")
def deleteEnrollment(request):
    return JsonResponse({})



def updateEnrollment(request):
    return JsonResponse({})
