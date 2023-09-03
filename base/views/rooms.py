from django.shortcuts import render, redirect
from ..models import Room, Topic, Message
from ..forms import RoomForm, MessageForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
# Create your views here.


@login_required(login_url='login')
def createRoom(request):
    from_url = request.GET.get(
        'from') if request.GET.get('from') else 'home'

    if request.method == 'POST':
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
