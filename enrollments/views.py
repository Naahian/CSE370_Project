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
    if(id):
        enrollment = Enrollment.objects.filter(id=id).first()
        return JsonResponse(enrollment.serializeJSON())
        
    enrolls = [enrollment.serializeJSON() for enrollment in Enrollment.objects.all()]
    return JsonResponse({"enrollment":enrolls})
 

@login_required
def createEnrollment(request):
    if(request.POST['user_id']):
        user = User.objects.filter(id=request.POST['user_id']).first()
    else:
        user = request.user
    course = Course.objects.filter(id=request.POST['course_id']).first()

    if Enrollment.objects.filter(user=user, course=course).exists():
        messages.error(request, "You are already enrolled in this course.")
        print("Error")
    else:
        # Create the enrollment
        print("Create the enrollment")
        enrollment = Enrollment.objects.create(user=request.user, course=course)
        Activity.objects.create(user=request.user, action="ENROLLED", details=f"Enrolled course {course.title}")
        messages.success(request, f"You have successfully enrolled in {course.title}!")
    return redirect('courses', course_id=course.id)


@login_required(login_url="/user/login")
def deleteEnrollment(request):
    return JsonResponse({})



def updateEnrollment(request):
    return JsonResponse({})
