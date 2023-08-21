from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.db.models import Count
# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics_only = request.GET.get(
        'topic') if request.GET.get('q') != None else ''

    top_topics = Topic.objects.annotate(
        room_count=Count('room')).order_by('-room_count')[:7]
    top_topics_name = [topic.name for topic in top_topics]
    topics = Topic.objects.all()

    topics_only = True if topics_only and q in [
        topic.name for topic in topics] else False

    if topics_only:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q)
        )

    else:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    print(topics_only)
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q) | Q(room__name__icontains=q) |
        Q(room__description__icontains=q)).order_by('-updated')

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages, 'top_topics': top_topics, 'top_topics_names': top_topics_name, 'q': q, 'topics_only': topics_only}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.filter()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('message')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}

    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']

            # Separate handling for topic creation
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)

            Room.objects.create(
                host=request.user,
                topic=topic,
                name=name,
                description=description,
            )
            return redirect('home')
    else:
        form = RoomForm()

    context = {'form': form, 'topics': Topic.objects.all()}
    return render(request, 'base/room-form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room-form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


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
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    return render(request, 'base/register_login.html', context)


def RegisterPage(request):
    form = UserCreationForm()
    context = {'form': form}
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/register_login.html', context)


@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=message.room.id)
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def EditMessage(request, pk):
    msg = Message.objects.get(id=pk)
    msg_form = MessageForm(instance=msg)

    if request.user != msg.user:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=msg)
        if form.is_valid():
            form.save()
            return redirect('room', pk=msg.room.id)

    context = {'msg': msg, 'form': msg_form}
    return render(request, 'base/edit_msg.html', context)


def UserProfile(request, user):
    user = User.objects.get(username=user)
    rooms = Room.objects.filter(host=user)
    context = {'user': user, 'rooms': rooms}

    return render(request, 'base/profile.html', context)
