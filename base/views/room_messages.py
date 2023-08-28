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


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.filter()

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}

    return render(request, 'base/room.html', context)


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
