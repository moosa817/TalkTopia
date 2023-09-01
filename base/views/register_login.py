from django.shortcuts import render, redirect
from ..models import Room, Topic, Message, UserProfile
from ..forms import RoomForm, MessageForm, ProfileCreationForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
# Create your views here.


def LoginPage(request):
    page = 'login'
    context = {'page': page}
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            user = User.objects.get(email=username)
            username = user.username
        except:
            messages.error(request, 'Username or Email does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    return render(request, 'base/register_login.html', context)


def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    ProfileForm = ProfileCreationForm()
    UserForm = UserCreationForm()

    if request.method == 'POST':
        UserForm = UserCreationForm(request.POST)
        ProfileForm = ProfileCreationForm(request.POST)

        if ProfileForm.is_valid() and UserForm.is_valid():
            user = UserForm.save(commit=False)
            user.username = user.username.lower()
            user.save()

            profile = UserProfile.objects.create(
                username=user,
                name=request.POST.get('name'),
                email=request.POST.get('email').lower(),
            )

            login(request, user)
            return redirect('home')

        else:
            UserForm = UserCreationForm(request.POST)
            ProfileForm = ProfileCreationForm(request.POST)

    context = {'UserForm': UserForm, 'ProfileForm': ProfileForm}
    return render(request, 'base/register_login.html', context)


@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return redirect('home')
