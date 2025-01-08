from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from dashboard.models import Activity

@login_required(login_url='login/')
def getAllUsers(request):
    if(getUsertype(request.user) == "admin"):
        id = request.GET.get("id")
        if(id):
            user = User.objects.values().filter(id=id).first()
            return JsonResponse(user)
        
        users = [user for user in User.objects.values()]
        
        for user in users:
            user_obj = User.objects.get(id=user['id'])
            user["user_type"] = getUsertype(user_obj)
        return JsonResponse({"users":users})
    else:
        return redirect("login")


def register_view(request:HttpRequest): 
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_type = request.POST['user_type']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        group = Group.objects.get(name=user_type)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        #create user
        user.save()
        user.groups.add(group)
        Activity.objects.create(user=request.user, action="USER_CREATED", details=f"Created user {user.username}")

        #log
        if(not request.user.is_authenticated):
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        elif(getUsertype(request.user)=='admin'):
            return redirect('dashboard')
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

@login_required
def deleteUser(request):
    if request.GET['id']:
        user = User.objects.filter(id = request.GET['id']).first()
        if(user):
            user.delete()
            Activity.objects.create(user=request.user, action="USER_DELETED", details=f"Created user {user.username}")

            messages.success(request, "user deleted successfully!")
        else:
            messages.error(request, "failed to delete user!")
        return redirect('dashboard')  # Redirect to the course list


def getUsertype(user:User):
     if(user.groups.filter(name="admin").exists()):
        return "admin"
     elif(user.groups.filter(name="student").exists()):
        return "student"
     elif(user.groups.filter(name="teacher").exists()):
        return "teacher"
