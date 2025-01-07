from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .models import Course, Enrollment
from django.shortcuts import get_object_or_404, redirect
from myapp.models import Course, Enrollment
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
    else:
        return render(request, 'register.html')

@never_cache
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get checkbox value

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            username = user.username  

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  

                return redirect('success')  
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('login')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


@never_cache
@login_required(login_url='/login/')
def success_view(request):
    return render(request, 'success.html')

def get_courses(request):
    courses = Course.objects.all() 
    return JsonResponse({"courses": [course.serialize() for course in courses]})
   
@staff_member_required
def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        detail = request.POST.get('detail')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        modules = request.POST.get('modules')
        video_url = request.POST.get('video_url')
        thumbnail = request.FILES.get('thumbnail')  # For file uploads

        # Create the course
        Course.objects.create(
            title=title,
            detail=detail,
            price=price,
            duration=duration,
            modules=modules,
            video_url=video_url,
            thumbnail=thumbnail,
        )

        messages.success(request, "Course created successfully!")
        return redirect('courses')  # Redirect to the course list

    return render(request, 'create_course.html')

@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.detail = request.POST.get('detail')
        course.price = request.POST.get('price')
        course.duration = request.POST.get('duration')
        course.modules = request.POST.get('modules')
        course.video_url = request.POST.get('video_url')
        if 'thumbnail' in request.FILES:
            course.thumbnail = request.FILES['thumbnail'] 

        course.save()
        messages.success(request, "Course updated successfully!")
        return redirect('courses')  

    return render(request, 'update_course.html', {'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect('courses')  # Redirect to the course list

    return render(request, 'delete_course.html', {'course': course})

@login_required
def success_page(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'success.html', {'course': course})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, "You are already enrolled in this course.")
    else:
        # Create the enrollment
        Enrollment.objects.create(user=request.user, course=course)
        messages.success(request, f"You have successfully enrolled in {course.title}!")
    return redirect('course_detail', course_id=course.id)

@login_required
def get_all_users(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Permission denied. Only admins can view users.'}, status=403)

    users = User.objects.all().values('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined')
    return JsonResponse(list(users), safe=False)

# Delete a user
@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Permission denied. Only admins can delete users.'}, status=403)

    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        return JsonResponse({'error': 'Cannot delete a superuser.'}, status=403)

    user.delete()
    return JsonResponse({'message': f'User with ID {user_id} has been deleted successfully.'})
