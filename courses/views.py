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


def get_courses(request):
    courses = Course.objects.filter()
    course_id = request.GET.get("id")
    course_user = request.GET.get("username")
    if(course_id):
        #SELECT * FROM course WHERE id = <course_id>;
        
        course = Course.objects.all().filter(id=course_id).first()
        return JsonResponse(course.serialize())
    if(course_user):
        #SELECT * FROM auth_user WHERE username = '<course_user>';
        user = User.objects.filter(username=course_user).first()
        if user:
            # SELECT * FROM course WHERE created_by_id = <user_id>;


            course = Course.objects.filter(created_by=user).first()
            if course:
                return JsonResponse(course.serialize(), safe=False)
            return JsonResponse({"error": "No courses found for the user"}, status=404)
        return JsonResponse({"error": "User not found"}, status=404)
        
    return JsonResponse({"courses": [course.serialize() for course in courses]})
   
@login_required
def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        detail = request.POST.get('detail')
        created_by_id = request.POST.get('created_by')
        duration = request.POST.get('duration')
        video_url = request.POST.get('video_url')
        thumbnail = request.FILES.get('thumbnail')  # For file uploads
        created_by = User.objects.filter(id=created_by_id).first()
        
        # Create the course
        #INSERT INTO course (title, detail, duration, created_by_id, video_url, thumbnail)VALUES ('<title>', '<detail>', '<duration>', <created_by_id>, '<video_url>', '<thumbnail>');

        course = Course.objects.create(
            title=title,
            detail=detail,
            duration=duration,
            created_by=created_by,
            video_url=video_url,
            thumbnail=thumbnail,
        )
        Activity.objects.create(user=request.user, action="COURSE_CREATED", details=f"Created course {course.title}")
        
        
        messages.success(request, "Course created successfully!")
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
            Activity.objects.create(user=request.user, action="COURSE_DELETED", details=f"Created user {user.username}")

            messages.success(request, "course deleted successfully!")
        else:
            messages.error(request, "failed to delete course!")
        return redirect('dashboard')  # Redirect to the course list

    return render(request, 'dashboard.html', {'course': course})
