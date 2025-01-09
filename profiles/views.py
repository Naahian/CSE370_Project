from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile

def profile_view(request:HttpRequest):
    if(not request.user.is_authenticated):
        return redirect('/users/login')
    profile = Profile.objects.get(user=request.user)
    #SELECT * FROM profile WHERE user_id = <user_id>;
    return render(request, 'profile_view.html', {'profile': profile})


# Create your views here.
