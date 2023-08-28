from django.shortcuts import render, redirect
from ..models import Room
from django.db.models import Q
from django.db.models import Count
# Create your views here.


def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics_only = request.GET.get(
        'topic') if request.GET.get('q') != None else ''

    if not request.GET.get('page'):
        page = 1
    else:
        page = request.GET.get('page')
        page = int(page)

    if not request.GET.get('filter'):
        filter_by = 'popular'
    else:
        filter_by = 'recent'

    one_page = 10
    end_page = page * one_page
    start_page = end_page - 10

    print(start_page, end_page)

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

    rooms = rooms.filter(Q(private=False) | Q(
        participants=int(request.user.id)))

    room_count = rooms.count()
    rooms = rooms[start_page:end_page]

    context = {'rooms': rooms,
               'q': q, 'topics_only': topics_only, 'room_count': room_count}
    return render(request, 'base/home.html', context)
