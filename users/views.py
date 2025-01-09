from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from dashboard.models import Activity
from profiles.models import Profile

@login_required(login_url='login/')
def getAllUsers(request):
    if(getUsertype(request.user) == "admin"):
        id = request.GET.get("id")
        #SELECT usertype FROM auth_user WHERE id = <request.user.id>;
        if(id):
            user = User.objects.values().filter(id=id).first()
            return JsonResponse(user)
            #SELECT * FROM user WHERE id = <id> LIMIT 1;

        users = [user for user in User.objects.values()]
        #SELECT * FROM user;

        for user in users:
            user_obj = User.objects.get(id=user['id'])
            #SELECT * FROM user WHERE id = <user['id']> LIMIT 1;

            user["user_type"] = getUsertype(user_obj)
            #SELECT usertype FROM user WHERE id = <user['id']>;
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
            #SELECT COUNT(*) FROM user WHERE username = '<username>';

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')
            #SELECT COUNT(*) FROM user WHERE email = '<email>';

        group = Group.objects.get(name=user_type)
        #SELECT * FROM auth_group WHERE name = '<user_type>' LIMIT 1;


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        #INSERT INTO user (username, email, password) VALUES('<username>','<email>','<hashed_password>');

        #create user
        user.save()
        user.groups.add(group)
        #INSERT INTO auth_user_groups (user_id, group_id) VALUES (<user_id>, <group_id>);

        Activity.objects.create(user=request.user, action="USER_CREATED", details=f"Created user {user.username}")
        Profile.objects.create(user=user, bio="bio",location="Dhaka")
        #INSERT INTO activity (user_id, action, details) VALUES (<request_user_id>, 'USER_CREATED', 'Created user <username>');

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
            #SELECT COUNT(*) FROM user WHERE email = '<email>';
            user = User.objects.get(email=email)
            #SELECT * FROM user WHERE email = '<email>' LIMIT 1;
            username = user.username  

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  

                return redirect('home')  
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('login')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    #DELETE FROM django_session WHERE session_key = '<current_session_key>';
    messages.success(request, "You have successfully logged out.")
    return redirect('login')




@never_cache
@login_required(login_url='/login/')
def success_view(request):
    return render(request, 'home.html')

@login_required
def deleteUser(request):
    if request.GET['id']:
        user = User.objects.filter(id = request.GET['id']).first()
        #SELECT *  FROM auth_user WHERE id = '<id>' LIMIT 1;
        if(user):
            user.delete()
            #DELETE FROM auth_user WHERE id = '<id>';
            Activity.objects.create(user=request.user, action="USER_DELETED", details=f"Deleted user {user.username}")
            #INSERT INTO activity (user_id, action, details, created_at) VALUES ('<current_user_id>', 'USER_DELETED', 'Deleted user <username>', '<timestamp>');

            messages.success(request, "user deleted successfully!")
        else:
            messages.error(request, "failed to delete user!")
        return redirect('dashboard')  # Redirect to the course list


def getUsertype(user:User):
     if(user.groups.filter(name="admin").exists()):
        #SELECT 1  FROM auth_user_groups WHERE user_id = <user_id> AND group_id = (SELECT id FROM auth_group WHERE name = 'admin')LIMIT 1;
        return "admin"
     elif(user.groups.filter(name="student").exists()):
        #SELECT 1 FROM auth_user_groups WHERE user_id = <user_id> AND group_id = (SELECT id FROM auth_group WHERE name = 'student')LIMIT 1;
        return "student"
     elif(user.groups.filter(name="teacher").exists()):
        #SELECT 1 FROM auth_user_groups WHERE user_id = <user_id> AND group_id = (SELECT id FROM auth_group WHERE name = 'teacher')LIMIT 1;
        return "teacher"
