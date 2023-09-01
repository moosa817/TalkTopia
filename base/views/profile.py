from django.shortcuts import render, redirect
from ..models import Room, Topic, Message
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


def UserProfile(request, pk):
    user = User.objects.get(username=pk)
    rooms = Room.objects.filter(host=user)

    context = {'user': user, 'rooms': rooms}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def JoinedRooms(request):
    user_id = request.user.id

    rooms = Room.objects.filter(participants=user_id)
    context = {'rooms': rooms}
    return render(request, 'base/joined_rooms.html', context)


@login_required(login_url='login')
def AccountSettings(request):
    context = {}
    return render(request, 'base/account_settings.html', context)
