from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models import Room
from django.db.models import Q
from django.db.models import Count
from guest_user.decorators import allow_guest_user


@allow_guest_user
def welcome_user(request):
    next = 'home' if not request.GET.get('next') else request.GET.get('next')

    return redirect(next)
