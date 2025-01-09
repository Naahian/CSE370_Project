from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from courses.models import Course
from django.contrib.auth.models import User

from dashboard.models import Activity
from enrollments.models import Enrollment


def get_courses(request):
    course_id = request.GET.get("id")
    user_id = request.GET.get("user_id")
    if(course_id):
        course = Course.objects.filter(id=course_id).first()
        return JsonResponse(course.serialize())
        
    # Optimized query with select_related for related model and only specific fields
    courses = Course.objects.values('id','title', 'created_by__username','thumbnail')

    return JsonResponse({"courses": list(courses)})
   
   
@login_required
def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        detail = request.POST.get('detail')
        created_by_id = request.POST.get('created_by')
        duration = request.POST.get('duration')
        video_url = request.POST.get('video_url')
        thumbnail = request.FILES.get('thumbnail')  # For file uploads
        created_by = User.objects.only('id').get(id=created_by_id)
        
        # Create the course
        course = Course.objects.create( title=title, detail=detail, duration=duration, created_by=created_by, video_url=video_url, thumbnail=thumbnail)
        if(course):
            course.save()
            Activity.objects.create(user=request.user, action="COURSE_CREATED", details=f"Created course {course.title}")
            messages.success(request, "Course created successfully!")
            return redirect('dashboard')  # Redirect to the course list
        else:
            messages.error(request, "Failed to create Course!")
            return redirect('dashboard')  # Redirect to the course list

    return render(request, 'create_course.html')


@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
  
#SELECT * FROM courses WHERE id = ?;
#UPDATE courses_course
#SET title = ‘’, detail = ?, duration = ?, video_url = ?, created_by = ?, thumbnail = ?WHERE id = ?;


    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.detail = request.POST.get('detail')
        course.created_by = request.POST.get('created_by')
        course.duration = request.POST.get('duration')
        course.video_url = request.POST.get('video_url')
        if 'thumbnail' in request.FILES:
            course.thumbnail = request.FILES['thumbnail'] 

        course.save()
        messages.success(request, "Course updated successfully!")
        return redirect('courses')  

    return render(request, 'update_course.html', {'course': course})


@login_required
def delete_course(request):
    #SELECT * FROM courses WHERE id = ?;

    #DELETE FROM courses WHERE id = ?;


    if request.GET['id']:
        course = Course.objects.filter(id = request.GET['id']).first()
        if(course):
            course.delete()

            Activity.objects.create(user=request.user, action="COURSE_DELETED", details=f"deleted course {course.title}")

            messages.success(request, "course deleted successfully!")
        else:
            messages.error(request, "failed to delete course!")
        return redirect('dashboard')  # Redirect to the course list

    return render(request, 'dashboard.html', {'course': course})

def course_detail(request):
    course_id = request.GET.get("id")
    if(course_id):
        context = Course.objects.filter(id=course_id).first().serialize()
        enrolled = Enrollment.objects.filter(user__id=request.user.id)
        if(enrolled): context["enrolled"] = True
        else:context["enrolled"] = True
        return render(request, 'course_detail.html', context=context)
    else:
        messages.error(request,"course does not exist!")
        return redirect("home")
        
