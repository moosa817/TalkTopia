from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics_only = request.GET.get(
        'topic') if request.GET.get('q') != None else ''

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
    context = {'rooms': rooms,
               'q': q, 'topics_only': topics_only}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.filter()

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}

    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    from_url = request.GET.get(
        'from') if request.GET.get('from') else 'home'

    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            private = form.cleaned_data['private']
            print(private, type(private))
            # Separate handling for topic creation
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)

            room = Room.objects.create(
                host=request.user,
                topic=topic,
                name=name,
                description=description,
                private=private
            )

            room.participants.add(request.user)
            if from_url == 'profile':
                return redirect(from_url, pk=str(request.user))
            else:
                return redirect(from_url)
    else:
        form = RoomForm()

    context = {'form': form, 'from_url': from_url,
               'topics': Topic.objects.all()}
    return render(request, 'base/roomform.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    from_url = request.GET.get(
        'from') if request.GET.get('from') else 'home'

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    context = {}
    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            if from_url == 'profile':
                return redirect(from_url, pk=str(request.user))
            else:
                return redirect(from_url)
    else:
        # coudnt get current_topic value for html simply(was instead getting id)

        current_topic = form['topic'].value()
        if current_topic:
            current_topic = Topic.objects.get(id=current_topic)
            context = {'form': form, 'updateRoom': True,
                       'current_topic': current_topic, 'from_url': from_url}
        else:
            context = {'form': form, 'updateRoom': False, 'from_url': from_url}

        return render(request, 'base/roomform.html', context)

    return render(request, 'base/roomform.html', context)


@login_required(login_url='login')
def deleteRoom(request):
    if request.method == 'POST':
        pk = request.POST.get('room_id')
        user = request.POST.get('user')
        if str(request.user) != str(user):
            return HttpResponse('You are not allowed here')
        room = Room.objects.get(id=pk)
        room.delete()
        return JsonResponse({'success': True})


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
